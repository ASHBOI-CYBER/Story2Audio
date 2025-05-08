# -*- coding: utf-8 -*-
import sys, os
import time
import asyncio
import grpc
from grpc import aio
from statistics import mean, quantiles

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
proto_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "proto"))
sys.path.insert(0, proto_dir)

import story2audio_pb2, story2audio_pb2_grpc

TEXT = "This is a short story for benchmarking purposes."
CONCURRENCY_LEVELS = [1, 5, 10, 20]

async def wait_for_server(channel, timeout=5.0):
    """Wait until the gRPC channel is READY or timeout."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        state = channel.get_state(True)
        if state == grpc.ChannelConnectivity.READY:
            return True
        await asyncio.sleep(0.1)
    return False

async def call_generate(stub):
    req = story2audio_pb2.AudioRequest(
        story_text=TEXT,
        voice="Thomas",
        speed=1.0,
        emotion="neutral"
    )
    # up to 3 retries on UNAVAILABLE
    for attempt in range(3):
        try:
            start = time.perf_counter()
            await stub.Generate(req)
            return time.perf_counter() - start
        except aio.AioRpcError as e:
            if e.code() == grpc.StatusCode.UNAVAILABLE and attempt < 2:
                await asyncio.sleep(0.5)
                continue
            else:
                raise

async def benchmark(concurrency):
    channel = grpc.aio.insecure_channel('localhost:50051')
    ready = await wait_for_server(channel)
    if not ready:
        print("ERROR: gRPC server not reachable on localhost:50051", file=sys.stderr)
        sys.exit(1)

    stub = story2audio_pb2_grpc.Story2AudioStub(channel)
    tasks = [call_generate(stub) for _ in range(concurrency)]
    results = await asyncio.gather(*tasks)
    await channel.close()

    avg = mean(results)
    if len(results) >= 2:
        p95 = quantiles(results, n=100)[94]
    else:
        p95 = avg

    return concurrency, avg, p95

async def main():
    print("Concurrency,Avg Latency,P95 Latency")
    for c in CONCURRENCY_LEVELS:
        c, avg, p95 = await benchmark(c)
        print(f"{c},{avg:.3f},{p95:.3f}")

if __name__ == "__main__":
    asyncio.run(main())