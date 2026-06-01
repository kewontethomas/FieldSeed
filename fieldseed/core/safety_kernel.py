from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import json, hashlib

from fieldseed.paths import LOGS, ROOT

RISKY_TERMS = [
    "delete", "format", "wipe", "factory reset", "disable firewall", "turn off antivirus",
    "remove all", "clear logs", "bypass", "force", "overwrite", "registry", "reg delete",
    "diskpart clean", "rd /s", "del /f", "shutdown", "restart service"
]

READ_ONLY_TERMS = [
    "check", "show", "list", "get", "query", "inspect", "collect", "export", "read",
    "ipconfig", "systeminfo", "get-service", "get-eventlog", "get-disk"
]

@dataclass
class SafetyDecision:
    allowed: bool
    risk: str
    confidence: int
    reason: str
    requires_confirmation: bool = False
    requires_backup: bool = False
    read_only: bool = True

    def as_dict(self):
        return {
            "allowed": self.allowed,
            "risk": self.risk,
            "confidence": self.confidence,
            "reason": self.reason,
            "requires_confirmation": self.requires_confirmation,
            "requires_backup": self.requires_backup,
            "read_only": self.read_only,
        }

def classify_action(action_text: str) -> SafetyDecision:
    text = (action_text or "").lower()
    if not text.strip():
        return SafetyDecision(False, "Unknown", 0, "No action was provided.")

    risky = [term for term in RISKY_TERMS if term in text]
    read_only_hits = [term for term in READ_ONLY_TERMS if term in text]

    if risky:
        return SafetyDecision(
            allowed=False,
            risk="High",
            confidence=90,
            reason="Potentially destructive or service-impacting action detected: " + ", ".join(risky[:5]),
            requires_confirmation=True,
            requires_backup=True,
            read_only=False,
        )

    if read_only_hits:
        return SafetyDecision(True, "Low", 85, "Read-only diagnostic action.", False, False, True)

    return SafetyDecision(
        allowed=True,
        risk="Medium",
        confidence=55,
        reason="Action is not clearly destructive, but should be reviewed before use.",
        requires_confirmation=True,
        requires_backup=False,
        read_only=False,
    )

def audit_event(event_type: str, details: dict) -> Path:
    LOGS.mkdir(parents=True, exist_ok=True)
    payload = {
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "event_type": event_type,
        "details": details,
    }
    raw = json.dumps(payload, sort_keys=True)
    payload["event_hash"] = hashlib.sha256(raw.encode("utf-8")).hexdigest()
    out = LOGS / f"audit_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.json"
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return out

def safe_recommendation(text: str) -> dict:
    decision = classify_action(text)
    audit = audit_event("safety_decision", {"action": text, "decision": decision.as_dict()})
    data = decision.as_dict()
    data["audit_path"] = str(audit)
    return data
