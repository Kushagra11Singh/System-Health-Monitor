import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from monitor import collect  # noqa: E402


def test_collect_keys():
    data = collect()
    assert "cpu_percent" in data
    assert "top_processes" in data
    assert len(data["top_processes"]) <= 5