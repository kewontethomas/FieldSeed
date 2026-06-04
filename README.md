# FieldSeed

FieldSeed is a lightweight field-technician assistant for documenting service calls, following troubleshooting checklists, and turning messy field work into clean notes.

## Current MVP

This first version is a browser-based tool that can run from GitHub Pages or locally by opening `index.html`.

### Features

- Field dashboard for active service notes
- Guided troubleshooting flows for common field issues
- Site/device note capture
- Action checklist with completion tracking
- Auto-generated service summary
- Local browser storage so notes stay after refresh
- Exportable notes as plain text

## How to use

1. Open `index.html` in a browser.
2. Fill in the site, system, device, and issue details.
3. Pick a troubleshooting flow.
4. Work through the checklist.
5. Add findings and resolution notes.
6. Copy or download the final summary.

## Goal

FieldSeed is meant to grow into a practical technician companion for access control, cameras, servers, networking, and field documentation.

Future versions can include:

- Saved site profiles
- Device inventory
- IP scanner result imports
- CCURE / Exacq / OpenEye / Milestone troubleshooting playbooks
- Ticket templates
- Photo attachment support
- AI-assisted summaries
- Offline-first mobile support


## Command Center

Run these from the project root:

```powershell
python -m fieldseed doctor
python -m fieldseed app
python -m fieldseed collect
python -m fieldseed tickets
python -m fieldseed brain "OpenEye command station login works in web but not app"
```

Use `doctor` first after each major change. It checks folders, required files, Python compilation, database access, Ollama status, and open tickets.


## Advanced hardening commands

FieldSeed now includes a hardened safety spine for higher-trust technician work.

```powershell
python -m fieldseed diagnose "OpenEye command station login works in web but not app"
python -m fieldseed safety "restart service"
python -m fieldseed evidence-score "data/evidence_packages/example/evidence_package.json"
```

These commands add:
- safety/risk classification before actions
- diagnostic orchestration from issue text
- evidence package scoring
- audit JSON logs with event hashes
- stronger separation between confirmed knowledge, similar knowledge, and unknowns


## AI Contribution Model

FieldSeed uses AI as a controlled reasoning layer, not as an unchecked repair bot.

AI can contribute by:
- rewriting confirmed knowledge into clear technician language
- comparing the current issue to saved closed tickets
- helping summarize evidence packages
- suggesting questions to close unknowns
- ranking likely next diagnostic steps
- generating service-ticket notes from confirmed facts
- explaining why a fix is confirmed, similar, weak, or unknown

AI should not:
- invent fixes without evidence
- run destructive actions
- bypass the Safety Kernel
- treat similar issues as confirmed fixes
- modify systems without human approval, backup, and rollback plan

The intended flow is:

Issue -> Fact Engine -> Playbook Match -> Knowledge Match -> Evidence Score -> Safety Kernel -> Diagnostic Plan -> Audit Log.

## FieldSeed vNext Cockpit Layout

This build turns FieldSeed into the central desktop cockpit for the ecosystem:

- **Mission Control**: daily overview for tickets, health, improvement ideas, and system status.
- **Intake Engine**: paste emails, Teams messages, tickets, or work orders and extract ticket/task/checklist/closeout details.
- **Observe Mode**: captures before/after snapshots so FieldSeed can learn from what changed while a problem was being solved.
- **Toolbox**: launch point for Windows, network, storage/RAID, camera/VMS, access control, and USB rescue workflows.
- **Tickets**: quick work capture for simple boring tickets and complex issues.
- **Playbooks**: guided procedures for repeat field work.
- **Brain**: truth-gated AI assistant and diagnostic planner.
- **Evidence**: collector/import/score area for desktop, USB, and remote evidence packages.
- **Memory**: confirmed fixes, closed tickets, observations, and reusable knowledge.
- **Systems**: architecture map for Desktop App, USB Rescue, GPS Task App, Cloud Hub, and Observer Agents.
- **Safety Audit**: risk classification and audit review.
- **Growth**: self-inspection, repair candidates, and screenshot evidence.

New command line helpers:

```powershell
python -m fieldseed intake --file email.txt --ticket --geo-task
python -m fieldseed observe start "camera offline issue"
python -m fieldseed observe stop --folder data/observations/<folder> --resolved --note "Camera returned online"
python -m fieldseed audit
```


## GPS Context App Integration

FieldSeed is the intelligence layer and your GPS/context app is the execution layer.

1. Open FieldSeed Desktop.
2. Go to **Sites**.
3. Click **Set GPS App Drop Folder**.
4. Choose the folder your GPS/context app watches for imports.
5. In **Intake**, paste or load a ticket/email.
6. Review and correct the extracted fields.
7. Click **Export GPS Task** or **Ticket + GPS**.

FieldSeed writes each task JSON to:

```text
data/tasks/
data/gps_outbox/
```

If a GPS drop folder is configured, FieldSeed also copies the same task package there. Your GPS app should import the JSON, create a location-aware task, and later send back completion/arrival/departure data.

## Ticket Protection

FieldSeed now blocks empty quick tickets. Tickets can also be archived or deleted from the Ticket board. Delete removes the ticket and timeline; archive keeps it out of active work without losing history.
