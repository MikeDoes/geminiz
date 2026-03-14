"""
Audit Logger — Logs all PII access attempts for Gemini Z.
Every access is recorded: which tool, which data, when, allowed or blocked.
"""

import os
from datetime import datetime, timezone


def log_access(audit_path, tool_name, field_name, value, action, reason=''):
    """Log a PII access attempt to the audit file.

    Args:
        audit_path: Path to the audit log file
        tool_name: Name of the tool/skill requesting access
        field_name: PIMS field name (e.g. BOOKING_CODE, PASSPORT_NUMBER)
        value: The actual value detected (masked in log for blocked items)
        action: ALLOWED, BLOCKED, or USER_APPROVED
        reason: Why this field was accessed (e.g. "Flight check-in requires booking code")
    """
    timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

    # Mask value for blocked items in the log
    if action == 'BLOCKED':
        masked_value = '*' * min(len(value), 20)
    else:
        masked_value = value[:3] + '***' if len(value) > 3 else value

    if not reason:
        if action == 'ALLOWED':
            reason = f"Tool declared {field_name} as required"
        else:
            reason = f"{field_name} not in tool's declared PII scope"

    log_line = f"{timestamp} | {tool_name:<20} | {field_name:<30} | {action:<15} | {masked_value:<22} | {reason}\n"

    os.makedirs(os.path.dirname(audit_path), exist_ok=True)
    with open(audit_path, 'a') as f:
        f.write(log_line)


def read_audit_log(audit_path):
    """Read and return all audit log entries."""
    if not os.path.exists(audit_path):
        return []

    entries = []
    with open(audit_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 4:
                entries.append({
                    'timestamp': parts[0],
                    'tool': parts[1],
                    'field': parts[2],
                    'action': parts[3],
                    'value': parts[4] if len(parts) > 4 else '',
                    'reason': parts[5] if len(parts) > 5 else '',
                })
    return entries


def clear_audit_log(audit_path):
    """Clear the audit log."""
    if os.path.exists(audit_path):
        os.remove(audit_path)
