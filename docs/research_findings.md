# TCP vs QUIC — Experimental Findings

## Dataset

The completed experiment contains 270 trials across:

- TCP CUBIC, TCP Reno, and QUIC Reno
- Six RTT configurations: 10, 50, 100, 250, 500, 1000 ms
- Three packet-loss configurations: 0%, 1%, 3%
- Five repetitions per condition

All results are preserved in `results/results.csv`.

## Finding 1: RTT and Throughput

At 0% packet loss, mean throughput decreased as RTT increased
for all three protocol configurations.

From 10 ms to 1000 ms RTT:

- TCP CUBIC: 89.279 to 8.122 Mbps
- TCP Reno: 89.565 to 8.084 Mbps
- QUIC Reno: 86.986 to 6.242 Mbps

These observations demonstrate substantial throughput degradation
with increasing emulated latency in this experimental setup.

## Finding 2: Packet Loss and Throughput

At 100 ms RTT, mean throughput decreased as configured packet
loss increased from 0% to 3%:

- TCP CUBIC: 53.904 to 0.915 Mbps
- TCP Reno: 53.924 to 0.890 Mbps
- QUIC Reno: 49.852 to 0.599 Mbps

All three configurations experienced severe throughput reductions.

## Finding 3: Protocol Comparison

TCP generally achieved higher measured throughput than QUIC Reno
under the tested configurations.

TCP CUBIC showed higher mean throughput than TCP Reno at
1000 ms RTT under both 1% and 3% packet loss.

These results are specific to the implementations, parameters,
payload size, and emulated network used in this experiment.

They do not establish universal protocol superiority.

## Finding 4: Trial Variability

Some TCP conditions showed substantial throughput variability.

At 50 ms RTT and 1% packet loss:

- TCP CUBIC: mean 14.396 Mbps, median 4.273 Mbps
- TCP Reno: mean 25.707 Mbps, median 4.641 Mbps

Their coefficients of variation were approximately 139.7%
and 121.2%, respectively.

A small number of high-throughput trials strongly influenced
the means. All five trials were retained for each condition.

Both mean and median should be reported when interpreting
these variable conditions.

## Measurement Validation

All 270 recorded throughput values were checked against:

    throughput_mbps = (10 * 1024 * 1024 * 8)
                      / transfer_time_s / 1,000,000

The maximum absolute difference was 0.000499 Mbps,
consistent with rounding.

## Limitations

- Five repetitions per condition limit statistical confidence.
- QUIC's initial RTT estimate was tuned to the emulated RTT.
- TCP connection timing excludes TLS, while QUIC includes TLS.
- Retransmission and recovery behavior were not directly measured.
- The topology emulates controlled latency and packet loss,
  not a complete satellite network.
- Observed differences should not be treated as proof of
  statistically significant or universal protocol superiority.

## Interpretation Status

These findings are descriptive and based on the completed
experimental dataset. Further discussion will connect the
observations to transport-protocol behavior and related research.
