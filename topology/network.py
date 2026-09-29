#!/usr/bin/env python3

"""
CNT 6707 - Advanced Computer Networks
QUIC vs. TCP Under Network Latency and Packet Loss

Initial Mininet topology:

    h1 (Client) ---- s1 ---- h2 (Server)

This topology provides the baseline network used to verify
connectivity before introducing latency and packet loss.
"""

from mininet.net import Mininet
from mininet.node import OVSController
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel, info


def create_network():
    """Create and start the baseline Mininet topology."""

    net = Mininet(
        controller=OVSController,
        link=TCLink,
        autoSetMacs=True
    )

    info("*** Adding controller\n")
    net.addController("c0")

    info("*** Adding hosts\n")
    h1 = net.addHost("h1", ip="10.0.0.1/24")
    h2 = net.addHost("h2", ip="10.0.0.2/24")

    info("*** Adding switch\n")
    s1 = net.addSwitch("s1")

    info("*** Creating links\n")
    net.addLink(h1, s1)
    net.addLink(h2, s1)

    info("*** Starting network\n")
    net.start()

    info("\n*** Network configuration\n")
    info("h1 (Client): 10.0.0.1\n")
    info("h2 (Server): 10.0.0.2\n")

    info("\n*** Testing connectivity\n")
    net.pingAll()

    info("\n*** Starting Mininet CLI\n")
    info("Try: h1 ping -c 4 10.0.0.2\n")
    info("Type 'exit' to stop the simulation.\n\n")

    CLI(net)

    info("*** Stopping network\n")
    net.stop()


if __name__ == "__main__":
    setLogLevel("info")
    create_network()
