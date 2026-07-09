import json
import re
from collections import Counter
from pathlib import Path

REPORT_PATH = Path("/app/report.json")
LOG_PATH = Path("/app/access.log")


def _expected():
    """Independently recompute total requests, unique IPs, and top path from the raw log."""
    paths, ips, total = Counter(), set(), 0
    for line in LOG_PATH.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        total += 1
        ips.add(line.split()[0])
        m = re.search(r'"(?:GET|POST|PUT|DELETE|HEAD|PATCH) (\S+) ', line)
        if m:
            paths[m.group(1)] += 1
    return total, len(ips), paths.most_common(1)[0][0]


def test_report_is_valid_json():
    """Criterion 1: /app/report.json exists and is a valid JSON object."""
    assert REPORT_PATH.exists(), "no report.json found at /app/report.json"
    report = json.loads(REPORT_PATH.read_text())
    assert isinstance(report, dict)


def test_total_requests():
    """Criterion 1: total_requests matches the number of log lines exactly."""
    report = json.loads(REPORT_PATH.read_text())
    expected_total, _, _ = _expected()
    assert report.get("total_requests") == expected_total


def test_unique_ips():
    """Criterion 2: unique_ips matches the number of distinct client IPs exactly."""
    report = json.loads(REPORT_PATH.read_text())
    _, expected_ips, _ = _expected()
    assert report.get("unique_ips") == expected_ips


def test_top_path():
    """Criterion 3: top_path names the most frequently requested path."""
    report = json.loads(REPORT_PATH.read_text())
    _, _, expected_top = _expected()
    assert report.get("top_path") == expected_top
