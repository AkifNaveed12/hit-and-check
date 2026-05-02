# Hit & Check Development Plan

This file is the project execution tracker. Each phase is treated as a module, and each module is broken into trackable tasks.

## Module 1: Foundation

Goal: Build the base repository, Streamlit shell, validation layer, and educational PIN transformation layer.

- T1. Create finalized folder structure and baseline files.
- T2. Configure Streamlit page settings, theme, and navigation layout.
- T3. Add user input form for name, email, demo PIN, encryption method, and attack type.
- T4. Add strict PIN validation: exactly 4 numeric digits.
- T5. Add safety warning that users must not enter real ATM or banking PINs.
- T6. Implement educational transformations:
  - Caesar Digit Shift
  - Digit Substitution Cipher
  - SHA-256 Reduced Demo Hash
- T7. Add unit tests for each transformation.

## Module 2: Attack Simulation

Goal: Simulate brute-force and dictionary-style attacks against the transformed demo PIN.

- T1. Generate all 10,000 numeric PIN candidates from `0000` to `9999`.
- T2. Implement brute-force attack simulation.
- T3. Add common PIN dictionary data source.
- T4. Implement dictionary attack simulation.
- T5. Implement combined attack: dictionary first, then brute-force.
- T6. Track attempts, cracked candidate, elapsed time, and search percentage.
- T7. Add unit tests for attack correctness and attempt counts.

## Module 3: Scoring and Dashboard Analytics

Goal: Convert attack results into meaningful educational security metrics.

- T1. Implement strength score calculation out of 100.
- T2. Implement hack probability calculation out of 100.
- T3. Implement risk levels: Low, Medium, High, Critical.
- T4. Estimate crack time for multiple attacker speeds.
- T5. Build dashboard metric cards.
- T6. Add Plotly charts:
  - attempts vs total combinations
  - cracked position percentage
  - risk score gauge
  - estimated crack-time comparison
- T7. Add tests for scoring boundary cases.

## Module 4: Groq AI Report Integration

Goal: Send strict JSON analysis payloads to Groq and display structured AI reports.

- T1. Define report request JSON contract.
- T2. Define expected Groq response JSON contract.
- T3. Create report prompt that requires strict JSON output.
- T4. Implement Groq API client.
- T5. Add response parsing and fallback handling if the model returns invalid JSON.
- T6. Display report sections in Streamlit.
- T7. Add safe prompt rules: no real PIN exposure, education-only guidance, no harmful instructions.

## Module 5: Groq Chatbot

Goal: Provide an educational security assistant for user questions.

- T1. Define chatbot request JSON contract.
- T2. Create chatbot prompt with safety boundaries.
- T3. Build Streamlit chat interface.
- T4. Pass limited context only: attack type, attempts, risk level, score.
- T5. Prevent asking for or storing sensitive credentials.
- T6. Add fallback response if Groq credentials are missing.
- T7. Add transcript handling within session state only.

## Module 6: Email Report

Goal: Send the user a clean educational report by email.

- T1. Define email formatting rules in `mail.md`.
- T2. Implement report-to-email builder.
- T3. Implement SMTP email service.
- T4. Support Streamlit Cloud secrets and local `.env`.
- T5. Include dashboard link if configured.
- T6. Include safety disclaimer and recommendations.
- T7. Ensure no executable files, payloads, scripts, or harmful links are sent.

## Module 7: Safe Awareness Demo, Testing, and Deployment

Goal: Add a harmless awareness simulation and prepare the app for deployment.

- T1. Implement in-app safe awareness demo.
- T2. Add visible start, stop, and reset controls.
- T3. Show simulated social engineering warnings inside Streamlit only.
- T4. Add test coverage for pure Python modules.
- T5. Add `README.md` setup and deployment instructions.
- T6. Add `.gitignore`, `requirements.txt`, and `.streamlit/config.toml`.
- T7. Run local validation and prepare for Streamlit Community Cloud deployment.

## Current Priority

1. Complete repository scaffold.
2. Complete project documentation source of truth.
3. Implement Module 1.
4. Verify the app runs locally.

