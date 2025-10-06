
from __future__ import annotations
import os, yaml, re
from typing import List, Dict, Any
from .schema import Rule, MatchTarget
from ..utils import match_regex, safe_str
from ..mitre import describe

def load_rules(dir_path: str) -> List[Rule]:
    rules: List[Rule] = []
    for fname in os.listdir(dir_path):
        if fname.endswith((".yml", ".yaml")):
            with open(os.path.join(dir_path, fname), "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                rules.append(Rule(**data))
    return rules

def _evaluate_target(target: MatchTarget, telemetry: Dict[str, Any]) -> List[Dict[str, Any]]:
    findings = []
    if target.target == "process.tree":
        for proc in telemetry.get("processes", []):
            parent = safe_str(proc.get("parent_name"))
            child = safe_str(proc.get("name"))
            cmd = safe_str(proc.get("cmdline"))
            ok = True
            w = target.where
            if w.parent_regex and not match_regex(w.parent_regex, parent):
                ok = False
            if w.child_regex and not match_regex(w.child_regex, child):
                ok = False
            if w.cmdline_regex and not match_regex(w.cmdline_regex, cmd):
                ok = False
            if ok:
                findings.append({"evidence": proc})
    elif target.target == "persistence.registry":
        for item in telemetry.get("persistence", []):
            if item.get("type") != "registry":
                continue
            w = target.where
            ok = True
            if w.hive and safe_str(item.get("hive")).upper() != safe_str(w.hive).upper():
                ok = False
            if w.value_regex and not match_regex(w.value_regex, safe_str(item.get("data"))):
                ok = False
            if ok:
                findings.append({"evidence": item})
    elif target.target == "process.exec_path":
        for proc in telemetry.get("processes", []):
            cmd = safe_str(proc.get("cmdline"))
            if target.where.path_contains and target.where.path_contains.lower() in cmd.lower():
                findings.append({"evidence": proc})
    return findings

def run(rules: List[Rule], telemetry: Dict[str, Any]) -> List[Dict[str, Any]]:
    results: List[Dict[str, Any]] = []
    for rule in rules:
        matched_evidence = []
        cond = rule.match
        if "any" in cond:
            for target in cond["any"]:
                matched_evidence += _evaluate_target(target, telemetry)
        elif "all" in cond:
            all_sets = []
            for target in cond["all"]:
                all_sets.append(_evaluate_target(target, telemetry))
            # flatten if all non-empty
            if all(all_sets):
                for s in all_sets:
                    matched_evidence += s
        if matched_evidence:
            results.append({
                "id": rule.id,
                "name": rule.name,
                "severity": rule.severity,
                "attack": {"id": rule.attack.technique, **describe(rule.attack.technique)},
                "explain": rule.explain,
                "next_steps": rule.next_steps,
                "evidence": matched_evidence,
            })
    return results
