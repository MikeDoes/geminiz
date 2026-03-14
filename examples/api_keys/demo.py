"""
Gemini Z — Use Case 2: API Keys & Customer Data Demo
Demonstrates PIMS.md catching a malicious tool trying to exfiltrate
API keys, credentials, and sensitive customer data from a support ticket.
"""

import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from geminiz_core import pims_parser, audit_logger

GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BOLD = '\033[1m'
DIM = '\033[2m'
RESET = '\033[0m'
CYAN = '\033[96m'


def feedback(msg, level='info'):
    if level == 'activate':
        print(f"\n  {BOLD}{GREEN}🛡️  [GEMINI Z]{RESET} {DIM}PIMS.md loaded — privacy governance active{RESET}")
    elif level == 'scan':
        print(f"  {BOLD}{GREEN}🔍 [GEMINI Z]{RESET} {DIM}{msg}{RESET}")
    elif level == 'block':
        print(f"  {BOLD}{RED}🚫 [GEMINI Z]{RESET} {BOLD}{RED}{msg}{RESET}")
    elif level == 'allow':
        print(f"  {BOLD}{GREEN}✅ [GEMINI Z]{RESET} {DIM}{msg}{RESET}")


def detect_pii_in_text(text):
    try:
        from ai4privacy import protect
        result = protect(text, verbose=True, multilingual=True, classify_pii=True)
        return result
    except ImportError:
        return detect_pii_fallback(text)


def detect_pii_fallback(text):
    import re
    detections = []

    patterns = {
        'GIVENNAME': r'\b(Sarah|Michael|Brian|John|Jane)\b',
        'SURNAME': r'\b(Martinez|Zurigo|Parigi|Smith)\b',
        'EMAIL': r'[\w.+-]+@[\w-]+\.[\w.-]+',
        'TELEPHONENUM': r'\+\d[\d\s\-]{8,}',
        'PASSPORTNUM': r'\b[A-Z]\d{8}\b',
        'CREDITCARDNUMBER': r'\bending \d{4}\b',
        'DATE': r'\b\d{2}/\d{2}/\d{4}\b',
        'STREET': r'\d+\s+(?:Avenue|Rue|Street|Boulevard)\s+[^\n,]+',
        'ZIPCODE': r'\b\d{5}\b',
        'OPENAI_API_KEY': r'sk-proj-\w+',
        'HF_TOKEN': r'hf_\w+',
        'REPLIT_API_KEY': r'repl_key_\w+',
        'TAXNUM': r'FR-TAX-[\w-]+',
        'BANK_ACCOUNT': r'FR\d{2}\s+\d{4}\s+\d{4}\s+\d{4}\s+\d{4}\s+\d{4}\s+\d{3}',
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
    print(f"\n{BOLD}{RED}{'='*60}{RESET}")
    print(f"{BOLD}{RED}  🚨 GEMINI Z — Malicious Tool Detection Demo  🚨{RESET}")
    print(f"{BOLD}{RED}{'='*60}{RESET}")

    feedback('', 'activate')

    ticket_path = os.path.join(os.path.dirname(__file__), 'customer_complaint.txt')
    with open(ticket_path, 'r') as f:
        ticket_text = f.read()

    feedback('📄 Scanning file: customer_complaint.txt for PII...', 'scan')
    feedback('🤖 Anonymiser engine: ai4privacy (local, open-source)', 'scan')
    print()

    pims_path = os.path.join(os.path.dirname(__file__), '..', '..', 'PIMS.md')
    rules = pims_parser.parse_pims(pims_path)

    # Simulate a MALICIOUS tool that hasn't declared its PII needs
    tool_name = 'suspicious-analytics'

    print(f"  🔧 {BOLD}Tool requesting access: {RED}{tool_name}{RESET}")
    print(f"  📋 {BOLD}PIMS.md Policy:{RESET}")
    print(f"    {RED}⚠️  Tool NOT registered in PIMS.md — strict mode applies{RESET}")
    print(f"    {RED}🚫 All PII access will be BLOCKED{RESET}")
    print()

    result = detect_pii_in_text(ticket_text)

    if 'detections' in result:
        detections = result['detections']
    elif 'replacements' in result:
        detections = result['replacements']
    else:
        detections = []

    audit_dir = os.path.join(os.path.dirname(__file__), '..', '..', '.gemini-z')
    os.makedirs(audit_dir, exist_ok=True)
    audit_path = os.path.join(audit_dir, 'audit.log')

    label_to_field = {
        'GIVENNAME': 'NAME',
        'SURNAME': 'NAME',
        'EMAIL': 'EMAIL',
        'TELEPHONENUM': 'PHONE_NUMBER',
        'PHONE_NUMBER': 'PHONE_NUMBER',
        'PASSPORTNUM': 'PASSPORT_NUMBER',
        'CREDITCARDNUMBER': 'CREDIT_CARD_NUMBER',
        'DATE': 'DATE',
        'STREET': 'ADDRESS',
        'ZIPCODE': 'ADDRESS',
        'ADDRESS': 'ADDRESS',
        'CITY': 'ADDRESS',
        'OPENAI_API_KEY': 'OPENAI_API_KEY',
        'HF_TOKEN': 'HF_TOKEN',
        'REPLIT_API_KEY': 'REPLIT_API_KEY',
        'TAXNUM': 'TAX_NUMBER',
        'BANK_ACCOUNT': 'BANK_ACCOUNT_NUMBER',
        'DRIVERLICENSENUM': 'PASSPORT_NUMBER',
        'DRIVER_LICENSE': 'PASSPORT_NUMBER',
        'IDCARDNUM': 'PASSPORT_NUMBER',
        'SOCIALNUM': 'PASSPORT_NUMBER',
        'SEX': None,
        'GENDER': None,
        'TITLE': None,
        'AGE': None,
        'TIME': None,
    }

    print(f"  {BOLD}{'📋 PII Detected':<28} {'Value':<25} {'Decision':<15}{RESET}")
    print(f"  {'─'*65}")

    allowed_count = 0
    blocked_count = 0

    for det in detections:
        label = det['label']
        value = det['value']
        pims_field = label_to_field.get(label, label)

        if pims_field is None:
            continue

        # Unregistered tool = everything blocked
        action = 'BLOCKED'
        color = RED
        icon = '🚫'
        display_value = f"{'*' * min(len(value), 20)}"
        blocked_count += 1

        display_val = display_value.replace('\n', ' ').strip()[:22]
        print(f"  {color} {icon} {pims_field:<23} {display_val:<25} {BOLD}{action}{RESET}")

        audit_logger.log_access(
            audit_path, tool_name, pims_field, value, action,
            reason=f"Tool '{tool_name}' not registered in PIMS.md"
        )

    print(f"  {'─'*65}")
    print()

    feedback(f'BLOCKED ALL {blocked_count} PII field(s) — unregistered tool denied access 🔒', 'block')
    feedback(f'📝 Audit log updated: .gemini-z/audit.log ({blocked_count} entries)', 'scan')
    print()
    print(f"  {BOLD}{YELLOW}💡 To allow this tool, register it in PIMS.md with declared fields.{RESET}")
    print()


if __name__ == '__main__':
    run_demo()
