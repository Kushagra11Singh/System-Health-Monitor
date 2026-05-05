from monitor import collect

def test_collect_keys():
    data = collect()
    assert "cpu_percent" in data
    assert "top_processes" in data
    assert len(data["top_processes"]) <= 5