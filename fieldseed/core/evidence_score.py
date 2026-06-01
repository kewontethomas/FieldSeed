from __future__ import annotations
import json
from pathlib import Path

REQUIRED_KEYS = ["created_at", "site", "issue_type", "hostname", "platform", "commands", "command_results"]

def score_evidence_package(path: str | Path) -> dict:
    p = Path(path)
    package = p / "evidence_package.json" if p.is_dir() else p
    if not package.exists():
        return {"score": 0, "status": "Missing", "details": ["No evidence_package.json found."]}

    data = json.loads(package.read_text(encoding="utf-8", errors="ignore"))
    details = []
    score = 0

    for key in REQUIRED_KEYS:
        if key in data and data.get(key) not in ("", None, [], {}):
            score += 10
        else:
            details.append(f"Missing or empty: {key}")

    commands = data.get("commands", {})
    command_results = data.get("command_results", [])

    if commands:
        score += min(20, len(commands) * 2)
    ok_count = sum(1 for r in command_results if r.get("ok"))
    fail_count = sum(1 for r in command_results if not r.get("ok"))
    score += min(20, ok_count * 2)
    score -= min(20, fail_count * 3)

    if data.get("findings"):
        score += 10
    else:
        details.append("No automatic findings were generated.")

    score = max(0, min(100, score))
    status = "Strong" if score >= 80 else "Usable" if score >= 60 else "Weak" if score >= 35 else "Insufficient"
    return {"score": score, "status": status, "details": details, "package": str(package)}
