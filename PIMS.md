# PIMS.md — Personal Information Management System

Think of this like `.gitignore`, but for your personal data. Defines what PII
exists, sensitivity levels, and access rules per tool.

## Personal Data Fields

```
NAME                        | high     | Full legal name
LASTNAME                    | high     | Family name
EMAIL                       | medium   | Email address
PHONE_NUMBER                | high     | Phone number
ADDRESS                     | high     | Physical address
PASSPORT_NUMBER             | critical | Passport number
BIRTH_CERTIFICATE           | critical | Birth certificate data
DATE_OF_BIRTH               | high     | Date of birth
CREDIT_CARD_NUMBER          | critical | Credit card number
CREDIT_CARD_EXPIRATION_DATE | critical | Card expiry
CREDIT_CARD_CVV             | critical | Card CVV
BANK_ACCOUNT_NUMBER         | critical | Bank account
BOOKING_CODE                | low      | Flight/hotel booking reference
FLIGHT_NUMBER               | low      | Flight number
SEAT_NUMBER                 | low      | Seat assignment
OPENAI_API_KEY              | critical | OpenAI API key
HF_TOKEN                    | critical | HuggingFace token
REPLIT_API_KEY              | critical | Replit API key
GCP_API_KEY                 | critical | Google Cloud API key
GEMINI_API_KEY              | critical | Gemini API key
```

## Access Rules

```
airline-checkin | BOOKING_CODE, FLIGHT_NUMBER, SEAT_NUMBER, NAME, EMAIL, PHONE_NUMBER, DATE | PASSPORT_NUMBER, CREDIT_CARD_NUMBER, ADDRESS
replit-deploy | REPLIT_API_KEY | OPENAI_API_KEY, HF_TOKEN, GCP_API_KEY, GEMINI_API_KEY
gemini-cli | NAME, EMAIL | CREDIT_CARD_NUMBER, PASSPORT_NUMBER, BANK_ACCOUNT_NUMBER
```

## Modes

- `strict` — block all PII unless explicitly allowed per tool
- `passive` — allow all but log every access (default)
- `ask` — prompt user for permission on each PII access

```
MODE: passive
```

## Audit

All PII access attempts are logged to `.gemini-z/audit.log`

Format: `timestamp | tool | field | action (ALLOWED/BLOCKED/USER_APPROVED)`
