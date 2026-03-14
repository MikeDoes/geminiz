"""
PIMS.md Parser — Reads Personal Information Management System rules.
Parses the PIMS.md file to extract field definitions and per-tool access rules.
"""

import re


def parse_pims(pims_path):
    """Parse a PIMS.md file and return structured rules."""
    with open(pims_path, 'r') as f:
        content = f.read()

    rules = {
        'fields': {},
        'tools': {},
        'mode': 'passive',
    }

    # Parse field definitions: FIELD_NAME | sensitivity | description
    field_pattern = re.compile(
        r'^([A-Z_]+)\s*\|\s*(low|medium|high|critical)\s*\|\s*(.+)$',
        re.MULTILINE
    )
    for match in field_pattern.finditer(content):
        rules['fields'][match.group(1).strip()] = {
            'sensitivity': match.group(2).strip(),
            'description': match.group(3).strip(),
        }

    # Parse access rules sections
    # Look for tool name followed by allowed | blocked
    tool_pattern = re.compile(
        r'^([a-z][\w-]+)\s*\|\s*([^|]+)\|\s*(.+)$',
        re.MULTILINE
    )
    for match in tool_pattern.finditer(content):
        tool_name = match.group(1).strip()
        allowed = [f.strip() for f in match.group(2).split(',')]
        blocked = [f.strip() for f in match.group(3).split(',')]
        rules['tools'][tool_name] = {
            'allowed': allowed,
            'blocked': blocked,
        }

    # Parse mode
    mode_match = re.search(r'^MODE:\s*(\w+)', content, re.MULTILINE)
    if mode_match:
        rules['mode'] = mode_match.group(1).strip()

    return rules


def check_access(rules, tool_name, field_name):
    """Check if a tool is allowed to access a field.

    Returns: 'ALLOWED', 'BLOCKED', or 'ASK'
    """
    mode = rules.get('mode', 'passive')
    tool_rules = rules.get('tools', {}).get(tool_name, {})

    allowed = tool_rules.get('allowed', [])
    blocked = tool_rules.get('blocked', [])

    if field_name in blocked:
        return 'BLOCKED'
    elif field_name in allowed:
        return 'ALLOWED'
    elif mode == 'strict':
        return 'BLOCKED'
    elif mode == 'ask':
        return 'ASK'
    else:  # passive
        return 'ALLOWED'
