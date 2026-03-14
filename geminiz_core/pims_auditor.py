"""
Gemini Z — PIMS Auditor (Live Panel)
Run in a separate terminal panel alongside Gemini CLI.
Watches the audit log and displays live PII access events.
Uses in-place rewriting like tqdm — no screen clearing, no flicker.

Usage: python -m geminiz_core.pims_auditor
"""

import os
import sys
import time
import shutil

GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BOLD = '\033[1m'
DIM = '\033[2m'
RESET = '\033[0m'
CYAN = '\033[96m'
HIDE_CURSOR = '\033[?25l'
SHOW_CURSOR = '\033[?25h'
MOVE_UP = '\033[{}A'
CLEAR_LINE = '\033[2K'

from geminiz_core.audit_logger import read_audit_log

PIXEL_Z = f"""{GREEN}{BOLD}    ███████╗
    ╚════██║
      ███╔═╝
    ██╔══╝
    ███████╗
    ╚══════╝{RESET}"""

SPINNER = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']


def build_frame(entries, frame, prev_count, max_rows):
    """Build all lines for one frame."""
    lines = []
    total = len(entries)
    allowed = sum(1 for e in entries if e['action'] == 'ALLOWED')
    blocked = sum(1 for e in entries if e['action'] == 'BLOCKED')
    spin = SPINNER[frame % len(SPINNER)]

    lines.append(f"    {BOLD}{GREEN}🛡️  [GEMINI Z] PIMS Auditor{RESET}  {GREEN}{spin}{RESET}")
    lines.append(f"    {DIM}📡 Live monitoring • Privacy governance active{RESET}")
    lines.append(f"    {GREEN}{'─'*58}{RESET}")
    lines.append(f"    📊 {BOLD}Total:{RESET} {total}  ✅ {GREEN}Allowed:{RESET} {allowed}  🚫 {RED}Blocked:{RESET} {blocked}")

    if blocked > 0 and total > 0:
        pct = round(blocked / total * 100)
        bar_len = 20
        filled = round(pct / 100 * bar_len)
        bar = f"{RED}{'█' * filled}{DIM}{'░' * (bar_len - filled)}{RESET}"
        lines.append(f"    🔒 Blocked: [{bar}] {BOLD}{RED}{pct}%{RESET}")
    else:
        lines.append(f"    🔒 Blocked: [{DIM}{'░' * 20}{RESET}] 0%")

    lines.append(f"    {GREEN}{'─'*58}{RESET}")

    if not entries:
        lines.append(f"    {spin} {DIM}Waiting for PII access events...{RESET}")
        lines.append(f"    {DIM}💡 Run Gemini CLI in another panel{RESET}")
        # Pad to fixed height
        for _ in range(max_rows - len(lines) - 2):
            lines.append("")
    else:
        lines.append(f"    {BOLD}{'⏰ Time':<11} {'🔧 Tool':<19} {'📋 Field':<23} {'Status'}{RESET}")
        lines.append(f"    {'─'*58}")

        # How many entry rows we can show
        entry_rows = max_rows - len(lines) - 3  # leave room for footer
        shown = entries[-max(entry_rows, 3):]

        for entry in shown:
            action = entry['action']
            if action == 'ALLOWED':
                color = GREEN
                icon = '✅'
            else:
                color = RED
                icon = '🚫'

            ts = entry['timestamp'][11:19] if len(entry['timestamp']) > 19 else entry['timestamp']
            tool = entry['tool'][:17]
            field = entry['field'][:21]

            lines.append(f"    {color}{icon} {ts:<9} {tool:<19} {field:<23} {BOLD}{action}{RESET}")

        # Pad remaining rows
        remaining = max_rows - len(lines) - 3
        for _ in range(max(remaining, 0)):
            lines.append("")

        if total > prev_count and prev_count > 0:
            new_count = total - prev_count
            lines.append(f"    {BOLD}{YELLOW}⚡ +{new_count} new event(s)!{RESET}")
        else:
            lines.append("")

    lines.append(f"    {GREEN}{'─'*58}{RESET}")
    lines.append(f"    {GREEN}{spin}{RESET} {DIM}Refreshing every 1s • Ctrl+C to stop{RESET}")

    return lines


def main():
    audit_path = os.path.join(os.path.dirname(__file__), '..', '.gemini-z', 'audit.log')
    if len(sys.argv) > 1:
        audit_path = sys.argv[1]

    sys.stdout.write(HIDE_CURSOR)
    sys.stdout.flush()

    # Print the pixel Z once (stays at top, never redrawn)
    print(PIXEL_Z)
    print()

    term_lines = shutil.get_terminal_size().lines
    max_rows = term_lines - 10  # Z art takes ~7 lines + padding

    frame = 0
    prev_count = 0
    first_draw = True

    try:
        while True:
            entries = read_audit_log(audit_path)
            total = len(entries)

            lines = build_frame(entries, frame, prev_count, max_rows)

            # Move cursor up to overwrite previous frame (tqdm style)
            if not first_draw:
                sys.stdout.write(MOVE_UP.format(len(lines)))

            for line in lines:
                sys.stdout.write(CLEAR_LINE + line + '\n')

            sys.stdout.flush()
            first_draw = False
            prev_count = total
            frame += 1
            time.sleep(1)

    except KeyboardInterrupt:
        sys.stdout.write(SHOW_CURSOR)
        sys.stdout.flush()
        print(f"\n{GREEN}🛡️  [GEMINI Z] Auditor stopped.{RESET}")


if __name__ == '__main__':
    main()
