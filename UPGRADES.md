# GeminiZ Upgrades Beyond Gemini CLI

## What We Added

| Feature           | Gemini CLI             | GeminiZ                                                     |
| ----------------- | ---------------------- | ----------------------------------------------------------- |
| PII Detection     | None                   | Local AI4Privacy model scans all files for personal data    |
| Access Control    | None                   | PIMS.md policy file governs what each tool can see          |
| Audit Trail       | None                   | Every PII access logged with tool, field, timestamp, reason |
| Privacy Skill     | None                   | PII-Awareness skill auto-activates on session start         |
| Live Monitoring   | None                   | PIMS Auditor panel shows real-time access events            |
| Tool Registration | Tools have full access | Tools must declare PII needs or get blocked                 |
| Compliance        | None                   | Out-of-the-box GDPR / EU AI Act compliance via audit logs   |

## New Files

| File                                    | Purpose                                                   |
| --------------------------------------- | --------------------------------------------------------- |
| `PIMS.md`                               | Declarative privacy policy (.gitignore for personal data) |
| `geminiz_core/pims_parser.py`           | Parses PIMS.md into structured access rules               |
| `geminiz_core/audit_logger.py`          | Logs all PII access attempts with reasons                 |
| `geminiz_core/audit_viewer.py`          | Colored audit trail viewer                                |
| `geminiz_core/pims_auditor.py`          | Live tqdm-style monitoring panel                          |
| `examples/booking_flight/demo.py`       | Use case 1: flight check-in with PII governance           |
| `examples/api_keys/demo.py`             | Use case 2: malicious tool blocked from customer data     |
| `.gemini/skills/pii-awareness/SKILL.md` | Gemini CLI skill for auto PII protection                  |

## How It Works

1. User places `PIMS.md` in their project (or home directory)
2. Each tool/skill is registered with allowed and blocked PII fields
3. When a file is read, the AI4Privacy model (running locally) detects PII
4. PIMS.md rules are enforced: allowed fields pass through, blocked fields are
   masked
5. Unregistered tools get zero access (strict mode)
6. Everything is logged to `.gemini-z/audit.log`

## Three Modes

- **strict**: block all PII unless explicitly allowed per tool
- **passive**: allow all but log every access (default)
- **ask**: prompt user for permission on each PII access

## Demo Commands

```bash
# Use case 1: legitimate tool (airline check-in)
python3 examples/booking_flight/demo.py

# Use case 2: malicious/unregistered tool (everything blocked)
python3 examples/api_keys/demo.py

# View audit trail
python3 -m geminiz_core.audit_viewer

# Live monitoring panel
python3 -m geminiz_core.pims_auditor
```
