PLAYBOOKS = {
    "CCURE Badge / Door Issue": {
        "system": "CCure",
        "category": "Access Control",
        "goal": "Find whether the issue is badge, person record, clearance, schedule, reader, panel, or door group related.",
        "steps": [
            "Confirm scope: one badge/user, one door/reader, tenant group, or everyone.",
            "Check the person's record: active status, expiration, lost/stolen flag, badge number, and assigned clearances.",
            "Verify the door/reader is in the expected door group and schedule.",
            "Check recent changes: new group, schedule, holiday, tenant change, or clearance edit.",
            "Review recent access events for denied reason and exact reader name.",
            "If only one group is failing, create or clone a clean door group and retest before editing many records.",
            "Document confirmed root cause and the exact fix in the ticket before closing."
        ],
        "do_not_guess": [
            "Do not assume a badge is bad until you confirm event history.",
            "Do not change broad access groups without documenting before/after behavior."
        ]
    },
    "OpenEye Command Station Login Issue": {
        "system": "OpenEye",
        "category": "Video / Camera",
        "goal": "Separate web portal authentication from local Command Station client/database/profile problems.",
        "steps": [
            "Confirm the same username works in the web client/service.",
            "Confirm whether the error is invalid credentials, app crash, server connection, or permissions.",
            "Test another known-good user in Command Station if allowed.",
            "Check whether the local app profile/database/cache is corrupt or stale.",
            "Rename or back up the local Command Station database/profile folder before resetting it.",
            "Reconfigure the application connection and retest the user login.",
            "Record whether the fix was local app reconfiguration, credential reset, permissions, or server-side change."
        ],
        "do_not_guess": [
            "Do not reset credentials if web login already proves credentials work.",
            "Do not delete local app data without backing it up or renaming it first."
        ]
    },
    "Exacq Camera / Recording Issue": {
        "system": "ExacqVision",
        "category": "Video / Camera",
        "goal": "Determine whether the issue is camera connectivity, recording schedule, storage, licensing, or client playback.",
        "steps": [
            "Confirm live video works, playback works, or both fail.",
            "Check whether one camera, a group, or all cameras are affected.",
            "Verify server storage is online, initialized, and assigned for recording.",
            "Review camera status and recent disconnect events.",
            "Check recording schedule and retention settings.",
            "Confirm server time is correct before judging playback gaps.",
            "Document exact camera names, times tested, storage path, and confirmed fix."
        ],
        "do_not_guess": [
            "Do not assume cameras are down if live view works but playback fails.",
            "Do not rebuild storage without confirming recording target and retention settings."
        ]
    },
    "Milestone XProtect Playback Issue": {
        "system": "Milestone XProtect",
        "category": "Video / Camera",
        "goal": "Separate Management Server, Recording Server, storage, camera, and client-side playback causes.",
        "steps": [
            "Confirm whether live video works and playback fails, or both fail.",
            "Identify affected camera count and exact timeframe.",
            "Check Recording Server service state and storage availability.",
            "Verify camera recording settings and archive paths.",
            "Check Management Client for device status, recording server status, and recent warnings.",
            "Test playback from another client/workstation if possible.",
            "Document confirmed recording path, service state, and fix."
        ],
        "do_not_guess": [
            "Do not assume missing playback means camera failure.",
            "Do not upgrade components until current version, backup, and affected server roles are documented."
        ]
    },
    "Windows Update Boot Loop": {
        "system": "Windows",
        "category": "Windows / Server",
        "goal": "Stop a stuck update loop without deleting customer data.",
        "steps": [
            "Confirm the Windows drive letter from recovery before running commands.",
            "Back up or preserve customer/application data before destructive actions.",
            "Check pending update state and failed update logs where possible.",
            "Use offline recovery actions to revert pending updates before attempting repair installs.",
            "Run disk and file system checks only after confirming the correct volume.",
            "If repair succeeds, reboot and confirm application services start normally.",
            "Document exact drive letters, commands used, and final boot result."
        ],
        "do_not_guess": [
            "Do not assume C: in WinRE is the Windows partition.",
            "Do not wipe or reset Windows before preserving application data and checking recovery options."
        ]
    },
    "RAID / Storage Recording Issue": {
        "system": "Storage",
        "category": "Storage",
        "goal": "Restore usable recording storage while avoiding accidental data loss.",
        "steps": [
            "Identify controller, virtual disks, physical disks, and foreign/offline states.",
            "Confirm whether drives need RAID or individual recording volumes.",
            "Check if the OS/application sees the volumes after controller changes.",
            "Initialize or format only the intended recording drives, not the OS drive.",
            "Assign recording paths inside the VMS/application after Windows sees storage.",
            "Test live view and playback/recording after storage assignment.",
            "Document controller state, drive IDs, volume labels, and application recording target."
        ],
        "do_not_guess": [
            "Do not clear foreign config until you know whether data must be preserved.",
            "Do not initialize a disk unless you are sure it is not the OS or needed data volume."
        ]
    },
    "Server Random Shutdown": {
        "system": "Windows Server",
        "category": "Windows / Server",
        "goal": "Find whether shutdowns are power, thermal, hardware, update, OS, or application triggered.",
        "steps": [
            "Check System event logs for Kernel-Power, BugCheck, thermal, disk, or controller events.",
            "Check uptime and exact shutdown pattern.",
            "Review hardware health: fans, PSU, RAID/controller, disk SMART/status, and temperatures.",
            "Check scheduled tasks, Windows Update restart history, and vendor management logs.",
            "Confirm UPS/power source and whether other devices lose power.",
            "Collect evidence package before changing hardware or OS settings.",
            "Document event IDs, timestamps, hardware findings, and next action."
        ],
        "do_not_guess": [
            "Do not call it a power issue without logs or power evidence.",
            "Do not replace hardware before checking event timing and health indicators."
        ]
    },
    "Network Device Discovery Issue": {
        "system": "Network",
        "category": "Network",
        "goal": "Find devices that should be labeled or reachable but are missing from scans.",
        "steps": [
            "Confirm the expected subnet, VLAN, and gateway for the missing devices.",
            "Compare scanner results against DHCP leases, ARP table, switch MAC table, and known server software.",
            "Check whether devices may be isolated by VLAN, firewall, offline state, or static IP outside the scanned range.",
            "Use known systems like CCURE, Exacq, OpenEye, or Milestone to identify device names/IPs from application records.",
            "Ping known addresses and compare hostname, MAC vendor, and open ports only where authorized.",
            "Label confirmed devices in your notes with evidence source.",
            "Document unknowns instead of inventing names."
        ],
        "do_not_guess": [
            "Do not rename or label devices based only on scanner guesses.",
            "Do not scan networks you are not authorized to troubleshoot."
        ]
    }
}


def list_playbooks():
    return sorted(PLAYBOOKS.keys())


def get_playbook(name):
    return PLAYBOOKS.get(name)


def search_playbooks(query):
    q = (query or "").lower().strip()
    if not q:
        return list_playbooks()
    matches = []
    for name, book in PLAYBOOKS.items():
        hay = " ".join([name, book.get("system", ""), book.get("category", ""), book.get("goal", ""), " ".join(book.get("steps", []))]).lower()
        if any(part in hay for part in q.split()):
            matches.append(name)
    return sorted(matches)


def render_playbook(name):
    book = get_playbook(name)
    if not book:
        return "Playbook not found."
    lines = [name, "=" * len(name), f"System: {book['system']}", f"Category: {book['category']}", "", f"Goal: {book['goal']}", "", "Steps:"]
    for index, step in enumerate(book.get("steps", []), 1):
        lines.append(f"{index}. {step}")
    warnings = book.get("do_not_guess", [])
    if warnings:
        lines.extend(["", "Do not guess:"])
        for item in warnings:
            lines.append(f"- {item}")
    return "\n".join(lines)
