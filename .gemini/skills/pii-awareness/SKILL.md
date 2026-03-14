---
name: PII-Awareness
description: A skill that prevents the model from revealing personally identifiable information (PII) such as names, lastnames, addresses, or sensitive environment variables like `OPENAI_API_KEY` by using placeholders and reading files with (local) privacy anonymizers. Activate this skill BEFORE reading any file that may contain personal data.
---

## CRITICAL INSTRUCTIONS

When this skill is active, you MUST follow these rules for EVERY file you read:

### Step 1: Read PIMS.md
Before displaying ANY file content, read `PIMS.md` from the project root to load the access rules.

### Step 2: Identify the context
Determine what "tool" or "task" is requesting the data. Examples:
- User asks to check in for a flight = `airline-checkin`
- User asks to deploy code = `replit-deploy`
- User asks to read a customer complaint = `support-ticket`
- Unknown or unspecified context = `unknown-tool` (block everything)

### Step 3: Scan for PII
When you read a file, identify ALL personal information:
- **Names**: first name, last name, full name
- **Contact**: email, phone number, address, city, zip code
- **Documents**: passport number, ID number, driver license, birth certificate, date of birth
- **Financial**: credit card number, bank account, CVV, expiry date
- **Credentials**: API keys (sk-..., hf_..., repl_key_...), tokens, passwords
- **Tax/Social**: tax ID, social security number

### Step 4: Apply PIMS.md rules
Check the Access Rules section in PIMS.md:
- If the field is in the tool's **allowed** list: show the value normally
- If the field is in the tool's **blocked** list: replace with `[REDACTED_FIELDNAME]`
- If the tool is NOT registered in PIMS.md: redact ALL PII fields

### Step 5: Display with governance table
After reading the file, ALWAYS display a PII governance summary like this:

```
🛡️ [GEMINI Z] PII Governance Report
─────────────────────────────────────────
Tool: airline-checkin
Mode: passive

✅ NAME           Michael Zurigo     ALLOWED (declared by tool)
✅ BOOKING_CODE   GZ-2026-PAR        ALLOWED (declared by tool)
✅ EMAIL          michael@ai4p...    ALLOWED (declared by tool)
🚫 PASSPORT      [REDACTED]         BLOCKED (not in tool scope)
🚫 CREDIT_CARD   [REDACTED]         BLOCKED (not in tool scope)
🚫 ADDRESS        [REDACTED]         BLOCKED (not in tool scope)
─────────────────────────────────────────
Allowed: 3 | Blocked: 3
```

### Step 6: Write audit log
After displaying the governance report, run this command to log the access:
```bash
python3 -c "
import sys; sys.path.insert(0, '.');
from geminiz_core.audit_logger import log_access;
log_access('.gemini-z/audit.log', 'TOOL_NAME', 'FIELD_NAME', 'VALUE', 'ACTION', 'REASON')
"
```
Run one command per PII field detected. Replace TOOL_NAME, FIELD_NAME, VALUE, ACTION, and REASON with actual values.

### Step 7: Never leak blocked PII
In your response text, NEVER write out the actual value of blocked fields. Always use `[REDACTED]` or `[REDACTED_FIELDNAME]`. This applies to:
- Your summary text
- Any quotes from the file
- Any actions you describe taking

## Example Interaction

User: "Read my flight ticket at examples/booking_flight/flight_ticket.txt and check in for me"

You should:
1. Activate this skill (already done)
2. Read PIMS.md
3. Read the flight ticket
4. Identify context: `airline-checkin`
5. Scan for PII in the ticket
6. Apply PIMS.md rules for `airline-checkin`
7. Display governance table showing allowed/blocked fields
8. Write audit log entries
9. Respond with: "Your check-in is complete. Booking GZ-2026-PAR, flight LX 1234, seat 12A. Your passport number and credit card were redacted per PIMS.md policy."

## Example: Unknown Tool

User: "Analyze this customer complaint file"

If no tool is registered for this context:
1. Read PIMS.md
2. Read the file
3. Context: `unknown-tool` (not in PIMS.md)
4. ALL PII is BLOCKED
5. Display governance table with everything redacted
6. Respond using only redacted values
