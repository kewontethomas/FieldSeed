from __future__ import annotations
from datetime import datetime

from .fact_engine import analyze_intake
from .truth_gate import search_knowledge
from .safety_kernel import safe_recommendation, audit_event

BASE_ACTIONS = {
    "Video / Camera": [
        "Check whether live video, playback, or both are failing.",
        "Collect camera server services, event logs, disk status, and VMS platform notes.",
        "Confirm whether the issue affects one camera, multiple cameras, or the full recorder.",
    ],
    "Access Control": [
        "Confirm whether this affects one badge, one reader, one door group, or all access.",
        "Check recent group, clearance, schedule, holiday, and personnel changes.",
        "Document exact reader/door, cardholder, time, and access result.",
    ],
    "Windows / Server": [
        "Collect systeminfo, event logs, services, disk health, and recent update history.",
        "Confirm uptime, shutdown pattern, and whether the issue repeats after 24 hours.",
        "Check power, thermal, storage, service, update, and application error evidence.",
    ],
    "Network": [
        "Confirm IP, hostname, subnet, gateway, DNS, and whether device appears in scanner results.",
        "Compare switch/MAC/IP evidence before assuming a device is missing.",
        "Document what is reachable by ping, web portal, RDP, or vendor client.",
    ],
    "Storage": [
        "Collect disk, RAID/controller, recording path, and event log evidence.",
        "Confirm whether recording storage is mounted, initialized, online, and assigned correctly.",
        "Do not delete or initialize unknown disks until role and data status are confirmed.",
    ],
    "Application": [
        "Confirm whether login works in web portal, thick client, another workstation, or local server.",
        "Check local app cache/database/profile state before assuming account credentials are bad.",
        "Document exact error, account, app version, and successful alternate access method.",
    ],
}

def build_diagnostic_plan(issue_text: str) -> dict:
    analysis = analyze_intake(issue_text)
    knowledge = search_knowledge(issue_text)
    actions = BASE_ACTIONS.get(analysis["category"], [
        "Identify the affected system, access method, scope, and most recent change.",
        "Collect evidence before attempting a fix.",
        "Create or update a ticket with confirmed facts and unknowns.",
    ])

    gated_actions = []
    for action in actions:
        gated_actions.append({"action": action, "safety": safe_recommendation(action)})

    plan = {
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "issue": issue_text,
        "analysis": analysis,
        "knowledge_state": knowledge.get("match", {}).get("state", "unknown"),
        "knowledge_confidence": knowledge.get("confidence", 0),
        "actions": gated_actions,
        "rule": "Evidence first. Confirm scope. Do not guess. Escalate destructive actions.",
    }
    audit_event("diagnostic_plan", plan)
    return plan

def format_plan(plan: dict) -> str:
    a = plan["analysis"]
    lines = [
        "FieldSeed Diagnostic Plan",
        "=" * 50,
        f"Category: {a.get('category')}",
        f"System: {a.get('confirmed_system')}",
        f"Access: {a.get('access_mode')} {a.get('access_tool')}".strip(),
        f"Completeness: {a.get('completeness')}%",
        "",
        "Confirmed facts:",
    ]
    for fact in a.get("confirmed_facts", []):
        lines.append(f"- {fact}")
    lines.append("")
    lines.append("Unknowns:")
    for item in a.get("unknowns", []):
        lines.append(f"- {item}")
    lines.append("")
    lines.append("Recommended next actions:")
    for i, item in enumerate(plan.get("actions", []), start=1):
        s = item["safety"]
        lines.append(f"{i}. {item['action']}")
        lines.append(f"   Safety: {s['risk']} | Allowed: {s['allowed']} | {s['reason']}")
    lines.append("")
    lines.append(plan.get("rule", ""))
    return "\n".join(lines)
