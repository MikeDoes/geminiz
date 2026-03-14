"""
Gemini Z — PIMS Auditor (Live Panel)
Run in a separate terminal panel alongside Gemini CLI.
Watches the audit log and displays live PII access events with auto-scroll.

Usage: python -m geminiz_core.pims_auditor
"""

import os
import sys
import time
import shutil

# ANSI colors & controls
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BOLD = '\033[1m'
DIM = '\033[2m'
RESET = '\033[0m'
CYAN = '\033[96m'
WHITE = '\033[97m'
CLEAR = '\033[2J\033[H'
HIDE_CURSOR = '\033[?25l'
SHOW_CURSOR = '\033[?25h'

from geminiz_core.audit_logger import read_audit_log

PIXEL_Z = f"""{GREEN}{BOLD}
    ███████╗
    ╚════██║
      ███╔═╝
    ██╔══╝
    ███████╗
    ╚══════╝{RESET}
"""

SPINNER = ['🔄', '🔃', '🔄', '🔃']


def render(audit_path, frame=0, prev_count=0):
    """Render the full auditor display."""
    cols = shutil.get_terminal_size().columns
    entries = read_audit_log(audit_path)
    total = len(entries)
    allowed = sum(1 for e in entries if e['action'] == 'ALLOWED')
    blocked = sum(1 for e in entries if e['action'] == 'BLOCKED')
    is_new = total > prev_count

    print(CLEAR, end='')
    print(PIXEL_Z)
    print(f"    {BOLD}{GREEN}🛡️  [GEMINI Z] PIMS Auditor{RESET}")
    print(f"    {DIM}📡 Live monitoring • Privacy governance active{RESET}")
    print(f"    {GREEN}{'─'*min(60, cols-4)}{RESET}\n")

    print(f"    📊 {BOLD}Total:{RESET} {total}    ✅ {GREEN}Allowed:{RESET} {allowed}    🚫 {RED}Blocked:{RESET} {blocked}")

    if blocked > 0:
        pct = round(blocked / total * 100) if total > 0 else 0
        print(f"    🔒 {BOLD}{RED}Threat prevention rate: {pct}% of accesses blocked{RESET}")
    print()

    if not entries:
        spin = SPINNER[frame % len(SPINNER)]
        print(f"    {spin} {DIM}Waiting for PII access events...{RESET}")
        print(f"    {DIM}💡 Run Gemini CLI in another panel to see live data.{RESET}")
    else:
        # Show header
        print(f"    {BOLD}{'⏰ Time':<12} {'🔧 Tool':<20} {'📋 Field':<24} {'Status':<10}{RESET}")
        print(f"    {'─'*min(65, cols-4)}")

        # Auto-scroll: show last entries that fit the terminal
        rows_available = shutil.get_terminal_size().lines - 22
        shown = entries[-max(rows_available, 5):]

        for entry in shown:
            action = entry['action']
            reason = entry.get('reason', '')
            if action == 'ALLOWED':
                color = GREEN
                icon = '✅'
            else:
                color = RED
                icon = '🚫'

            ts_short = entry['timestamp'][11:19] if len(entry['timestamp']) > 19 else entry['timestamp']
            tool_display = entry['tool'][:18]
            field_display = entry['field'][:22]

            print(f"    {color}{icon} {ts_short:<10} {tool_display:<20} {field_display:<24} {BOLD}{action}{RESET}")

        if is_new and total > prev_count:
            new_count = total - prev_count
            print(f"\n    {BOLD}{YELLOW}⚡ +{new_count} new event(s) detected!{RESET}")

    print(f"\n    {GREEN}{'─'*min(60, cols-4)}{RESET}")
    spin = SPINNER[frame % len(SPINNER)]
    print(f"    {spin} {DIM}Auto-refreshing • Ctrl+C to stop{RESET}")

    return total


def main():
    audit_path = os.path.join(os.path.dirname(__file__), '..', '.gemini-z', 'audit.log')

    if len(sys.argv) > 1:
        audit_path = sys.argv[1]

    print(HIDE_CURSOR, end='')
    print(f"{GREEN}🛡️  [GEMINI Z] PIMS Auditor starting...{RESET}")

    frame = 0
    prev_count = 0
    try:
        while True:
            prev_count = render(audit_path, frame, prev_count)
            frame += 1
            time.sleep(1)
    except KeyboardInterrupt:
        print(SHOW_CURSOR)
        print(f"\n{GREEN}🛡️  [GEMINI Z] Auditor stopped.{RESET}")


if __name__ == '__main__':
    main()
