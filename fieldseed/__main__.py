import argparse

from fieldseed.core.database import init_db, connect
from fieldseed.core.agent_loop import run_health_check
from fieldseed.core.ai_bridge import ask_fieldseed, ollama_online
from fieldseed.core.ticket_manager import list_tickets
from fieldseed.modes.collector import collect

from fieldseed.core.diagnostic_orchestrator import build_diagnostic_plan, format_plan
from fieldseed.core.safety_kernel import safe_recommendation
from fieldseed.core.evidence_score import score_evidence_package
from fieldseed.paths import ROOT, DATA, EVIDENCE, LOGS, TOOLS, DB
from fieldseed.playbooks import list_playbooks, render_playbook, search_playbooks


def doctor():
    init_db()
    print()
    print("FieldSeed Doctor")
    print("=" * 50)
    print(f"Project root: {ROOT}")
    print(f"Database: {DB}")
    print(f"Ollama: {'online' if ollama_online() else 'offline'}")

    required_paths = [ROOT / "fieldseed", ROOT / "fieldseed" / "core", ROOT / "fieldseed" / "modes", DATA, EVIDENCE, LOGS, TOOLS]
    required_files = [
        ROOT / "fieldseed" / "app.py",
        ROOT / "fieldseed" / "paths.py",
        ROOT / "fieldseed" / "core" / "database.py",
        ROOT / "fieldseed" / "core" / "agent_loop.py",
        ROOT / "fieldseed" / "core" / "ticket_manager.py",
        ROOT / "fieldseed" / "core" / "truth_gate.py",
        ROOT / "fieldseed" / "core" / "evidence_engine.py",
        ROOT / "fieldseed" / "modes" / "collector.py",
        ROOT / "START_FIELDSEED.bat",
        ROOT / "START_COLLECTOR_MODE.bat",
        ROOT / "START_RESCUE_MODE.bat",
    ]

    problems = []
    print()
    print("Required folders:")
    for path in required_paths:
        ok = path.exists() and path.is_dir()
        label = "OK" if ok else "MISSING"
        print(f"[{label}] {path}")
        if not ok:
            problems.append(f"Missing folder: {path}")

    print()
    print("Required files:")
    for path in required_files:
        ok = path.exists() and path.is_file()
        label = "OK" if ok else "MISSING"
        print(f"[{label}] {path}")
        if not ok:
            problems.append(f"Missing file: {path}")

    print()
    print("Python health check:")
    health = run_health_check()
    print(f"Checked Python files: {health['checked']}")
    print(f"Compile failures: {len(health['failures'])}")
    for filename, error in health["failures"]:
        print(f"- {filename}: {error}")
        problems.append(f"Compile failure: {filename}")

    print()
    print("Database check:")
    try:
        con = connect()
        tables = [row[0] for row in con.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
        con.close()
        print("Tables: " + ", ".join(tables))
    except Exception as exc:
        print(f"Database error: {exc}")
        problems.append(f"Database error: {exc}")

    print()
    print("Open tickets:")
    open_tickets = health.get("open_tickets", [])
    if not open_tickets:
        print("No open tickets detected.")
    else:
        for ticket_id, title, next_action in open_tickets:
            print(f"#{ticket_id} {title}")
            if next_action:
                print(f"Next: {next_action}")

    print()
    if problems:
        print(f"Doctor result: NEEDS ATTENTION ({len(problems)} issue(s))")
        return 1
    print("Doctor result: HEALTHY")
    return 0


def show_tickets(limit=25):
    init_db()
    rows = list_tickets(limit=limit)
    if not rows:
        print("No tickets yet.")
        return 0
    for row in rows:
        ticket_id, title, status, category, system, access_mode, access_tool, complete, next_action, updated = row
        print(f"#{ticket_id} [{status}] {title}")
        print(f"Category: {category}")
        print(f"System: {system}")
        print(f"Access: {access_mode} {access_tool}".strip())
        print(f"Complete: {complete}%")
        print(f"Updated: {updated}")
        if next_action:
            print(f"Next: {next_action}")
        print("-" * 50)
    return 0


def ask_brain(prompt):
    init_db()
    if not prompt:
        prompt = input("Ask FieldSeed Brain: ").strip()
    print(ask_fieldseed(prompt))
    return 0


def run_collector(args):
    mission = {
        "site": args.site or input("Site name: ").strip() or "Unknown Site",
        "customer": args.customer or input("Customer/company: ").strip(),
        "issue_type": args.issue or input("Issue type: ").strip() or "Unknown",
        "ticket_id": args.ticket or input("Ticket ID if known: ").strip(),
        "contact_name": args.contact or input("Contact person: ").strip(),
        "access_method": args.access_method,
        "level": args.level,
    }
    folder = collect(mission)
    print(f"Evidence saved: {folder}")
    return 0



def show_playbooks(query=""):
    matches = search_playbooks(query)
    if not matches:
        print("No matching playbooks found.")
        return 1
    if query and len(matches) == 1:
        print(render_playbook(matches[0]))
        return 0
    for name in matches:
        print(f"- {name}")
    print()
    print('Tip: run python -m fieldseed playbooks --show "OpenEye"')
    return 0

def show_playbook_detail(query):
    matches = search_playbooks(query)
    if not matches:
        print("No matching playbooks found.")
        return 1
    print(render_playbook(matches[0]))
    return 0

def launch_app():
    from fieldseed.app import FieldSeedApp
    init_db()
    app = FieldSeedApp()
    app.mainloop()
    return 0



def diagnose_cli(args):
    prompt = " ".join(args.issue).strip()
    if not prompt:
        prompt = input("Describe the issue: ").strip()
    plan = build_diagnostic_plan(prompt)
    print(format_plan(plan))
    return 0


def safety_cli(args):
    action = " ".join(args.action).strip()
    if not action:
        action = input("Action to safety-check: ").strip()
    result = safe_recommendation(action)
    print("FieldSeed Safety Gate")
    print("=" * 50)
    for key, value in result.items():
        print(f"{key}: {value}")
    return 0


def evidence_score_cli(args):
    result = score_evidence_package(args.path)
    print("FieldSeed Evidence Score")
    print("=" * 50)
    print(f"Status: {result['status']}")
    print(f"Score: {result['score']}%")
    print(f"Package: {result.get('package', args.path)}")
    for detail in result.get("details", []):
        print(f"- {detail}")
    return 0

def main():
    parser = argparse.ArgumentParser(description="FieldSeed command center")
    sub = parser.add_subparsers(dest="command")
    sub.add_parser("doctor")
    sub.add_parser("app")

    diagnose_parser = sub.add_parser("diagnose")
    diagnose_parser.add_argument("issue", nargs="*")

    safety_parser = sub.add_parser("safety")
    safety_parser.add_argument("action", nargs="*")

    evidence_parser = sub.add_parser("evidence-score")
    evidence_parser.add_argument("path")

    playbooks_parser = sub.add_parser("playbooks")
    playbooks_parser.add_argument("query", nargs="*")
    playbooks_parser.add_argument("--show", action="store_true")
    tickets_parser = sub.add_parser("tickets")
    tickets_parser.add_argument("--limit", type=int, default=25)
    brain_parser = sub.add_parser("brain")
    brain_parser.add_argument("prompt", nargs="*")
    collect_parser = sub.add_parser("collect")
    collect_parser.add_argument("--site", default="")
    collect_parser.add_argument("--customer", default="")
    collect_parser.add_argument("--issue", default="")
    collect_parser.add_argument("--ticket", default="")
    collect_parser.add_argument("--contact", default="")
    collect_parser.add_argument("--access-method", default="USB Collector")
    collect_parser.add_argument("--level", choices=["Quick", "Standard", "Deep"], default="Standard")
    args = parser.parse_args()
    if args.command == "doctor":
        return doctor()
    if args.command == "tickets":
        return show_tickets(args.limit)
    if args.command == "brain":
        return ask_brain(" ".join(args.prompt).strip())
    if args.command == "collect":
        return run_collector(args)
    if args.command == "diagnose":
        return diagnose_cli(args)

    if args.command == "safety":
        return safety_cli(args)

    if args.command == "evidence-score":
        return evidence_score_cli(args)

    if args.command == "app":
        return launch_app()
    if args.command == "playbooks":
        query = " ".join(args.query).strip()
        return show_playbook_detail(query) if args.show else show_playbooks(query)
    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
