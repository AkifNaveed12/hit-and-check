# Hit & Check

Hit & Check is a Streamlit-based cybersecurity awareness app that demonstrates how 4-digit numeric demo PINs can be tested through brute-force and dictionary-style simulations.

The app is educational. Do not enter real ATM, banking, account, recovery, or personal PINs.

## Features

- Streamlit dashboard
- 4-digit demo PIN validation
- Educational numeric transformations
- Brute-force simulation
- Dictionary attack simulation
- Combined attack simulation
- Strength scoring and risk metrics
- Groq-powered AI report with local fallback
- Groq-powered chatbot with local fallback
- Email report support
- Safe in-app awareness demo

## Safety Scope

This project does not include malware, hidden payloads, auto-running email links, persistence, evasion, destructive behavior, or system-level popups.

The awareness demo runs only inside Streamlit and is user-triggered.

## Tech Stack

- Python
- Streamlit
- Groq API
- Pandas
- Plotly
- SMTP email
- Pytest

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy sample.env .env
```

Fill `.env` with your own keys. Do not commit `.env`.

## Environment Variables

```text
GROQ_API_KEY=
GROQ_MODEL=llama-3.1-8b-instant
SMTP_HOST=
SMTP_PORT=587
SMTP_USERNAME=
SMTP_PASSWORD=
SMTP_FROM_EMAIL=
SMTP_FROM_NAME=Hit & Check
APP_PUBLIC_URL=
ENABLE_EMAIL=true
ENABLE_GROQ=true
```

For Streamlit Cloud, configure these values in Streamlit secrets instead of `.env`.

## Run Locally

```bash
streamlit run app.py
```

## Project Documents

- `planning.md`: module and task tracker
- `context.md`: implementation context log
- `userflows.md`: complete user flows
- `architecture.md`: Mermaid architecture diagrams
- `design.d`: Streamlit UI/UX rules
- `mail.md`: email formatting and `.env` requirements

## Folder Structure

```text
hit-and-check/
|-- app.py
|-- requirements.txt
|-- README.md
|-- .gitignore
|-- sample.env
|-- planning.md
|-- context.md
|-- userflows.md
|-- architecture.md
|-- design.d
|-- mail.md
|-- .streamlit/
|   `-- config.toml
|-- src/
|   |-- __init__.py
|   |-- config.py
|   |-- validators.py
|   |-- encryption.py
|   |-- attacks.py
|   |-- scoring.py
|   |-- groq_client.py
|   |-- email_service.py
|   |-- report_builder.py
|   `-- awareness_demo.py
|-- data/
|   `-- common_pins.json
|-- prompts/
|   |-- pin_report_prompt.txt
|   `-- chatbot_prompt.txt
|-- assets/
`-- tests/
    |-- test_encryption.py
    |-- test_attacks.py
    `-- test_scoring.py
```
