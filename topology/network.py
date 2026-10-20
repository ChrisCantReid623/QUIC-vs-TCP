#!/usr/bin/env python3
"""TCP vs. QUIC hierarchical Mininet topology."""

import argparse

from mininet.net import Mininet
from mininet.node import OVSBridge
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel, info


def create_network(rtt_ms=0.0, loss_pct=0.0, interactive=True):

    if rtt_ms < 0:
        raise ValueError("RTT cannot be negative.")

    if not 0 <= loss_pct <= 100:
        raise ValueError("Packet loss must be between 0 and 100.")

    net = Mininet(
        controller=None,
        switch=OVSBridge,
        link=TCLink,
        autoSetMacs=True
    )

    info("*** Adding hosts\n")

    hosts = {}

    for i in range(1, 7):
        hosts[f"h{i}"] = net.addHost(
            f"h{i}",
            ip=f"10.0.0.{i}/24"
        )

    info("*** Adding switches\n")

    switches = {}

    for i in range(1, 8):
        switches[f"s{i}"] = net.addSwitch(f"s{i}")

    info("*** Creating hierarchical links\n")

    # Two core-distribution links lie on the client-server path.
    # Each direction on each link contributes RTT / 4.
    # Packet loss is applied on one link to avoid compounding loss.

    one_way_delay = rtt_ms / 4.0

    net.addLink(
        switches["s1"],
        switches["s2"],
        cls=TCLink,
        bw=100,
        delay=f"{one_way_delay}ms",
        loss=loss_pct
    )

    net.addLink(
        switches["s1"],
        switches["s3"],
        cls=TCLink,
        bw=100,
        delay=f"{one_way_delay}ms"
    )

    # Distribution-to-access links
    for a, b in [
        ("s2", "s4"),
        ("s2", "s5"),
        ("s3", "s6"),
        ("s3", "s7")
    ]:
        net.addLink(switches[a], switches[b])

    # Access-to-host links
    for host, switch in [
        ("h1", "s4"),
        ("h3", "s4"),
        ("h4", "s5"),
        ("h5", "s6"),
        ("h2", "s7"),
        ("h6", "s7")
    ]:
        net.addLink(hosts[host], switches[switch])

    info("*** Starting network\n")
    net.start()

    info("\n*** Network configuration\n")
    info("Topology: 7 switches, 6 hosts (13 nodes)\n")
    info("Client: 10.0.0.1\n")
    info("Server: 10.0.0.2\n")
    info(f"Target RTT: {rtt_ms} ms\n")
    info(f"Configured loss per direction: {loss_pct}%\n")
    info("Core-distribution bandwidth: 100 Mbps\n")

    info("\n*** Testing connectivity\n")
    net.pingAll()

    if interactive:
        info("\n*** Starting Mininet CLI\n")

        try:
            CLI(net)
        finally:
            info("*** Stopping network\n")
            net.stop()
    else:
        return net


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="TCP vs. QUIC Hierarchical Mininet Simulation"
    )

    parser.add_argument(
        "--rtt",
        type=float,
        default=0.0,
        help="Target round-trip time in milliseconds"
    )

    parser.add_argument(
        "--loss",
        type=float,
        default=0.0,
        help="Packet loss percentage per direction"
    )

    args = parser.parse_args()

    setLogLevel("info")

    create_network(
        rtt_ms=args.rtt,
        loss_pct=args.loss
    )
