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
