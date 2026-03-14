"""
Gemini Z — Audit Trail Viewer
Run: python -m geminiz_core.audit_viewer
Shows all PII access attempts with colored output and emojis.
"""

import os
import sys

# ANSI colors
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BOLD = '\033[1m'
DIM = '\033[2m'
RESET = '\033[0m'
CYAN = '\033[96m'

from geminiz_core.audit_logger import read_audit_log


def display_audit(audit_path=None):
    if audit_path is None:
        audit_path = os.path.join(os.path.dirname(__file__), '..', '.gemini-z', 'audit.log')

    entries = read_audit_log(audit_path)

    if not entries:
        print(f"\n{YELLOW}⚠️  No audit entries found.{RESET}")
        print(f"{DIM}💡 Run a demo first to generate audit data.{RESET}\n")
        return

    print(f"\n{BOLD}{GREEN}{'='*90}{RESET}")
    print(f"{BOLD}{GREEN}  🛡️  [GEMINI Z] Audit Trail  📋{RESET}")
    print(f"{BOLD}{GREEN}{'='*90}{RESET}\n")

    # Stats
    total = len(entries)
    allowed = sum(1 for e in entries if e['action'] == 'ALLOWED')
    blocked = sum(1 for e in entries if e['action'] == 'BLOCKED')

    print(f"  📊 {BOLD}Total:{RESET} {total}    "
          f"✅ {GREEN}Allowed:{RESET} {allowed}    "
          f"🚫 {RED}Blocked:{RESET} {blocked}")

    if blocked > 0:
        pct = round(blocked / total * 100)
        print(f"  🔒 {BOLD}Threat prevention rate: {RED}{pct}%{RESET} of accesses blocked")
    print()

    print(f"  {BOLD}{'⏰ Timestamp':<26} {'🔧 Tool':<22} {'📋 Field':<27} {'Decision':<12} {'Reason'}{RESET}")
    print(f"  {'─'*100}")

    for entry in entries:
        action = entry['action']
        reason = entry.get('reason', '')
        if action == 'ALLOWED':
            color = GREEN
            icon = '✅'
        elif action == 'BLOCKED':
            color = RED
            icon = '🚫'
        else:
            color = YELLOW
            icon = '❓'

        print(f"  {color}{icon} {entry['timestamp']:<22} {entry['tool']:<22} {entry['field']:<25} {BOLD}{action:<12}{RESET} {DIM}{reason}{RESET}")

    print(f"\n  {'─'*100}")
    print(f"  {DIM}📁 Log file: {audit_path}{RESET}\n")


if __name__ == '__main__':
    if len(sys.argv) > 1:
        display_audit(sys.argv[1])
    else:
        display_audit()
