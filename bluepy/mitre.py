
MITRE_TECHNIQUES = {
    "T1547.001": {"name": "Registry Run Keys/Startup Folder", "tactic": "Persistence"},
    "T1204": {"name": "User Execution", "tactic": "Execution"},
    "T1059": {"name": "Command and Scripting Interpreter", "tactic": "Execution"},
}

def describe(tech_id: str) -> dict:
    return MITRE_TECHNIQUES.get(tech_id, {"name": "Unknown", "tactic": "Unknown"})
