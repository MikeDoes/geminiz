---
name: PII-Awareness
description: A skill that prevents the model from revealing personally identifiable information (PII) such as names, lastnames, addresses, or sensitive environment variables like `OPENAI_API_KEY` by using placeholders and reading files with (local) privacy anonymizers.
---

## How It Works

Gemini Z uses a **PIMS.md** (Personal Information Management System) file — like `.gitignore` but for personal data — to govern what PII each tool can access.

### 1. PII Detection
When a tool or skill reads a file, Gemini Z runs a **local** open-source PII detection model (e.g. `ai4privacy/llama-ai4privacy-multilingual-categorical-anonymiser-openpii` from HuggingFace) to identify personal information. Supported PII types include:
- Names (GIVENNAME, SURNAME)
- Contact info (EMAIL, PHONE_NUMBER, ADDRESS)
- Documents (PASSPORT_NUMBER, BIRTH_CERTIFICATE)
- Financial (CREDIT_CARD_NUMBER, BANK_ACCOUNT_NUMBER)
- Credentials (API keys, tokens)

**Your data never leaves your machine.** The model runs locally.

### 2. Policy Enforcement (PIMS.md)
Each tool must declare what PII it needs. PIMS.md defines:
- **Allowed fields** per tool (e.g. airline check-in can see BOOKING_CODE)
- **Blocked fields** per tool (e.g. airline check-in cannot see BIRTH_CERTIFICATE)
- **Sensitivity levels** (low, medium, high, critical)

If a tool requests data it hasn't declared or isn't allowed → **request is blocked**.

### 3. Modes
- **strict** — block all PII unless explicitly allowed per tool
- **passive** — allow all but log every access (default)
- **ask** — prompt user for permission on each PII access

### 4. Audit Trail
Every PII access is logged to `.gemini-z/audit.log`:
```
2026-03-14T14:32:01Z | airline-checkin | BOOKING_CODE | ALLOWED
2026-03-14T14:32:01Z | airline-checkin | BIRTH_CERTIFICATE | BLOCKED
2026-03-14T14:32:05Z | replit-deploy | REPLIT_API_KEY | ALLOWED
2026-03-14T14:32:05Z | replit-deploy | HF_TOKEN | BLOCKED
```

Not just to protect you — but to **prove it** to your clients, your team, your regulators.

## Usage

1. Place a `PIMS.md` file in your project root or home directory
2. Install the PII-Awareness skill
3. Tools and skills will be governed by PIMS.md rules automatically
4. Run `gemini-z audit` to view the full access log

## Compatibility
- Gemini CLI
- Antigravity
- Gemini App (browser)
- Mobile (on-device models)
