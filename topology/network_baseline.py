#!/usr/bin/env python3

"""
CNT 6707 - Advanced Computer Networks
TCP vs. QUIC Network Simulation

Topology:
    h1 (Client) ---- s1 (OVS Bridge) ---- h2 (Server)

Configurable RTT and packet loss using Mininet TCLink.
"""

import argparse

from mininet.net import Mininet
from mininet.node import OVSBridge
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel, info


def create_network(rtt_ms=0.0, loss_pct=0.0):

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
    h1 = net.addHost("h1", ip="10.0.0.1/24")
    h2 = net.addHost("h2", ip="10.0.0.2/24")

    info("*** Adding switch\n")
    s1 = net.addSwitch("s1")

    # Configure one impaired link.
    # Each direction contributes half of the target RTT.

    one_way_delay = rtt_ms / 2.0

    info("*** Creating links\n")

    net.addLink(
        h1,
        s1,
        cls=TCLink,
        bw=100,
        delay=f"{one_way_delay}ms",
        loss=loss_pct
    )

    net.addLink(
        h2,
        s1,
        cls=TCLink
    )

    info("*** Starting network\n")
    net.start()

    info("\n*** Network configuration\n")
    info("Client: 10.0.0.1\n")
    info("Server: 10.0.0.2\n")
    info(f"Target RTT: {rtt_ms} ms\n")
    info(f"Configured loss per direction: {loss_pct}%\n")

    info("\n*** Testing connectivity\n")
    net.pingAll()

    info("\n*** Starting Mininet CLI\n")
    info("Try: h1 ping -c 10 10.0.0.2\n")
    info("Type 'exit' to stop the simulation.\n\n")

    try:
        CLI(net)
    finally:
        info("*** Stopping network\n")
        net.stop()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="TCP vs. QUIC Mininet Simulation"
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
