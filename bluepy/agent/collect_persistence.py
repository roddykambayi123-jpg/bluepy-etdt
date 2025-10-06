
from __future__ import annotations
import sys
from typing import List, Dict

def collect(demo: bool=False) -> List[Dict]:
    items: List[Dict] = []
    if demo:
        if sys.platform.startswith("win"):
            items.append({
                "platform": "windows",
                "type": "registry",
                "hive": "HKCU",
                "path": r"Software\Microsoft\Windows\CurrentVersion\Run",
                "value_name": "DemoEntry",
                "data": "powershell.exe -NoProfile -Command echo hello"
            })
        else:
            items.append({
                "platform": "posix",
                "type": "cron",
                "path": "~/.crontab",
                "entry": "@reboot /usr/bin/python3 -c 'print(42)'"
            })
    # NOTE: Real collection would safely read persistence locations read-only.
    return items
