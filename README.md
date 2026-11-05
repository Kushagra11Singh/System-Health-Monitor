# System Health Monitor

A lightweight Python utility that collects host resource metrics and exposes current and recent CPU/RAM information through a small Flask API.

## Overview

The project uses `psutil` to collect:

- CPU utilisation
- RAM utilisation
- Disk utilisation
- A snapshot of the five highest-CPU processes

Each collection is timestamped and appended to a local JSON Lines file (`metrics.log`). The monitor prints a sustained-CPU warning when CPU utilisation remains above 85% for three consecutive collection cycles. A Flask API provides a live sample and a summary of the collected CPU and RAM data from the previous 24 hours.

> **Scope note:** This is a host-resource monitoring project. It is not a SIEM, endpoint-detection product, vulnerability scanner or security-monitoring platform. The CPU threshold is a simple demonstration rule, not a production alerting policy.

## Architecture

1. `monitor.py` collects machine metrics with `psutil`.
2. Each sample is appended to `metrics.log` as one JSON object per line.
3. `api.py` exposes the live sample and reads recent samples for the summary endpoint.
4. `tests/test_monitor.py` checks the structure of a collected sample.

## Requirements

- Python 3.11 or later
- Dependencies listed in `requirements.txt`

## Run locally

### 1. Clone the repository

Clone or download the repository from your GitHub account, then open the project folder:

```bash
cd System-Health-Monitor
```

### 2. Create and activate a virtual environment

**Windows PowerShell**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Start the metrics collector

Open a terminal in the project folder and run:

```bash
python monitor.py
```

The collector writes a new timestamped record to `metrics.log` every 30 seconds. Keep this process running to accumulate samples for the 24-hour summary.

### 5. Start the API

Open a second terminal, activate the same virtual environment, and run:

```bash
python api.py
```

The API listens on `http://127.0.0.1:5000`.

## API endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/metrics/live` | Collects and returns a live CPU, RAM, disk and top-process sample. |
| GET | `/metrics/summary` | Returns the number of samples and average CPU/RAM utilisation from the last 24 hours. Returns `{"error":"no data"}` when no recent samples exist. |

Example requests:

```bash
curl http://127.0.0.1:5000/metrics/live
curl http://127.0.0.1:5000/metrics/summary
```

## Run with Docker

The Docker image starts the Flask API. Start the collector as a second process inside the same container so it writes to the file read by the API.

```bash
docker build -t system-health-monitor .
docker run -d --name system-health-monitor -p 5000:5000 system-health-monitor
docker exec -d system-health-monitor python monitor.py
```

Then open `http://127.0.0.1:5000/metrics/live` or `http://127.0.0.1:5000/metrics/summary`.

To stop and remove the container:

```bash
docker stop system-health-monitor
docker rm system-health-monitor
```

## Run tests

```bash
python -m pytest tests/ -v
```

The included smoke test checks that `collect()` returns CPU, RAM and top-process fields and that no more than five process records are returned.

## Repository structure

```text
System-Health-Monitor/
├── .github/
│   └── workflows/
│       └── ci.yml
├── tests/
│   └── test_monitor.py
├── .gitignore
├── README.md
├── api.py
├── monitor.py
├── Dockerfile
└── requirements.txt
```

`metrics.log` is generated at runtime and is not included in the source repository.

## Limitations and future improvements

- Metrics are stored locally in a simple append-only file; there is no database, retention policy or log rotation.
- The summary endpoint reports average CPU and RAM only; it does not calculate historical disk or per-process trends.
- The sustained-CPU warning is printed to the collector terminal; it is not sent to email, chat or an alert-management platform.
- The API has no authentication, authorisation, rate limiting or production deployment hardening.
- When run in Docker, `psutil` reports the environment visible to the container, not necessarily all host-machine processes or resources.
- The project is intended for learning and demonstration, not production infrastructure monitoring.

## Learning outcomes

This project demonstrates a basic workflow for collecting system metrics, writing structured JSON Lines records, exposing data through HTTP endpoints, running a small pytest check and packaging a Python application with Docker and GitHub Actions.

## Licence

Add the licence you intend to use for this repository. Do not claim a licence unless a corresponding licence file is present.

### Recommended `.gitignore`

The repository's ignore rules should exclude local environments, caches and generated metrics. Add or confirm these entries in `.gitignore`:

```gitignore
.venv/
venv/
__pycache__/
.pytest_cache/
*.py[cod]
*.log
```

Do not commit a local virtual environment or generated runtime logs.
