# BluePy: Endpoint Threat Detection & Triage (ETDT) 🛡️

A lightweight, cross-platform Python toolkit that collects endpoint telemetry, applies a YAML rules engine mapped to MITRE ATT&CK, and generates HTML/JSON triage reports.

> **Note for macOS users:**  
> Network connection collection (`--all`) may require `sudo` or granting your Terminal “Full Disk Access”.

---

## 🚀 Quick Start

```bash
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e .
sudo bluepy scan --all --report html
```

---

## 🎬 Demo

```bash
bluepy scan --demo --report html
```

This triggers safe, benign findings so you can screenshot the HTML report for your portfolio.

---

## ✨ Features (MVP)

- Process, network, and persistence snapshots (read-only)  
- YAML rules (severity + ATT&CK mapping)  
- HTML & JSON reports with Dark/Light mode support  
- Clean CLI, unit tests, CI  

---

## 📊 Example Report

<img width="1034" height="884" alt="BluePy ETDT Report" src="https://github.com/user-attachments/assets/d12d4607-7c2c-43eb-b3fe-4c9f80a32e8b" />

---

> **Ethics**: No malware here. Demo scenarios are benign and self-contained.

---

## 📄 License

MIT License.  
Developed by [YourGitHubUsername](https://github.com/roddykambayi123-jpg).
