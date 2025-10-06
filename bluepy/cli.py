from __future__ import annotations
import os
import click
import platform
import socket
import psutil
from datetime import datetime
from .agent import collect_process, collect_network, collect_persistence
from .rules.engine import load_rules, run
from .report.render import render_html


def _fmt_duration(seconds: float) -> str:
    """Convert uptime seconds into a human-readable string."""
    seconds = int(seconds)
    d, r = divmod(seconds, 86400)
    h, r = divmod(r, 3600)
    m, s = divmod(r, 60)
    parts = []
    if d:
        parts.append(f"{d}d")
    if h:
        parts.append(f"{h}h")
    if m:
        parts.append(f"{m}m")
    if not parts:
        parts.append(f"{s}s")
    return " ".join(parts)


@click.group()
def cli():
    """BluePy ETDT command-line interface."""
    pass


@cli.command(help="Run a snapshot scan and produce a report")
@click.option("--all", "scan_all", is_flag=True, help="Collect processes, network and persistence")
@click.option("--report", "report_fmt", type=click.Choice(["html", "json"]), default="html")
@click.option("--demo", is_flag=True, help="Trigger benign demo findings")
def scan(scan_all: bool, report_fmt: str, demo: bool):
    # --- Collect telemetry ---
    telemetry = {"processes": [], "network": [], "persistence": []}

    click.echo("[*] Collecting processes...")
    telemetry["processes"] = collect_process.collect()

    if scan_all:
        click.echo("[*] Collecting network connections...")
        telemetry["network"] = collect_network.collect()

        click.echo("[*] Checking persistence locations...")
        telemetry["persistence"] = collect_persistence.collect(demo=demo)

    # --- Load rules and run engine ---
    rules_dir = os.path.join(os.path.dirname(__file__), "rules", "builtin")
    rules = load_rules(rules_dir)
    findings = run(rules, telemetry)

    hi = sum(1 for f in findings if f.get("severity", "").lower() == "high")
    med = sum(1 for f in findings if f.get("severity", "").lower() == "medium")
    low = sum(1 for f in findings if f.get("severity", "").lower() == "low")
    click.echo(f"[!] Findings — high:{hi} medium:{med} low:{low}")

    # --- Build output directory with a permission-safe fallback ---
    ts = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    preferred = os.path.join(os.getcwd(), "reports", ts)
    try:
        out_dir = preferred
        os.makedirs(out_dir, exist_ok=True)
    except PermissionError:
        home_fallback = os.path.join(os.path.expanduser("~"), "bluepy-etdt-reports", ts)
        os.makedirs(home_fallback, exist_ok=True)
        click.echo(f"[!] No permission to write {preferred}. Using {home_fallback} instead.")
        out_dir = home_fallback

    # --- Prepare scan metadata (System Context + counts) ---
    boot_dt = datetime.fromtimestamp(psutil.boot_time())
    uptime = (datetime.now() - boot_dt).total_seconds()

    meta = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "process_count": len(telemetry.get("processes", [])),
        "network_count": len(telemetry.get("network", [])),
        "persistence_count": len(telemetry.get("persistence", [])),
        "hostname": socket.gethostname(),
        "os": f"{platform.system()} {platform.release()} ({platform.machine()})",
        "python": platform.python_version(),
        "boot_time": boot_dt.isoformat(timespec="seconds"),
        "uptime": _fmt_duration(uptime),
    }

    # --- Render output ---
    if report_fmt == "html":
        path = render_html(findings, out_dir, meta=meta)
        click.echo(f"[✓] HTML report: {path}")
    else:
        import json
        out = os.path.join(out_dir, "report.json")
        with open(out, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "meta": meta,
                    "summary": {"high": hi, "medium": med, "low": low},
                    "findings": findings,
                },
                f,
                indent=2,
            )
        click.echo(f"[✓] JSON report: {out}")


def main():
    cli()


if __name__ == "__main__":
    main()