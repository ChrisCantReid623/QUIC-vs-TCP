#!/usr/bin/env python3
"""Batch scheduler for TCP vs QUIC experiments."""

import argparse
import csv
import subprocess
import sys
from pathlib import Path

RTT_VALUES = [10, 50, 100, 250, 500, 1000]
LOSS_VALUES = [0, 1, 3]
PROTOCOLS = [
    ("tcp", "cubic"),
    ("tcp", "reno"),
    ("quic", "reno"),
]
TRIALS_PER_CONFIGURATION = 5

BASE_DIR = Path(__file__).resolve().parent.parent
RESULTS_FILE = BASE_DIR / "results" / "results.csv"


def completed_trials():
    """Read existing trials without modifying results."""
    completed = {}

    if not RESULTS_FILE.exists():
        return completed

    with RESULTS_FILE.open(newline="") as file:
        for row in csv.DictReader(file):
            key = (
                row["protocol"].lower(),
                row["congestion_control"].lower(),
                float(row["rtt_ms"]),
                float(row["loss_pct"]),
            )
            completed.setdefault(key, set()).add(int(row["trial"]))

    return completed



def execute_batch(pending, limit):
    """Execute pending trials and verify each CSV append."""
    runner = BASE_DIR / "experiments" / "run_experiments.py"
    selected = pending[:limit]

    for index, (protocol, congestion, rtt, loss, trial) in enumerate(
        selected, start=1
    ):
        print(
            f"\n=== Batch {index}/{len(selected)}: "
            f"{protocol.upper()} {congestion.upper()}, "
            f"RTT={rtt}, loss={loss}%, trial={trial} ===",
            flush=True,
        )

        before = completed_trials()
        key = (protocol, congestion, float(rtt), float(loss))

        if trial in before.get(key, set()):
            raise RuntimeError("Trial already exists; stopping.")

        with RESULTS_FILE.open(newline="") as file:
            count_before = sum(1 for _ in csv.DictReader(file))

        command = [
            sys.executable,
            "-u",
            str(runner),
            "--protocol", protocol,
            "--congestion", congestion,
            "--rtt", str(rtt),
            "--loss", str(loss),
        ]

        subprocess.run(command, cwd=BASE_DIR, check=True)

        with RESULTS_FILE.open(newline="") as file:
            count_after = sum(1 for _ in csv.DictReader(file))

        after = completed_trials()

        if count_after != count_before + 1:
            raise RuntimeError(
                "Unexpected CSV row count after experiment."
            )

        if trial not in after.get(key, set()):
            raise RuntimeError(
                "Expected trial was not recorded."
            )

        print("SUCCESS: Trial recorded and verified.", flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Execute experiments instead of previewing.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=1,
        help="Maximum experiments to execute (default: 1).",
    )
    args = parser.parse_args()

    if args.limit < 1:
        parser.error("--limit must be at least 1")

    completed = completed_trials()
    pending = []
    total = 0

    print("=== TCP vs QUIC Batch Schedule ===")

    for rtt in RTT_VALUES:
        for loss in LOSS_VALUES:
            for protocol, congestion in PROTOCOLS:
                key = (protocol, congestion, float(rtt), float(loss))
                existing = completed.get(key, set())

                for trial in range(1, TRIALS_PER_CONFIGURATION + 1):
                    total += 1

                    if trial in existing:
                        continue

                    pending.append(
                        (protocol, congestion, rtt, loss, trial)
                    )

                    if not args.execute:
                        print(
                            f"PENDING | {protocol.upper():4} "
                            f"{congestion.upper():5} | "
                            f"RTT={rtt:4} ms | "
                            f"Loss={loss}% | Trial={trial}"
                        )

    print()
    print(f"Total planned trials: {total}")
    print(f"Completed trials: {total - len(pending)}")
    print(f"Remaining trials: {len(pending)}")

    if not args.execute:
        print("PREVIEW ONLY: No experiments were executed.")
        return

    print(f"EXECUTION ENABLED: Maximum {args.limit} trial(s).")
    execute_batch(pending, args.limit)


if __name__ == "__main__":
    main()
