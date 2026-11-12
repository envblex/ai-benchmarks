import asyncio
from typing import Dict, List, Callable, Any

class AsyncEventBus:
    def __init__(self):
        self._subscribers: Dict[str, List[Callable[[Any], Any]]] = {}

    def subscribe(self, topic: str, handler: Callable[[Any], Any]):
        if topic not in self._subscribers:
            self._subscribers[topic] = []
        self._subscribers[topic].append(handler)

    async def publish(self, topic: str, message: Any):
        handlers = self._subscribers.get(topic, [])
        for h in handlers:
            # Spawn background task without awaiting or tracking completion
            asyncio.create_task(self._safe_call(h, message))

    async def _safe_call(self, handler, message):
        if asyncio.iscoroutinefunction(handler):
            await handler(message)
        else:
            handler(message)
