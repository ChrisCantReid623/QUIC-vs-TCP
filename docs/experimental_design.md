# Experimental Design

## Research Question

How does QUIC compare with TCP as network latency and packet loss increase?

## Hypotheses

H1: Increasing network latency will negatively affect the performance of both TCP and QUIC.

H2: Increasing packet loss will negatively affect both protocols, but the magnitude of performance degradation may differ.

H3: QUIC and TCP will exhibit different connection-establishment and transfer-completion behavior as network conditions deteriorate.

## Network Model

Experiments were conducted using a 13-node hierarchical office
network implemented in Mininet.

The topology consists of seven switches and six hosts:

- Core: s1
- Distribution: s2, s3
- Access: s4, s5, s6, s7
- Hosts: h1, h2, h3, h4, h5, h6

The experimental client runs on h1 (10.0.0.1), and the server
runs on h2 (10.0.0.2).

The traffic path is:

    h1 -- s4 -- s2 -- s1 -- s3 -- s7 -- h2

Each link has a configured bandwidth of 100 Mbps.

Network delay was introduced on the two core-distribution links,
s1-s2 and s1-s3, with each direction assigned one-quarter of
the target round-trip time.

Packet loss was configured on the s1-s2 link in both directions.
The second core-distribution link was not assigned additional
packet loss.

The network model represents controlled terrestrial and
high-latency conditions rather than a complete satellite
network simulation.

## Independent Variables

Protocol and congestion-control configuration:
- TCP CUBIC
- TCP Reno
- QUIC Reno

Target round-trip time (RTT):
- 10 ms
- 50 ms
- 100 ms
- 250 ms
- 500 ms
- 1000 ms

Configured packet loss:
- 0%
- 1%
- 3%

## Dependent Variables

Primary:
- Throughput
- Transfer completion time

Supporting:
- Connection establishment time

Target RTT and configured packet loss are independent variables,
not measured performance outcomes.

Retransmission and recovery behavior were not directly instrumented
in the collected experimental dataset.

## Experimental Matrix

The completed experiment contains:

- 3 protocol/congestion-control configurations
- 6 target RTT values
- 3 configured packet-loss levels
- 5 trials per condition

Total completed runs:

    3 x 6 x 3 x 5 = 270

All 270 trial records are stored in `results/results.csv`.

## Experimental Controls

The following parameters were held constant across trials:

- Network: 13-node hierarchical Mininet topology
- Client: h1 (10.0.0.1)
- Server: h2 (10.0.0.2)
- Transfer payload: 10 MiB
- Configured link bandwidth: 100 Mbps
- Software environment: Ubuntu 22.04 and Python
- Trials per condition: five

Throughput was calculated as payload bits divided by measured
transfer completion time. Transfer completion includes receipt
of the server's completion acknowledgment.

QUIC's initial RTT estimate was configured to match the target
emulated RTT. This tuning should be considered when interpreting
comparisons with TCP.

Only protocol/congestion-control configuration, target RTT,
and configured packet loss varied across experimental conditions.

## Experimental Workflow and Status

The following phases have been completed:

1. Configure the Ubuntu environment and hierarchical Mininet topology.
2. Implement TCP and QUIC client-server transfers.
3. Validate baseline connectivity and performance measurements.
4. Execute the full 270-trial experimental matrix.
5. Calculate descriptive statistics, including mean, median,
   and sample standard deviation.
6. Generate throughput and connection-establishment figures
   for all three packet-loss configurations.

The experimental dataset and analysis scripts are preserved
in the project repository.

Remaining project deliverables:

- Interpret the experimental findings and limitations.
- Prepare the final research report.
- Prepare the final presentation.

## Connection Establishment Measurement

Connection establishment time is measured using Python's
`time.perf_counter()` in both client implementations.

- **TCP:** Timing begins immediately before `socket.connect()` and
  ends when the TCP three-way handshake completes.
- **QUIC:** Timing begins immediately before entering aioquic's
  `connect()` context and ends when the context yields a connected
  protocol. The default `wait_connected=True` waits for QUIC
  connection establishment, including its integrated TLS handshake.
- **Transfer timing:** Both implementations begin measuring transfer
  completion after connection establishment and stop after receiving
  the server's completion acknowledgment.

**Comparability limitation:** TCP connection establishment does not
include TLS, whereas QUIC connection establishment includes its
integrated TLS handshake. Consequently, these measurements represent
implementation-specific connection milestones rather than equivalent
secure-connection setup costs. They should not be interpreted as a
direct comparison of secure TCP versus secure QUIC establishment.

The QUIC client also includes local asynchronous connection setup
within its measured interval.
