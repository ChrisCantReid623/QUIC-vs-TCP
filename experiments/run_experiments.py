#!/usr/bin/env python3
"""Automated TCP vs. QUIC experiments."""

import argparse
import csv
import re
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from topology.network import create_network


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--protocol",
        choices=["tcp", "quic"],
        default="tcp",
    )
    parser.add_argument(
        "--congestion",
        choices=["cubic", "reno"],
        default="cubic",
    )
    parser.add_argument("--rtt", type=float, default=100)
    parser.add_argument("--loss", type=float, default=0)
    args = parser.parse_args()

    if args.rtt < 0:
        parser.error("RTT must be nonnegative.")
    if not 0 <= args.loss <= 100:
        parser.error("Packet loss must be between 0 and 100%.")

    if args.protocol == "quic" and args.congestion != "reno":
        parser.error("QUIC currently supports Reno only.")

    print("\n=== Automated Experiment Runner ===", flush=True)
    print(f"Protocol: {args.protocol.upper()} {args.congestion.upper()}", flush=True)
    print(f"RTT: {args.rtt:g} ms", flush=True)
    print(f"Packet loss: {args.loss:g}%", flush=True)

    net = None
    server = None
    original_algorithm = None

    try:
        net = create_network(
            rtt_ms=args.rtt,
            loss_pct=args.loss,
            interactive=False
        )

        h1 = net.get("h1")
        h2 = net.get("h2")

        # Confirm the requested TCP congestion-control algorithm.
        algorithm = h1.cmd(
            "sysctl -n net.ipv4.tcp_congestion_control"
        ).strip()

        original_algorithm = algorithm

        if args.protocol == "tcp" and algorithm != args.congestion:
            result = h1.cmd(
                f"sysctl -w net.ipv4.tcp_congestion_control={args.congestion}"
            )
            print(result, flush=True)

        actual = h1.cmd(
            "sysctl -n net.ipv4.tcp_congestion_control"
        ).strip()

        if args.protocol == "tcp" and actual != args.congestion:
            raise RuntimeError(
                f"Expected TCP {args.congestion}, found {actual}"
            )

        if args.protocol == "quic" and args.congestion != "reno":
            raise ValueError("QUIC currently supports Reno only.")

        print(
            f"\n*** Starting {args.protocol.upper()} server ***",
            flush=True,
        )

        if args.protocol == "tcp":
            server_command = ["python3", "tcp/tcp_server.py"]
            client_command = "python3 tcp/tcp_client.py"
        else:
            python = str(PROJECT_ROOT / ".venv" / "bin" / "python")
            initial_rtt = args.rtt / 1000

            server_command = [
                python, "quic/quic_server.py",
                "--congestion", "reno",
                "--initial-rtt", str(initial_rtt),
            ]
            client_command = (
                f"{python} quic/quic_client.py --congestion reno "
                f"--initial-rtt {initial_rtt}"
            )

        server = h2.popen(
            server_command,
            cwd=str(PROJECT_ROOT)
        )

        time.sleep(1)

        if server.poll() is not None:
            raise RuntimeError("TCP server exited unexpectedly.")

        print(
            f"*** Running {args.protocol.upper()} client ***",
            flush=True,
        )

        output = h1.cmd(client_command)

        print(output, flush=True)

        if "Server acknowledgment: DONE" not in output:
            raise RuntimeError("TCP transfer was not acknowledged.")

        # Extract measurements from the TCP client output.
        def extract(pattern):
            match = re.search(pattern, output)
            if not match:
                raise RuntimeError(f"Missing measurement: {pattern}")
            return float(match.group(1))

        connection_time = extract(
            r"Connection time: ([0-9.]+) seconds"
        )
        transfer_time = extract(
            r"Transfer completion time: ([0-9.]+) seconds"
        )
        throughput = extract(
            r"Throughput: ([0-9.]+) Mbps"
        )

        # Preserve existing results and append one successful trial.
        results_path = PROJECT_ROOT / "results" / "results.csv"

        initial_rtt_ms = args.rtt if args.protocol == "quic" else ""
        quic_max_data = 8 * 1024 * 1024 if args.protocol == "quic" else ""
        quic_max_stream_data = 8 * 1024 * 1024 if args.protocol == "quic" else ""

        fields = [
            "protocol",
            "congestion_control",
            "rtt_ms",
            "loss_pct",
            "initial_rtt_ms",
            "quic_max_data_bytes",
            "quic_max_stream_data_bytes",
            "trial",
            "connection_time_s",
            "transfer_time_s",
            "throughput_mbps",
        ]

        if results_path.exists() and results_path.stat().st_size:
            with results_path.open(newline="") as file:
                existing_fields = csv.reader(file).__next__()
            if existing_fields != fields:
                raise RuntimeError(
                    f"Existing CSV columns differ: {existing_fields}"
                )

        results_path.parent.mkdir(parents=True, exist_ok=True)

        write_header = (
            not results_path.exists()
            or results_path.stat().st_size == 0
        )

        # Determine the next trial number for this configuration.
        previous_trials = []

        if results_path.exists() and results_path.stat().st_size:
            with results_path.open(newline="") as existing_file:
                reader = csv.DictReader(existing_file)

                for row in reader:
                    if (
                        row["protocol"] == args.protocol.upper()
                        and row["congestion_control"] == args.congestion
                        and float(row["rtt_ms"]) == args.rtt
                        and float(row["loss_pct"]) == args.loss
                        and row["initial_rtt_ms"] == str(initial_rtt_ms)
                        and row["quic_max_data_bytes"] == str(quic_max_data)
                        and row["quic_max_stream_data_bytes"] == str(quic_max_stream_data)
                    ):
                        previous_trials.append(int(row["trial"]))

        trial_number = max(
            len(previous_trials),
            max(previous_trials, default=0)
        ) + 1

        with results_path.open("a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fields)

            if write_header:
                writer.writeheader()

            writer.writerow({
                "protocol": args.protocol.upper(),
                "congestion_control": args.congestion,
                "rtt_ms": args.rtt,
                "loss_pct": args.loss,
                "initial_rtt_ms": initial_rtt_ms,
                "quic_max_data_bytes": quic_max_data,
                "quic_max_stream_data_bytes": quic_max_stream_data,
                "trial": trial_number,
                "connection_time_s": connection_time,
                "transfer_time_s": transfer_time,
                "throughput_mbps": throughput,
            })

        print(f"SUCCESS: Results saved to {results_path}")
        print(
            f"SUCCESS: Automated {args.protocol.upper()} "
            f"{args.congestion.upper()} trial completed."
        )

    finally:
        if original_algorithm is not None:
            from subprocess import run
            run(
                [
                    "sysctl", "-w",
                    f"net.ipv4.tcp_congestion_control={original_algorithm}",
                ],
                check=True,
            )
            print(
                f"SUCCESS: Restored TCP {original_algorithm.upper()}.",
                flush=True,
            )

        if server is not None and server.poll() is None:
            server.terminate()
            try:
                server.wait(timeout=5)
            except Exception:
                server.kill()
                server.wait()

        if net is not None:
            net.stop()
            print("SUCCESS: Mininet stopped cleanly.", flush=True)


if __name__ == "__main__":
    main()
