import asyncio
import pytest
from bus import AsyncEventBus

@pytest.mark.asyncio
async def test_concurrent_fanout():
    bus = AsyncEventBus()
    received = []

    async def slow_handler_1(msg):
        await asyncio.sleep(0.005) # simulates I/O
        received.append(("h1", msg))

    async def slow_handler_2(msg):
        await asyncio.sleep(0.008)
        received.append(("h2", msg))

    bus.subscribe("orders", slow_handler_1)
    bus.subscribe("orders", slow_handler_2)

    await bus.publish("orders", {"id": 101})

    # BUG: Flaky sleep-based wait! Often fails under CPU contention
    await asyncio.sleep(0.006)

    assert len(received) == 2, f"Flaky failure! Expected 2 handlers completed, got {len(received)}"
