#!/usr/bin/env python3
"""QUIC receiver for the TCP vs. QUIC Mininet experiment."""

import argparse
import asyncio
from pathlib import Path

from aioquic.asyncio import serve
from aioquic.quic.configuration import QuicConfiguration

PAYLOAD_SIZE = 10 * 1024 * 1024
PORT = 4433
BASE_DIR = Path(__file__).resolve().parent


async def handle_stream(reader, writer):
    received = 0

    while True:
        data = await reader.read(65536)
        if not data:
            break

        received += len(data)

        if received > PAYLOAD_SIZE:
            writer.write(b"ERROR: TOO MUCH DATA")
            writer.write_eof()
            await writer.drain()
            return

        if received == PAYLOAD_SIZE:
            break

    if received == PAYLOAD_SIZE:
        writer.write(b"DONE")
        print(f"QUIC server received {received} bytes", flush=True)
    else:
        writer.write(b"ERROR: INCOMPLETE TRANSFER")
        print(f"Incomplete QUIC transfer: {received} bytes", flush=True)

    writer.write_eof()
    await writer.drain()


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="10.0.0.2")
    parser.add_argument("--port", type=int, default=PORT)
    parser.add_argument("--congestion", default="reno")
    args = parser.parse_args()

    configuration = QuicConfiguration(
        is_client=False,
        alpn_protocols=["tcp-quic-benchmark"],
        congestion_control_algorithm=args.congestion,
    )

    configuration.load_cert_chain(
        str(BASE_DIR / "certs" / "server.crt"),
        str(BASE_DIR / "certs" / "server.key"),
    )

    server = await serve(
        args.host,
        args.port,
        configuration=configuration,
        stream_handler=lambda reader, writer: asyncio.create_task(
            handle_stream(reader, writer)
        ),
    )

    print(
        f"QUIC server listening on {args.host}:{args.port} "
        f"(congestion control: {args.congestion})",
        flush=True,
    )

    try:
        await asyncio.Event().wait()
    finally:
        server.close()


if __name__ == "__main__":
    asyncio.run(main())
