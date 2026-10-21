#!/usr/bin/env python3
"""Plot TCP vs QUIC throughput results."""

import csv
from collections import defaultdict
from pathlib import Path
from statistics import mean, median, stdev

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
import sys
LOSS_PCT = float(sys.argv[1]) if len(sys.argv) > 1 else 0.0
STAT = sys.argv[2].lower() if len(sys.argv) > 2 else "mean"
assert STAT in ("mean", "median"), "Use mean or median."
aggregate = median if STAT == "median" else mean

groups = defaultdict(list)

with (ROOT / "results/results.csv").open(newline="") as f:
    for row in csv.DictReader(f):
        if float(row["loss_pct"]) != LOSS_PCT:
            continue
        key = (
            row["protocol"].upper(),
            row["congestion_control"].upper(),
            int(float(row["rtt_ms"])),
        )
        groups[key].append(float(row["connection_time_s"]))

fig, ax = plt.subplots(figsize=(9, 5.5))

for protocol, cc in [("TCP", "CUBIC"), ("TCP", "RENO"), ("QUIC", "RENO")]:
    points = sorted(
        (rtt, aggregate(values))
        for (p, c, rtt), values in groups.items()
        if (p, c) == (protocol, cc)
    )
    x = [rtt for rtt, value in points]
    y = [value for rtt, value in points]

    if STAT == "mean":
        errors = [
            stdev(groups[(protocol, cc, rtt)])
            for rtt in x
        ]
        lower_errors = [min(value, sd) for value, sd in zip(y, errors)]
        ax.errorbar(
            x, y, yerr=[lower_errors, errors], marker="o",
            capsize=3, label=f"{protocol} {cc}",
        )
    else:
        ax.plot(
            x, y, marker="o", label=f"{protocol} {cc}",
        )

ax.set_xlabel("Round-trip time (ms)")
ax.set_ylabel(f"{STAT.title()} connection time (s)")
title = f"TCP vs QUIC Connection Time at {LOSS_PCT:g}% Packet Loss"
if STAT == "mean":
    title += " (Mean ± 1 SD)"
ax.set_title(title)
ax.set_xticks([10, 50, 100, 250, 500, 1000])
ax.grid(True, alpha=0.3)
ax.legend()
fig.text(
    0.5, 0.01,
    "TCP: transport handshake only | QUIC: TLS-integrated connection",
    ha="center", fontsize=8,
)
fig.tight_layout(rect=[0, 0.04, 1, 1])

output = ROOT / f"results/connection_time_{LOSS_PCT:g}pct_loss_{STAT}_sd.png" if STAT == "mean" else f"results/connection_time_{LOSS_PCT:g}pct_loss_{STAT}.png"
fig.savefig(output, dpi=200)
plt.close(fig)

print(f"SUCCESS: Created {output}")
