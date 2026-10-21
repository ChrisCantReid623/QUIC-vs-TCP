#!/usr/bin/env python3

"""
TCP server for the QUIC vs TCP performance experiment.

Runs on the Mininet server host (h2), receives a fixed-size TCP data
transfer, sends an application-level acknowledgment to the client,
and reports transfer statistics.
"""

import socket
import time


HOST = "0.0.0.0"
PORT = 5001
BUFFER_SIZE = 64 * 1024
PAYLOAD_SIZE = 10 * 1024 * 1024


def main():
    # Create an IPv4 TCP socket.
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:

        # Allow the port to be reused shortly after restarting the server.
        server_socket.setsockopt(
            socket.SOL_SOCKET,
            socket.SO_REUSEADDR,
            1
        )

        # Listen on all interfaces on TCP port 5001.
        server_socket.bind((HOST, PORT))
        server_socket.listen(1)

        print(f"TCP server listening on port {PORT}...")

        # Wait for the client to establish a TCP connection.
        connection, address = server_socket.accept()

        with connection:
            print(f"Connection from {address[0]}:{address[1]}")

            total_bytes = 0
            start_time = time.perf_counter()

            # Receive data until the complete payload has arrived.
            while total_bytes < PAYLOAD_SIZE:
                data = connection.recv(BUFFER_SIZE)

                if not data:
                    break

                total_bytes += len(data)

            end_time = time.perf_counter()

            # Tell the client that the complete payload was received.
            if total_bytes == PAYLOAD_SIZE:
                connection.sendall(b"DONE")

        transfer_time = end_time - start_time

        if transfer_time > 0:
            throughput_mbps = (
                total_bytes * 8 / transfer_time / 1_000_000
            )
        else:
            throughput_mbps = 0.0

        print("\n--- TCP Server Results ---")
        print(f"Bytes received: {total_bytes}")
        print(f"Transfer time: {transfer_time:.6f} seconds")
        print(f"Throughput: {throughput_mbps:.3f} Mbps")


if __name__ == "__main__":
    main()
