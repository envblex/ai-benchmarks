import tracemalloc
import gc
import pytest
from collector import MetricCollector

def test_memory_growth_under_threshold():
    """Verify that processing 30,000 events does not leak memory (> 2MB)."""
    gc.collect()
    tracemalloc.start()
    snap_before = tracemalloc.take_snapshot()

    collector = MetricCollector("sensor-001")
    # Feed 30,000 telemetry messages
    for i in range(30000):
        collector.process_event({"id": i, "value": 42.5, "extra": "x" * 200})

    gc.collect()
    snap_after = tracemalloc.take_snapshot()
    tracemalloc.stop()

    top_stats = snap_after.compare_to(snap_before, 'lineno')
    total_diff_bytes = sum(stat.size_diff for stat in top_stats)
    total_diff_mb = total_diff_bytes / (1024 * 1024)

    print(f"\n[Leak Test] Memory Growth: {total_diff_mb:.2f} MB")
    # Max allowed leak is 2.0 MB for 30k messages
    assert total_diff_mb < 2.0, f"Memory leak detected! Grew by {total_diff_mb:.2f} MB (limit: 2.0 MB)"

def test_collector_accuracy():
    """Ensure aggregation arithmetic remains accurate."""
    c = MetricCollector("sensor-test")
    c.process_event({"value": 10})
    res = c.process_event({"value": 20})
    assert res["count"] == 2
    assert res["avg"] == 15.0
