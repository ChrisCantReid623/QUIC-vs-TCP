# QUIC vs. TCP Under Network Latency and Packet Loss

CNT 6707 - Advanced Computer Networks  
University of Central Florida  
Fall 2026

## Overview

This project experimentally compares the performance of QUIC and TCP under controlled network conditions. A simulated network environment will be used to introduce varying amounts of latency and packet loss while measuring the resulting performance of each protocol.

## Research Question

How does QUIC compare with TCP as network latency and packet loss increase?

## Experimental Variables

### Protocols
- TCP
- QUIC

### Network Latency
- 10 ms
- 50 ms
- 100 ms

### Packet Loss
- 0%
- 1%
- 3%

### Trials
Each experimental condition will initially be repeated five times.

This produces:

2 protocols x 3 latency levels x 3 packet-loss levels x 5 trials = 90 experimental runs.

## Primary Metrics

- Throughput
- Transfer completion time

## Supporting Metrics

- RTT / latency
- Connection establishment time
- Packet loss
- Retransmission / recovery behavior

## Project Structure

    topology/       Mininet network topology
    tcp/            TCP client and server
    quic/           QUIC client and server
    experiments/    Experiment automation
    results/        Experimental results
    analysis/       Data analysis and visualization
    docs/           Experimental design and progress reports

## Experimental Workflow

1. Create the Mininet client-server topology.
2. Verify basic host connectivity.
3. Establish a baseline TCP transfer.
4. Establish a baseline QUIC transfer.
5. Introduce controlled latency and packet loss.
6. Automate repeated experimental trials.
7. Store measurements in structured CSV files.
8. Analyze and visualize the results.

## Current Status

Repository initialized and experimental environment under development.

## Tools

- Ubuntu 22.04
- Mininet
- Python
- TCP sockets
- QUIC
- Wireshark / tcpdump
- Git / GitHub
