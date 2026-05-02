# Hit & Check UI/UX Design Specification

This file defines Streamlit UI/UX rules for the project.

## Design Goals

- The app should feel like a professional cybersecurity education dashboard.
- The first screen should be the usable app, not a marketing landing page.
- The interface should be clear, compact, and easy to scan.
- The app should avoid fear-based language except inside clearly labeled safety simulations.
- The UI should make it obvious that this is an educational simulator.

## Layout

- Use Streamlit wide layout.
- Use a left sidebar for configuration and inputs.
- Use the main area for dashboard results, charts, AI report, chatbot, and awareness demo.
- Use tabs in the main area:
  - Dashboard
  - AI Report
  - Security Assistant
  - Email Report
  - Awareness Demo
- Avoid deeply nested cards.
- Use metric cards only for key dashboard values.
- Use clear section headers.

## Typography

- Use Streamlit default font stack unless a custom theme is added later.
- Headings should be short and descriptive.
- Avoid oversized text inside dashboard panels.
- Use concise labels:
  - `Strength Score`
  - `Hack Probability`
  - `Risk Level`
  - `Attempts`
  - `Estimated Crack Time`

## Colors

- Base style should be clean and neutral.
- Primary accent should be a security-themed blue.
- Risk colors:
  - Low: green
  - Medium: amber
  - High: orange
  - Critical: red
- Avoid using a single color family across the entire app.
- Avoid heavy gradients, decorative blobs, and distracting backgrounds.

## Buttons

- Primary action:
  - `Run Analysis`
  - full-width in sidebar
  - primary button style
- Secondary actions:
  - `Generate AI Report`
  - `Get Report on Email`
  - `Run Safe Awareness Demo`
- Destructive or reset action:
  - `Reset Demo`
  - visually secondary
- Stop action:
  - `Stop Demo`
  - visually distinct and clearly labeled

## Inputs

- PIN input must use password-style masking where possible.
- PIN field must limit the user to 4 digits through validation.
- Email is optional until the user sends a report.
- Algorithm and attack type should use dropdown/selectbox controls.
- Safety acknowledgement should use a checkbox before running analysis.

## Dashboard

- Show only the transformed demo PIN, never overemphasize the original PIN.
- Display metrics in a row:
  - Attempts to Crack
  - Strength Score
  - Hack Probability
  - Risk Level
- Display charts below metrics.
- Provide local recommendations even if Groq is unavailable.

## AI Report

- Display AI output in structured sections.
- Do not display raw JSON by default.
- Provide an expandable raw JSON viewer for debugging only.
- If Groq is unavailable, show a local fallback report.

## Chatbot

- Chatbot should answer only security-awareness questions.
- It must not ask for real passwords, bank PINs, OTPs, or recovery codes.
- It should keep answers practical and brief.
- It should explain when a request is unsafe.

## Awareness Demo

- The demo must run only inside Streamlit.
- It must be clearly labeled as a safe simulation.
- It must include a visible stop/reset control.
- It must not open external windows, modify files, download files, execute scripts, or send unexpected emails.

## Accessibility

- Use clear labels for all inputs.
- Avoid relying only on color to explain risk.
- Keep contrast readable.
- Use concise error messages.

## Responsive Behavior

- Dashboard should remain usable on laptop screens.
- Columns should collapse gracefully on smaller screens.
- Avoid long unbroken strings in visible UI.

