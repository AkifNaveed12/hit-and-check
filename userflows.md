# Hit & Check User Flows

## Flow 1: First App Visit

1. User opens the Streamlit app.
2. App shows the title, project description, and safety notice.
3. App warns the user not to enter a real ATM or banking PIN.
4. User continues to the demo input form.

## Flow 2: PIN Analysis

1. User enters name.
2. User optionally enters email.
3. User enters a demo 4-digit numeric PIN.
4. User selects an educational transformation algorithm:
   - Caesar Digit Shift
   - Digit Substitution Cipher
   - SHA-256 Reduced Demo Hash
5. User selects attack type:
   - Brute Force
   - Dictionary Attack
   - Combined Attack
6. User clicks `Run Analysis`.
7. App validates input.
8. App transforms the demo PIN.
9. App runs the selected attack simulation.
10. App records attempts, elapsed time, cracked candidate, and search percentage.
11. App calculates risk score, strength score, hack probability, and estimated crack times.
12. App displays the dashboard.

## Flow 3: Dashboard Review

1. User views the encrypted/transformed demo PIN.
2. User views total attempts needed to crack the transformed PIN.
3. User views score cards:
   - Strength Score
   - Hack Probability
   - Risk Level
   - Estimated Crack Time
4. User views charts:
   - Attempts vs total combinations
   - Risk gauge
   - Search space progress
   - Crack-time comparison
5. User reads basic local recommendations.

## Flow 4: AI Report

1. User clicks `Generate AI Report`.
2. App builds the strict report request JSON.
3. App sends the request to Groq.
4. Groq returns strict JSON.
5. App parses the JSON.
6. App displays:
   - summary
   - strength score
   - risk level
   - attack explanation
   - key findings
   - recommendations
   - educational note
7. If Groq is unavailable, app displays a local fallback report.

## Flow 5: Chatbot

1. User opens the security assistant panel.
2. User asks a security-awareness question.
3. App builds a chatbot JSON payload using limited context.
4. App sends the question to Groq.
5. Assistant answers in an educational, non-sensitive way.
6. Assistant refuses to collect real credentials or provide harmful instructions.

## Flow 6: Email Report

1. User enters an email address.
2. User clicks `Get Report on Email`.
3. App validates email format.
4. App builds an HTML/plain-text report.
5. App sends the email through configured SMTP credentials.
6. User receives the educational report.
7. Email contains no executable attachment, no payload, and no hidden script.

## Flow 7: Safe Awareness Demo

1. User clicks `Run Safe Attack Awareness Demo`.
2. App displays simulated social engineering warning messages inside Streamlit.
3. App explains how scare tactics and phishing prompts work.
4. User can click `Stop Demo` or `Reset Demo`.
5. No file is created, modified, downloaded, executed, or persisted.

