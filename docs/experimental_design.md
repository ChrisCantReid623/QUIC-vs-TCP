# Experimental Design

## Research Question

How does QUIC compare with TCP as network latency and packet loss increase?

## Hypotheses

H1: Increasing network latency will negatively affect the performance of both TCP and QUIC.

H2: Increasing packet loss will negatively affect both protocols, but the magnitude of performance degradation may differ.

H3: QUIC and TCP will exhibit different connection-establishment and transfer-completion behavior as network conditions deteriorate.

## Network Model

The initial experiment will use a simple client-server topology in Mininet.

    h1 (Client) -------- Network -------- h2 (Server)

The link between the hosts will be configured with controlled delay and packet-loss parameters.

## Independent Variables

Protocol:
- TCP
- QUIC

Latency:
- 10 ms
- 50 ms
- 100 ms

Packet Loss:
- 0%
- 1%
- 3%

## Dependent Variables

Primary:
- Throughput
- Transfer completion time

Supporting:
- RTT
- Connection establishment time
- Packet loss
- Retransmission / recovery behavior

## Experimental Matrix

Each combination of protocol, latency, and packet loss will initially be executed five times.

Total runs:

2 x 3 x 3 x 5 = 90

## Experimental Controls

To make comparisons meaningful, experiments should use the same:

- Network topology
- Client and server hosts
- Transfer size
- Link bandwidth
- Software environment
- Measurement procedure

Only the variables intentionally being tested should change between conditions.

## Planned Workflow

Phase 1: Environment and topology setup

Phase 2: TCP and QUIC baseline testing

Phase 3: Controlled latency and packet-loss experiments

Phase 4: Experiment automation and data collection

Phase 5: Statistical analysis and visualization

Phase 6: Final report and presentation
