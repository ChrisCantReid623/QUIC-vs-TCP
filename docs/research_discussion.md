# TCP vs QUIC — Research Discussion

## Purpose

Interpret the experimental findings while distinguishing
measured observations from possible explanations.

## 1. Impact of Network Latency

### Observed Results

At 0% configured packet loss, mean throughput declined
consistently as target RTT increased from 10 ms to 1000 ms.

- TCP CUBIC: 89.279 to 8.122 Mbps (90.9% reduction)
- TCP Reno: 89.565 to 8.084 Mbps (91.0% reduction)
- QUIC Reno: 86.986 to 6.242 Mbps (92.8% reduction)

All three configurations showed substantial sensitivity to
increasing latency in the tested network.

### Interpretation

Transport protocols rely on acknowledgments and feedback
to regulate the amount of data transmitted.

Longer RTTs can delay this feedback and slow congestion-window
growth, particularly during transfers of limited duration.

This behavior is a plausible explanation for the observed
throughput decline, but congestion-window evolution was not
directly measured in this experiment.

The results therefore establish an observed relationship
between configured RTT and throughput, not the precise
internal mechanism responsible for every measurement.

### Research Implication

High-latency paths can substantially reduce transfer
performance even without configured packet loss.

These findings apply to the specific implementations,
10 MiB payload, and controlled Mininet topology tested here.

## 2. Impact of Packet Loss

### Observed Results

At 100 ms target RTT, increasing configured packet loss
from 0% to 3% corresponded to substantial reductions
in mean throughput.

Measured mean throughput at 0%, 1%, and 3% loss:

- TCP CUBIC: 53.904, 2.313, and 0.915 Mbps
- TCP Reno: 53.924, 2.095, and 0.890 Mbps
- QUIC Reno: 49.852, 1.172, and 0.599 Mbps

All three configurations experienced severe degradation
under the tested packet-loss conditions.

### Interpretation

Packet loss can trigger congestion-control responses,
retransmission, and additional recovery delays.

These mechanisms provide plausible explanations for
the observed throughput reductions.

However, packet retransmissions, congestion-window
changes, and recovery events were not directly
instrumented in the experiment.

The measurements therefore demonstrate throughput
sensitivity to configured packet loss without identifying
the precise cause of each individual transfer delay.

### Research Implication

Even relatively modest configured packet-loss levels
can substantially affect performance in this controlled
network environment.

The results should not be generalized to all network
conditions, protocol implementations, or traffic patterns.

## 3. TCP CUBIC vs TCP Reno

### Observed Results

At 0% configured packet loss, TCP CUBIC and TCP Reno
achieved similar mean throughput.

Examples:

- 100 ms RTT: CUBIC 53.904 Mbps; Reno 53.924 Mbps
- 1000 ms RTT: CUBIC 8.122 Mbps; Reno 8.084 Mbps

At 1000 ms RTT with configured packet loss, CUBIC
achieved higher mean throughput:

- 1% loss: CUBIC 0.793 Mbps; Reno 0.208 Mbps
- 3% loss: CUBIC 0.266 Mbps; Reno 0.098 Mbps

These differences were not uniform across every
tested RTT and packet-loss combination.

### Interpretation

TCP Reno uses an acknowledgment-driven congestion-window
increase strategy, while TCP CUBIC uses a cubic window
growth function designed to improve performance on
high-bandwidth, high-delay paths.

Their different congestion-control strategies could
contribute to the observed performance differences.

However, congestion-window trajectories and packet
recovery events were not directly recorded.

The experiment therefore cannot establish that a
particular internal congestion-control mechanism
caused the measured throughput differences.

### Research Implication

TCP CUBIC showed a throughput advantage over TCP Reno
in selected high-latency, lossy configurations.

This is consistent with CUBIC's design objectives,
but the limited repetitions and controlled topology
do not establish universal or statistically
significant superiority.

## 4. TCP vs QUIC Reno

### Observed Results

TCP Reno achieved higher mean throughput than QUIC Reno
in several representative configurations.

At 0% configured packet loss:

- 10 ms RTT: TCP Reno 89.565 Mbps; QUIC Reno 86.986 Mbps
- 100 ms RTT: TCP Reno 53.924 Mbps; QUIC Reno 49.852 Mbps
- 1000 ms RTT: TCP Reno 8.084 Mbps; QUIC Reno 6.242 Mbps

At 100 ms RTT and 3% configured packet loss:

- TCP Reno: 0.890 Mbps
- QUIC Reno: 0.599 Mbps

These results describe the tested implementations and
experimental conditions, not every possible TCP or
QUIC deployment.

### Interpretation

TCP and QUIC differ in transport implementation,
connection establishment, and loss-recovery behavior.

However, the collected measurements do not isolate
which implementation differences explain the
observed throughput gap.

The QUIC implementation used an initial RTT estimate
configured to match the emulated network RTT.

TCP connection-establishment timing measured its
transport handshake, while QUIC timing included
its integrated TLS handshake.

Consequently, the recorded connection times are
not equivalent secure-connection establishment
measurements and should not be interpreted as a
direct comparison of handshake efficiency.

### Research Implication

TCP Reno achieved higher measured throughput than
QUIC Reno in the selected comparisons.

The findings do not establish that TCP is universally
faster than QUIC.

Further experiments using additional implementations,
payload sizes, and controlled handshake measurements
would help determine how broadly these observations
apply.

## 5. Throughput Variability

### Observed Results

Some TCP configurations exhibited substantial differences
between individual trial throughput measurements.

At 50 ms RTT and 1% configured packet loss:

- TCP CUBIC: mean 14.396 Mbps; median 4.273 Mbps
- TCP Reno: mean 25.707 Mbps; median 4.641 Mbps

The corresponding coefficients of variation were:

- TCP CUBIC: 139.7%
- TCP Reno: 121.2%

For TCP CUBIC, individual throughput measurements ranged
from 3.534 to 50.047 Mbps.

For TCP Reno, measurements ranged from 3.392 to
71.374 Mbps.

### Interpretation

A small number of high-throughput trials substantially
increased the arithmetic means relative to the medians.

This indicates that mean throughput alone may not
represent the typical observed trial in these conditions.

The experiment did not collect sufficient packet-level
evidence to determine the precise causes of this
variability.

### Research Implication

Both mean and median throughput should be considered
when comparing protocol configurations.

Sample standard deviation and individual trial results
provide additional context for interpreting unusually
variable conditions.

All five recorded trials were retained for each condition.
No measurements were excluded solely because they
differed substantially from the others.

With only five repetitions per condition, these
descriptive differences should not be interpreted
as statistically significant without further analysis.

## 6. Experimental Limitations

### Network Emulation

The experiment used a controlled 13-node hierarchical
Mininet topology with 100 Mbps configured links.

Latency and packet loss were introduced through
network emulation.

Although these conditions can resemble selected
characteristics of high-latency communication paths,
the topology does not reproduce a complete satellite
network or its dynamic behavior.

### Sample Size and Statistical Confidence

Each protocol, RTT, and packet-loss configuration
was tested five times.

This provides descriptive measurements but limits
the precision of estimated performance differences.

No formal statistical significance testing was
performed.

The observed differences therefore should not
be interpreted as statistically established
protocol superiority.

### Implementation and Configuration

The experiment compared specific TCP and QUIC
implementations and congestion-control settings.

QUIC's initial RTT estimate was configured to
match the emulated network RTT.

This tuning may influence QUIC's behavior and
limits the generality of comparisons with TCP.

Only a 10 MiB payload and the selected network
configurations were evaluated.

### Connection Timing Comparability

TCP connection timing measured establishment
of the transport connection without TLS.

QUIC connection timing included its integrated
TLS handshake.

These measurements do not represent equivalent
secure-connection establishment procedures.

Consequently, connection-time differences cannot
be interpreted as a direct comparison of
equivalent handshake operations.

### Missing Internal Protocol Measurements

The experiment recorded throughput, transfer
completion time, and connection establishment time.

It did not directly instrument congestion-window
evolution, packet retransmissions, or detailed
loss-recovery events.

Explanations involving these mechanisms remain
plausible interpretations rather than directly
verified causes.

### Scope of Conclusions

The findings describe performance within the
specific emulated topology, software environment,
payload size, and tested parameter combinations.

They should not be generalized to all real-world
networks, satellite systems, or transport-protocol
implementations without additional evidence.

## 7. Implications and Future Work

### Practical Implications

The results demonstrate that configured network
latency and packet loss can substantially reduce
throughput for TCP CUBIC, TCP Reno, and QUIC Reno.

The observed performance differences also show
why transport-protocol comparisons should consider
the specific network conditions and implementations.

No single configuration should be declared
universally superior from these measurements.

### Future Experimental Improvements

Future experiments could extend this work by:

- Increasing the number of repetitions per condition.
- Evaluating additional transfer sizes and traffic patterns.
- Testing other QUIC and TCP implementations.
- Comparing congestion-control algorithms under
  more closely matched configuration assumptions.
- Recording packet traces, retransmissions, and
  congestion-window behavior.
- Introducing variable latency, jitter, and
  dynamically changing packet loss.
- Comparing equivalent secure-connection
  establishment procedures.
- Applying statistical tests and confidence intervals
  to assess the reliability of observed differences.

These additions would help distinguish measured
performance differences from their underlying causes.

### Overall Conclusion

Within the controlled 13-node Mininet topology,
all three tested configurations experienced
substantial throughput degradation as configured
RTT and packet loss increased.

TCP generally achieved higher measured throughput
than QUIC Reno in the tested conditions, while
TCP CUBIC showed advantages over TCP Reno in
selected high-latency, lossy configurations.

These findings are descriptive rather than
proof of statistically significant or universal
protocol superiority.

The completed 270-trial dataset provides a
reproducible foundation for further investigation
of transport performance under challenging
network conditions.
