#!/usr/bin/env python3
"""Descriptive statistics for TCP vs QUIC experiments."""

import csv
import statistics
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "results" / "results.csv"


def main():
    groups = defaultdict(list)

    with CSV_PATH.open(newline="") as f:
        rows = list(csv.DictReader(f))

    for row in rows:
        key = (
            row["protocol"].upper(),
            row["congestion_control"].upper(),
            int(float(row["rtt_ms"])),
            float(row["loss_pct"]),
        )
        groups[key].append(float(row["throughput_mbps"]))

    print(f"Total trials: {len(rows)}")
    print(f"Experimental conditions: {len(groups)}")
    print()
    print(
        f"{'Protocol':<10} {'CC':<8} {'RTT':>6} "
        f"{'Loss':>6} {'N':>4} {'Mean':>10} "
        f"{'Median':>10} {'Std Dev':>10}"
    )
    print("-" * 76)

    for key, values in sorted(groups.items()):
        protocol, cc, rtt, loss = key
        print(
            f"{protocol:<10} {cc:<8} {rtt:>6} "
            f"{loss:>5.0f}% {len(values):>4} "
            f"{statistics.mean(values):>10.3f} "
            f"{statistics.median(values):>10.3f} "
            f"{statistics.stdev(values):>10.3f}"
        )


def analyze_timing():
    groups = defaultdict(lambda: {"connection": [], "transfer": []})

    with CSV_PATH.open(newline="") as f:
        for row in csv.DictReader(f):
            key = (
                row["protocol"].upper(),
                row["congestion_control"].upper(),
                int(float(row["rtt_ms"])),
                float(row["loss_pct"]),
            )
            groups[key]["connection"].append(float(row["connection_time_s"]))
            groups[key]["transfer"].append(float(row["transfer_time_s"]))

    print("\n=== Connection and Transfer Times (seconds) ===")
    print(f"{'Protocol':<10} {'CC':<8} {'RTT':>6} {'Loss':>6} "
          f"{'Conn Mean':>12} {'Transfer Mean':>15}")

    for (protocol, cc, rtt, loss), values in sorted(groups.items()):
        connection = statistics.mean(values["connection"])
        transfer = statistics.mean(values["transfer"])
        print(f"{protocol:<10} {cc:<8} {rtt:>6} {loss:>5.0f}% "
              f"{connection:>12.3f} {transfer:>15.3f}")


if __name__ == "__main__":
    main()
    analyze_timing()
