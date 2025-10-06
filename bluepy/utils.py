
import re
from typing import Optional

def match_regex(pattern: str, text: str) -> bool:
    try:
        return re.search(pattern, text or "", flags=re.IGNORECASE) is not None
    except re.error:
        return False

def safe_str(x) -> str:
    try:
        return str(x) if x is not None else ""
    except Exception:
        return ""
