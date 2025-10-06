
# BluePy: Endpoint Threat Detection & Triage (ETDT)

A lightweight, cross‑platform Python toolkit that collects endpoint telemetry,
applies a YAML rules engine mapped to MITRE ATT&CK, and generates HTML/JSON triage reports.

## Quick start
```bash
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e .
bluepy scan --all --report html
```

## Demo
```bash
bluepy scan --demo --report html
```
This triggers safe, benign findings so you can screenshot the HTML report for your portfolio.

## Features (MVP)
- Process, network, and persistence snapshots (read‑only)
- YAML rules (severity + ATT&CK mapping)
- HTML & JSON reports
- Clean CLI, unit tests, CI

> **Ethics**: No malware here. Demo scenarios are benign and self‑contained.

MIT License.
