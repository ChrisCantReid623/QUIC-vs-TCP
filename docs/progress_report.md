# TCP vs QUIC — Project Progress Report

Date: October 21, 2026

## Project Objective

Evaluate TCP and QUIC performance under controlled
network latency and packet-loss conditions using Mininet.

## Network Implementation

Completed a 13-node hierarchical office topology:

- 7 switches
- 6 hosts
- 100 Mbps configured link bandwidth
- Client: h1 (10.0.0.1)
- Server: h2 (10.0.0.2)

## Experimental Configurations

Protocols and congestion control:

- TCP CUBIC
- TCP Reno
- QUIC Reno

Target RTT values:

- 10, 50, 100, 250, 500, and 1000 ms

Packet-loss levels:

- 0%, 1%, and 3%

Five repetitions were completed per condition.

## Experiment Completion

Total planned trials: 270
Completed trials: 270
Completion: 100%

The complete dataset is stored in `results/results.csv`.

## Analysis Completed

- Descriptive statistics: mean, median, sample standard deviation
- Throughput performance visualizations
- Connection-establishment time visualizations
- Review of variability and selected outliers

Analysis scripts are available in `analysis/`.

## Measurement Limitations

TCP connection timing measures its transport handshake,
whereas QUIC connection timing includes its integrated
TLS handshake. These are not equivalent secure-connection
establishment measurements.

QUIC's initial RTT estimate was configured to match
the emulated RTT.

Retransmission and recovery behavior were not directly
instrumented.

The network emulates controlled latency and loss rather
than a complete satellite communication environment.

## Remaining Work

1. Interpret experimental findings and limitations.
2. Prepare the final research report.
3. Prepare the final presentation.

## Project Status

Experimental execution and descriptive analysis are complete.

Research interpretation and final deliverables remain in progress.
