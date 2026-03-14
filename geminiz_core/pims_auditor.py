"""
Gemini Z — PIMS Auditor (Live Panel)
Run in a separate terminal panel alongside Gemini CLI.
Watches the audit log and displays live PII access events.

Usage: python -m geminiz_core.pims_auditor
"""

import os
import sys
import time

# ANSI colors & controls
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BOLD = '\033[1m'
DIM = '\033[2m'
RESET = '\033[0m'
CYAN = '\033[96m'
CLEAR = '\033[2J\033[H'

from geminiz_core.audit_logger import read_audit_log

PIXEL_Z = f"""{GREEN}{BOLD}
  ███████╗
  ╚════██║
    ███╔═╝
  ██╔══╝
  ███████╗
  ╚══════╝{RESET}
"""


def render(audit_path):
    """Render the full auditor display."""
    entries = read_audit_log(audit_path)
    total = len(entries)
    allowed = sum(1 for e in entries if e['action'] == 'ALLOWED')
    blocked = sum(1 for e in entries if e['action'] == 'BLOCKED')

    print(CLEAR, end='')
    print(PIXEL_Z)
    print(f"  {BOLD}{GREEN}[GEMINI Z] PIMS Auditor{RESET}")
    print(f"  {DIM}Live monitoring • Privacy governance active{RESET}")
    print(f"  {GREEN}{'─'*60}{RESET}\n")

    print(f"  {BOLD}Total:{RESET} {total}  {GREEN}Allowed:{RESET} {allowed}  {RED}Blocked:{RESET} {blocked}\n")

    if not entries:
        print(f"  {DIM}Waiting for PII access events...{RESET}")
        print(f"  {DIM}Run Gemini CLI in another panel to see live data.{RESET}")
    else:
        # Show last 20 entries
        shown = entries[-20:]
        for entry in shown:
            action = entry['action']
            reason = entry.get('reason', '')
            if action == 'ALLOWED':
                color = GREEN
                icon = '✓'
            else:
                color = RED
                icon = '✗'

            ts_short = entry['timestamp'][11:19] if len(entry['timestamp']) > 19 else entry['timestamp']
            print(f"  {color}{icon} {ts_short}  {entry['tool']:<18} {entry['field']:<22} {BOLD}{action}{RESET}")
            if reason:
                print(f"    {DIM}{reason}{RESET}")

    print(f"\n  {GREEN}{'─'*60}{RESET}")
    print(f"  {DIM}Refreshing every 2s • Ctrl+C to stop{RESET}")


def main():
    audit_path = os.path.join(os.path.dirname(__file__), '..', '.gemini-z', 'audit.log')

    if len(sys.argv) > 1:
        audit_path = sys.argv[1]

    print(f"{GREEN}[GEMINI Z] PIMS Auditor starting...{RESET}")

    try:
        while True:
            render(audit_path)
            time.sleep(2)
    except KeyboardInterrupt:
        print(f"\n{GREEN}[GEMINI Z] Auditor stopped.{RESET}")


if __name__ == '__main__':
    main()
