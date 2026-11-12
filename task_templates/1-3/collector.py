"""
IoT Data Collector Daemon
Processes streaming sensor events and aggregates metrics.
"""
import time
from typing import Dict, Any, List

# Global event listeners registry
_listeners: List[Any] = []
_audit_trail: List[Dict[str, Any]] = []

class MetricCollector:
    def __init__(self, device_id: str):
        self.device_id = device_id
        self.total_count = 0
        self.total_val = 0.0

    def process_event(self, event: Dict[str, Any]) -> Dict[str, Any]:
        val = float(event.get("value", 0.0))
        self.total_count += 1
        self.total_val += val

        return {
            "device_id": self.device_id,
            "count": self.total_count,
            "avg": self.total_val / self.total_count
        }

def run_batch(events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    collector = MetricCollector("gateway-alpha")
    results = []
    for ev in events:
        res = collector.process_event(ev)
        results.append(res)
    return results
