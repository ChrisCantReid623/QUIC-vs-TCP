#!/usr/bin/env python3

"""
TCP client for the QUIC vs TCP performance experiment.

Runs on the Mininet client host (h1), connects to the TCP server on h2,
sends a fixed-size payload, waits for an application-level acknowledgment,
and reports connection and end-to-end transfer timing.
"""

import socket
import time


SERVER_IP = "10.0.0.2"
PORT = 5001

PAYLOAD_SIZE = 10 * 1024 * 1024
CHUNK_SIZE = 64 * 1024


def main():
    data_chunk = b"x" * CHUNK_SIZE
    bytes_sent = 0

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:

        # Measure TCP connection establishment time.
        connection_start = time.perf_counter()
        client_socket.connect((SERVER_IP, PORT))
        connection_end = time.perf_counter()

        connection_time = connection_end - connection_start

        # Start end-to-end transfer timing.
        transfer_start = time.perf_counter()

        # Send the complete fixed-size payload.
        while bytes_sent < PAYLOAD_SIZE:
            remaining = PAYLOAD_SIZE - bytes_sent
            chunk = data_chunk[:min(CHUNK_SIZE, remaining)]

            client_socket.sendall(chunk)
            bytes_sent += len(chunk)

        # Wait until the server confirms that the complete payload arrived.
        acknowledgment = client_socket.recv(4)

        transfer_end = time.perf_counter()

    transfer_time = transfer_end - transfer_start

    if transfer_time > 0:
        throughput_mbps = (
            bytes_sent * 8 / transfer_time / 1_000_000
        )
    else:
        throughput_mbps = 0.0

    print("\n--- TCP Client Results ---")
    print(f"Bytes sent: {bytes_sent}")
    print(f"Server acknowledgment: {acknowledgment.decode()}")
    print(f"Connection time: {connection_time:.6f} seconds")
    print(f"Transfer completion time: {transfer_time:.6f} seconds")
    print(f"Throughput: {throughput_mbps:.3f} Mbps")


if __name__ == "__main__":
    main()
