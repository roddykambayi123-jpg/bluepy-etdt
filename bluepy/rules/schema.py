
from __future__ import annotations
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class AttackRef(BaseModel):
    technique: str = Field(..., description="MITRE ATT&CK Technique ID, e.g., T1547.001")
    tactic: str

class WhereClause(BaseModel):
    parent_regex: Optional[str] = None
    child_regex: Optional[str] = None
    cmdline_regex: Optional[str] = None
    path_contains: Optional[str] = None
    hive: Optional[str] = None
    value_regex: Optional[str] = None

class MatchTarget(BaseModel):
    target: str  # e.g., "process.tree" or "persistence.registry"
    where: WhereClause

class Rule(BaseModel):
    id: str
    name: str
    severity: str
    attack: AttackRef
    match: Dict[str, List[MatchTarget]]  # 'any' / 'all'
    explain: str
    next_steps: List[str] = []
