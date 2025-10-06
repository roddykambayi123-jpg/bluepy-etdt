
from __future__ import annotations
import psutil
from typing import List, Dict

def collect() -> List[Dict]:
    proc_info = []
    for p in psutil.process_iter(attrs=["pid", "ppid", "name", "cmdline"]):
        info = p.info
        parent_name = None
        try:
            if p.ppid():
                parent_name = psutil.Process(p.ppid()).name()
        except Exception:
            parent_name = None
        proc_info.append({
            "pid": info.get("pid"),
            "ppid": info.get("ppid"),
            "name": info.get("name") or "",
            "cmdline": " ".join(info.get("cmdline") or []),
            "parent_name": parent_name or "",
        })
    return proc_info
