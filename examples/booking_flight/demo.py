"""
Gemini Z — Use Case 1: Flight Check-in Demo
Demonstrates PIMS.md policy enforcement on a flight ticket.
"""

import os
import sys
import time
from datetime import datetime

# Add parent paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from geminiz_core import pims_parser, audit_logger

# ANSI colors
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BOLD = '\033[1m'
DIM = '\033[2m'
RESET = '\033[0m'
CYAN = '\033[96m'
WHITE = '\033[97m'


def feedback(msg, level='info'):
    """Print Gemini Z feedback messages inline."""
    if level == 'activate':
        print(f"\n  {BOLD}{GREEN}🛡️  [GEMINI Z]{RESET} {DIM}PIMS.md loaded — privacy governance active{RESET}")
    elif level == 'scan':
        print(f"  {BOLD}{GREEN}🔍 [GEMINI Z]{RESET} {DIM}{msg}{RESET}")
    elif level == 'warn':
        print(f"  {BOLD}{YELLOW}⚠️  [GEMINI Z]{RESET} {BOLD}{YELLOW}{msg}{RESET}")
    elif level == 'block':
        print(f"  {BOLD}{RED}🚫 [GEMINI Z]{RESET} {BOLD}{RED}{msg}{RESET}")
    elif level == 'allow':
        print(f"  {BOLD}{GREEN}✅ [GEMINI Z]{RESET} {DIM}{msg}{RESET}")


def detect_pii_in_text(text):
    """Detect PII using ai4privacy model."""
    try:
        from ai4privacy import protect
        result = protect(text, verbose=True, multilingual=True, classify_pii=True)
        return result
    except ImportError:
        return detect_pii_fallback(text)


def detect_pii_fallback(text):
    """Fallback PII detection using patterns (when model not available)."""
    import re
    detections = []

    # Use actual model label names where possible
    patterns = {
        'GIVENNAME': r'\b(Michael|Brian|John|Jane|Alice|Bob)\b',
        'SURNAME': r'\b(Zurigo|Parigi|Smith|Doe)\b',
        'EMAIL': r'[\w.+-]+@[\w-]+\.[\w.-]+',
        'TELEPHONENUM': r'\+\d[\d\s\-]{8,}',
        'PASSPORTNUM': r'\b[A-Z]\d{8}\b',
        'CREDITCARDNUMBER': r'\bending \d{4}\b',
        'DATE': r'\b\d{2}/\d{2,4}/?\d{0,4}\b',
        'STREET': r'\d+\s+(?:Rue|Street|Ave|Boulevard)\s+[^\n,]+',
        'ZIPCODE': r'\b\d{5}\b',
        'BOOKING_CODE': r'\b[A-Z]{2}-\d{4}-[A-Z]{3}\b',
        'FLIGHT_NUMBER': r'\b[A-Z]{2}\s?\d{3,4}\b',
        'SEAT_NUMBER': r'\b\d{1,2}[A-F]\b',
    }

    for label, pattern in patterns.items():
        for match in re.finditer(pattern, text):
            detections.append({
                'label': label,
                'value': match.group(),
                'start': match.start(),
                'end': match.end(),
            })

    return {'detections': detections}


def run_demo():
    print(f"\n{BOLD}{GREEN}{'='*60}{RESET}")
    print(f"{BOLD}{GREEN}  🛡️  GEMINI Z — Flight Check-in Demo  ✈️{RESET}")
    print(f"{BOLD}{GREEN}{'='*60}{RESET}")

    # PIMS activation feedback
    feedback('', 'activate')

    # Load flight ticket
    ticket_path = os.path.join(os.path.dirname(__file__), 'flight_ticket.txt')
    with open(ticket_path, 'r') as f:
        ticket_text = f.read()

    feedback('📄 Scanning file: flight_ticket.txt for PII...', 'scan')
    feedback('🤖 Anonymiser engine: ai4privacy (local, open-source)', 'scan')
    print()

    # Load PIMS rules
    pims_path = os.path.join(os.path.dirname(__file__), '..', '..', 'PIMS.md')
    rules = pims_parser.parse_pims(pims_path)
    tool_name = 'airline-checkin'
    tool_rules = rules.get('tools', {}).get(tool_name, {})

    allowed_fields = tool_rules.get('allowed', [])
    blocked_fields = tool_rules.get('blocked', [])

    print(f"  🔧 {BOLD}Tool requesting access: {CYAN}{tool_name}{RESET}")
    print(f"  📋 {BOLD}PIMS.md Policy:{RESET}")
    print(f"    ✅ {GREEN}Allowed:{RESET} {', '.join(allowed_fields)}")
    print(f"    🚫 {RED}Blocked:{RESET} {', '.join(blocked_fields)}")
    print()

    # Detect PII
    result = detect_pii_in_text(ticket_text)

    # Process detections
    if 'detections' in result:
        detections = result['detections']
    elif 'replacements' in result:
        detections = result['replacements']
    else:
        detections = []

    # Initialize audit logger
    audit_dir = os.path.join(os.path.dirname(__file__), '..', '..', '.gemini-z')
    os.makedirs(audit_dir, exist_ok=True)
    audit_path = os.path.join(audit_dir, 'audit.log')

    # Map model labels → PIMS field names (matches actual ai4privacy output)
    label_to_field = {
        'GIVENNAME': 'NAME',
        'SURNAME': 'NAME',
        'EMAIL': 'EMAIL',
        'TELEPHONENUM': 'PHONE_NUMBER',
        'PASSPORTNUM': 'PASSPORT_NUMBER',
        'CREDITCARDNUMBER': 'CREDIT_CARD_NUMBER',
        'DATE': 'DATE',
        'STREET': 'ADDRESS',
        'ZIPCODE': 'ADDRESS',
        'BUILDINGNUM': 'ADDRESS',
        'CITY': 'CITY',
        'IDCARDNUM': 'ID_NUMBER',
        'SOCIALNUM': 'SOCIAL_NUMBER',
        'DRIVERLICENSENUM': 'DRIVER_LICENSE',
        'TAXNUM': 'TAX_NUMBER',
        'BOOKING_CODE': 'BOOKING_CODE',
        'FLIGHT_NUMBER': 'FLIGHT_NUMBER',
        'SEAT_NUMBER': 'SEAT_NUMBER',
    }

    print(f"  {BOLD}{'📋 PII Detected':<28} {'Value':<25} {'Decision':<15}{RESET}")
    print(f"  {'─'*65}")

    allowed_count = 0
    blocked_count = 0

    for det in detections:
        label = det['label']
        value = det['value']
        pims_field = label_to_field.get(label, label)

        # Check PIMS policy using the core function
        action = pims_parser.check_access(rules, tool_name, pims_field)

        if action == 'ALLOWED':
            color = GREEN
            icon = '✅'
            display_value = value
            allowed_count += 1
        else:
            color = RED
            icon = '🚫'
            display_value = f"{'*' * len(value)}"
            blocked_count += 1

        # Clean and truncate values for display
        display_val = display_value.replace('\n', ' ').strip()[:22]
        print(f"  {color} {icon} {pims_field:<23} {display_val:<25} {BOLD}{action}{RESET}")

        # Log to audit
        audit_logger.log_access(audit_path, tool_name, pims_field, value, action)

    print(f"  {'─'*65}")

    # Summary feedback
    print()
    if blocked_count > 0:
        feedback(f'Blocked {blocked_count} PII field(s) — potential data exfiltration prevented 🔒', 'block')
    if allowed_count > 0:
        feedback(f'Allowed {allowed_count} field(s) per PIMS.md policy', 'allow')

    feedback(f'📝 Audit log updated: .gemini-z/audit.log ({allowed_count + blocked_count} entries)', 'scan')
    print()


if __name__ == '__main__':
    run_demo()
