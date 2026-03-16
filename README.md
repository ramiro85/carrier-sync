# CarrierSync—Integration Utility API 

> REST API that integrates external transportation services for carrier lookup, debtor data, Gmail workflows, and ELD driver operations.
## Overview

**Integration Utility API** is a FastAPI service that centralizes external integrations used by transportation operations. It exposes a unified interface for broker verification, debtor lookup, email automation, and ELD driver management.

---

## Features

- **SAFER Carrier Lookup** — Query FMCSA SAFER data for carrier verification.
- **TAFS Debtor Lookup** — Retrieve debtor information from TAFS.
- **Gmail Workflows** — Send, search, manage attachments, and handle contacts via Google service accounts.
- **ELD Driver Operations** — Full CRUD and activation/deactivation of ELD drivers.

---
---

## Tech Stack

| Layer           | Technology               |
|-----------------|--------------------------|
| Language        | Python 3.12+             |
| Framework       | FastAPI                  |
| Validation      | Pydantic v2              |
| HTTP / Scraping | Requests + BeautifulSoup |
| Testing         | Pytest                   |

---

## Project Structure

```
app/
├── main.py                  # App entrypoint
├── core/                    # Shared models, routers, and utilities
└── services/
    ├── safer/               # SAFER integration
    ├── tafs/                # TAFS integration
    ├── googleCloud/         # Gmail integration
    └── eld/                 # ELD authentication and driver operations
tests/                       # Unit and API tests
docs/
└── API_METHODS.md           # Full method reference
```

---

## Local Setup
```bash

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

API base URL: `http://localhost:8000`

---


## Configuration

All configuration is environment-driven. The `.env` file is for **local development only**.

- **Never commit secrets or `.env` to version control.**
- All required keys are documented in `.env.example` with placeholder values.

---

## API Docs

| Interface        | URL                           |
|------------------|-------------------------------|
| Swagger UI       | `http://localhost:8000/docs`  |
| ReDoc            | `http://localhost:8000/redoc` |
| Method Reference | `docs/API_METHODS.md`         |

---

## Gmail Workflows (Service Account)

Gmail integration runs via a **Google service account** with domain-wide delegation — no user OAuth flow is required.

### Supported Operations

| Operation | Description |
|---|---|
| **Send** | Send emails on behalf of a delegated user |
| **Search** | Query the mailbox using Gmail search syntax |
| **Attachments** | Upload, download, and manage email attachments |
| **Contacts** | Read and manage Google Contacts for a delegated user |

### Service Account Setup

1. Create a service account in [Google Cloud Console](https://console.cloud.google.com).
2. Enable the **Gmail API** under *APIs & Services → Library*.
3. Grant **domain-wide delegation** to the service account in the Google Workspace Admin Console.
4. Assign the following OAuth scopes in the Admin Console under *Security → API Controls → Domain-wide Delegation*:
```
https://www.googleapis.com/auth/gmail.send
https://www.googleapis.com/auth/gmail.readonly
https://www.googleapis.com/auth/gmail.modify
https://www.googleapis.com/auth/contacts
```
5. Download the service account key JSON and set the path in your `.env`:

### Common Errors

| Error | Cause | Fix |
|---|---|---|
| `failedPrecondition` / `Mail service not enabled` | Gmail disabled for the account or Workspace OU | Enable Gmail in Google Admin Console → Apps → Google Workspace → Gmail |
| `Precondition check failed` | Account has never logged into Gmail or ToS not accepted | Sign into [mail.google.com](https://mail.google.com) with the account once |
| `insufficientPermissions` | Missing OAuth scope | Add required scopes in Admin Console domain-wide delegation settings |
| `invalid_grant` | Stale or revoked token | Regenerate the service account key and update `.env` |

---
## Testing

```bash

pytest -q
```

---
## Publish Checklist

Before pushing to any remote repository:
- [ ] `.env` is listed in `.gitignore` and not tracked by git
- [ ] `.env.example` contains only placeholder values (no real secrets)
- [ ] No personal emails, usernames, or passwords exist in tests or fixtures
- [ ] All tests pass locally (`pytest -q`)
- [ ] Service account key files are excluded from version control