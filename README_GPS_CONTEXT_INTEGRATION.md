# FieldSeed ↔ GPS Context Assistant Integration

FieldSeed is the technician intelligence system.
GPS Context Assistant is the location-based task/reminder system.

## Intended flow

1. Paste a work order, email, Teams message, or service note into FieldSeed Intake.
2. Review and correct the parsed work task.
3. Click **GPS Task** or **Ticket + GPS**.
4. FieldSeed creates a GPS Context-compatible JSON package in:

```text
data/gps_outbox
```

5. FieldSeed also creates a deep-link text file like:

```text
geo_task_YYYYMMDD_HHMMSS_gps_import_link.txt
```

6. Open that link on the Android phone that has GPS Context Assistant installed.
7. GPS Context Assistant imports the task into the FieldSeed Inbox.
8. Review/accept the task in GPS Context Assistant.
9. It becomes a normal location-based task.

## Payload format

```json
{
  "externalSourceId": "fieldseed-20260603-120000",
  "title": "Verify server storage",
  "placeName": "Work",
  "notes": "Check RAID status and playback storage.",
  "priority": "high",
  "contextType": "work",
  "reminderProfile": "persistent",
  "dueDate": "Next arrival",
  "dueTime": "As soon as available"
}
```

## Full desktop app build

Run:

```powershell
.\BUILD_FIELDSEED_APP.bat
```

The desktop build uses:

```text
assets\fieldseed.ico
```

as the application icon.

The built app will be created under:

```text
dist\FieldSeed\FieldSeed.exe
```
