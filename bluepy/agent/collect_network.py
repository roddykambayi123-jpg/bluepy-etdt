from __future__ import annotations
import psutil
from typing import List, Dict


def _conn_to_dict(c) -> Dict:
    try:
        laddr = f"{c.laddr.ip}:{c.laddr.port}" if c.laddr else ""
    except Exception:
        laddr = ""
    try:
        raddr = f"{c.raddr.ip}:{c.raddr.port}" if c.raddr else ""
    except Exception:
        raddr = ""
    return {
        "pid": getattr(c, "pid", None),
        "status": getattr(c, "status", ""),
        "laddr": laddr,
        "raddr": raddr,
        "family": str(getattr(c, "family", "")),
        "type": str(getattr(c, "type", "")),
    }


def collect() -> List[Dict]:
    """
    Best-effort network connection snapshot.
    On macOS without Full Disk Access / sudo, psutil.net_connections may raise
    AccessDenied. In that case, we fall back to an empty list rather than aborting
    the scan, so the CLI continues and other collectors/rules still run.
    """
    conns: List[Dict] = []
    try:
        for c in psutil.net_connections(kind="inet"):
            try:
                conns.append(_conn_to_dict(c))
            except Exception:
                # Skip malformed/ephemeral records
                continue
        return conns
    except (psutil.AccessDenied, PermissionError):
        print("[!] Skipping network collection: AccessDenied (try sudo or grant Full Disk Access)")
        return []
    except Exception:
        # Any other platform-specific error: just skip
        return []