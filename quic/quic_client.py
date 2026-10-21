#!/usr/bin/env python3
"""QUIC sender for the TCP vs. QUIC Mininet experiment."""

import argparse
import json
import asyncio
import time
from pathlib import Path

from aioquic.asyncio.client import connect
from aioquic.quic.configuration import QuicConfiguration
from aioquic.quic.logger import QuicLogger

PAYLOAD_SIZE = 10 * 1024 * 1024
CHUNK_SIZE = 65536
BASE_DIR = Path(__file__).resolve().parent


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="10.0.0.2")
    parser.add_argument("--port", type=int, default=4433)
    parser.add_argument("--congestion", default="reno")
    parser.add_argument("--initial-rtt", type=float, default=0.25)
    args = parser.parse_args()

    quic_logger = QuicLogger()

    configuration = QuicConfiguration(
        is_client=True,
        alpn_protocols=["tcp-quic-benchmark"],
        congestion_control_algorithm=args.congestion,
        initial_rtt=args.initial_rtt,
        quic_logger=quic_logger,
        max_data=8 * 1024 * 1024,
        max_stream_data=8 * 1024 * 1024,
    )

    configuration.load_verify_locations(
        cafile=str(BASE_DIR / "certs" / "server.crt")
    )

    connection_start = time.perf_counter()

    async with connect(
        args.host,
        args.port,
        configuration=configuration,
    ) as protocol:

        connection_time = time.perf_counter() - connection_start

        reader, writer = await protocol.create_stream()

        payload = b"x" * CHUNK_SIZE
        remaining = PAYLOAD_SIZE

        transfer_start = time.perf_counter()

        while remaining > 0:
            chunk = payload[:min(CHUNK_SIZE, remaining)]
            writer.write(chunk)
            await writer.drain()
            remaining -= len(chunk)

        writer.write_eof()
        await writer.drain()

        acknowledgment = await reader.read(1024)

        transfer_time = time.perf_counter() - transfer_start

        if acknowledgment != b"DONE":
            raise RuntimeError(
                f"Unexpected server acknowledgment: {acknowledgment!r}"
            )

        throughput = (PAYLOAD_SIZE * 8) / transfer_time / 1_000_000

        print("\n--- QUIC Client Results ---")
        print(f"Bytes sent: {PAYLOAD_SIZE}")
        print(f"Server acknowledgment: {acknowledgment.decode()}")
        print(f"Congestion control: {args.congestion}")
        print(f"Connection time: {connection_time:.6f} seconds")
        print(f"Transfer completion time: {transfer_time:.6f} seconds")
        print(f"Throughput: {throughput:.3f} Mbps")

    diagnostics = BASE_DIR.parent / "results" / "diagnostics"
    diagnostics.mkdir(parents=True, exist_ok=True)

    qlog_path = diagnostics / "quic_client_latest.qlog"

    with qlog_path.open("w") as file:
        json.dump(quic_logger.to_dict(), file)

    print(f"QLOG saved to: {qlog_path}")


if __name__ == "__main__":
    asyncio.run(main())
