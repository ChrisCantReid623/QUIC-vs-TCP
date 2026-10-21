# QUIC vs. TCP Under Network Latency and Packet Loss

CNT 6707 - Advanced Computer Networks  
University of Central Florida  
Fall 2026

## Overview

This project experimentally compares TCP and QUIC performance under
controlled network latency and packet-loss conditions.

Experiments were conducted using a 13-node hierarchical office
network implemented in Mininet on Ubuntu 22.04.

The study evaluates three protocol/congestion-control configurations:
TCP CUBIC, TCP Reno, and QUIC Reno.

A total of 270 experimental trials were completed across six RTT
configurations and three packet-loss levels.

The collected measurements include throughput, transfer completion
time, and connection establishment time. Results were analyzed
using descriptive statistics and visualized through performance plots.

For detailed methodology, see `docs/experimental_design.md`.

## Research Question

How does QUIC compare with TCP as network latency and packet loss increase?

## Experimental Variables

### Protocols and Congestion Control

- TCP CUBIC
- TCP Reno
- QUIC Reno

### Network Latency (Target RTT)

- 10 ms
- 50 ms
- 100 ms
- 250 ms
- 500 ms
- 1000 ms

### Packet Loss

- 0%
- 1%
- 3%

### Trials

Each experimental condition was repeated five times.

The completed experimental matrix consists of:

3 configurations x 6 RTT levels x 3 loss levels x 5 trials = 270 runs.

All 270 trial records are stored in `results/results.csv`.

## Primary Metrics

- Throughput
- Transfer completion time

## Supporting Metrics

- Connection establishment time

Target RTT and configured packet loss are independent variables,
not measured performance outcomes.

Retransmission and recovery behavior were not directly instrumented
in the collected experimental dataset.

## Project Structure

    topology/       Mininet network topology
    tcp/            TCP client and server
    quic/           QUIC client and server
    experiments/    Experiment automation
    results/        Experimental results
    analysis/       Data analysis and visualization
    docs/           Experimental design and progress reports

## Experimental Workflow

The following work has been completed:

1. Implement the 13-node hierarchical Mininet topology.
2. Validate connectivity between client h1 and server h2.
3. Implement TCP CUBIC, TCP Reno, and QUIC Reno transfers.
4. Configure controlled RTT and packet-loss conditions.
5. Automate and execute all 270 experimental trials.
6. Preserve the measurements in `results/results.csv`.
7. Calculate mean, median, and sample standard deviation.
8. Generate throughput and connection-establishment plots.

## Current Status

Experimental execution: Complete (270/270 trials).

Statistical analysis and performance visualizations: Complete.

The repository includes:

- `results/results.csv`: Complete experimental dataset.
- `analysis/analyze_results.py`: Descriptive statistical analysis.
- `analysis/plot_results.py`: Throughput visualizations.
- `analysis/plot_connection_time.py`: Connection-time visualizations.
- `docs/experimental_design.md`: Experimental methodology.

Remaining deliverables are interpretation of the results,
the final research report, and the final presentation.

## Tools

- Ubuntu 22.04
- Mininet
- Python
- TCP sockets
- QUIC
- Wireshark / tcpdump
- Git / GitHub
