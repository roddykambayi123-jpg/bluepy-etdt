
from bluepy.rules.engine import load_rules, run
from bluepy.agent import collect_process

def test_rules_load():
    rules = load_rules(__import__("os").path.join(__import__("os").path.dirname(__file__), "..", "bluepy", "rules", "builtin"))
    assert len(rules) >= 1

def test_run_with_dummy_proc():
    telemetry = {
        "processes": [
            {"pid":1,"ppid":0,"name":"cmd.exe","cmdline":"C:/Users/you/Downloads/tool.exe","parent_name":"python.exe"}
        ],
        "persistence":[]
    }
    rules = load_rules(__import__("os").path.join(__import__("os").path.dirname(__file__), "..", "bluepy", "rules", "builtin"))
    findings = run(rules, telemetry)
    assert isinstance(findings, list)
