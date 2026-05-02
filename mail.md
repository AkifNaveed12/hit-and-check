# Hit & Check Email Report Specification

This file defines email report formatting, content rules, and required environment variables.

## Email Purpose

The email report provides the user with the same educational analysis shown in the dashboard. It must not contain malware, executable attachments, hidden scripts, or surprise behavior.

## Email Subject

Recommended format:

```text
Hit & Check Security Awareness Report for {user_name}
```

Fallback:

```text
Your Hit & Check Security Awareness Report
```

## Email Structure

1. Greeting
2. Short safety disclaimer
3. Analysis summary
4. Key metrics
5. Risk explanation
6. Recommendations
7. Dashboard link if configured
8. Educational note
9. Footer

## Required Email Content

- User name
- Transformation algorithm
- Attack type
- Attempts to crack
- Total possible combinations
- Strength score
- Hack probability
- Risk level
- Estimated crack time
- Recommendations

## Prohibited Email Content

- Original demo PIN
- Real PINs or passwords
- Executable attachments
- Macros
- Tracking payloads
- Hidden JavaScript
- Auto-running links or files
- Code that creates popups or modifies a user's system

## HTML Style Rules

- Use simple responsive HTML.
- Use a max content width of around 640px.
- Use readable font stack: Arial, Helvetica, sans-serif.
- Use neutral background and white content panel.
- Use risk badges:
  - Low: green
  - Medium: amber
  - High: orange
  - Critical: red
- Use plain text fallback.

## Environment Variables

For local development, create a `.env` file using `sample.env` as the template.

Required for Groq:

```text
GROQ_API_KEY=
GROQ_MODEL=llama-3.1-8b-instant
```

Required for email:

```text
SMTP_HOST=
SMTP_PORT=587
SMTP_USERNAME=
SMTP_PASSWORD=
SMTP_FROM_EMAIL=
SMTP_FROM_NAME=Hit & Check
```

Optional:

```text
APP_PUBLIC_URL=
ENABLE_EMAIL=true
ENABLE_GROQ=true
```

## Streamlit Cloud Secrets

For Streamlit deployment, configure secrets in Streamlit Cloud instead of committing `.env`.

Example:

```toml
GROQ_API_KEY = "your_key_here"
GROQ_MODEL = "llama-3.1-8b-instant"

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = "your_email@gmail.com"
SMTP_PASSWORD = "your_app_password"
SMTP_FROM_EMAIL = "your_email@gmail.com"
SMTP_FROM_NAME = "Hit & Check"

APP_PUBLIC_URL = "https://your-app.streamlit.app"
ENABLE_EMAIL = true
ENABLE_GROQ = true
```

## Gmail Note

If using Gmail SMTP, use a Gmail App Password. Do not use your normal Gmail password.

