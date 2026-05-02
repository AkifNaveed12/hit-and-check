# Hit & Check Context Log

This file records project decisions, file changes, functions, and logic updates as development progresses.

## 2026-05-03: Initial Project Scaffold

### Project Decision

- The app will be built as a safe cybersecurity education simulator.
- Users must not enter real ATM or banking PINs.
- The app will simulate brute-force and dictionary attacks only against user-provided demo PINs.
- The project will not include malware, hidden payloads, email-triggered execution, persistence, evasion, or destructive behavior.
- The unsafe email-triggered "virus" idea has been replaced with a harmless in-app awareness demo.

### Files Added

- `planning.md`
  - Added seven module-based development phases.
  - Added task IDs `T1`, `T2`, `T3`, etc. for tracking.

- `context.md`
  - Added this context log.
  - Added initial safety and implementation decisions.

### Folder Structure Added

- `.streamlit/`
- `src/`
- `data/`
- `prompts/`
- `assets/`
- `tests/`
- `docs/`

### Pending Implementation

- Full implementation polish and deployment validation.

### Source Files Added

- `app.py`
  - Added Streamlit page setup, sidebar form, analysis orchestration, dashboard tab, AI report tab, chatbot tab, email tab, and awareness demo tab.
  - Functions added:
    - `initialize_state`
    - `render_sidebar`
    - `run_analysis`
    - `render_dashboard`
    - `render_ai_report`
    - `render_chatbot`
    - `render_email_tab`
    - `main`

- `src/config.py`
  - Added app constants for encryption methods and attack types.
  - Added `Settings` dataclass.
  - Added `get_settings` to load values from Streamlit secrets or environment variables.
  - Added guarded `python-dotenv` loading for local `.env` support.

- `src/validators.py`
  - Added `validate_pin` for strict 4-digit numeric PIN validation.
  - Added `validate_email` for optional or required email validation.

- `src/encryption.py`
  - Added `caesar_digit_shift`.
  - Added `digit_substitution_cipher`.
  - Added `sha256_reduced_hash`.
  - Added `transform_pin` dispatcher.

- `src/attacks.py`
  - Added PIN-space generation from `0000` to `9999`.
  - Added common PIN loading from `data/common_pins.json`.
  - Added `brute_force_attack`, `dictionary_attack`, `combined_attack`, and `run_attack`.
  - Attack results record attempts, cracked status, cracked candidate, elapsed time, and crack position percentage.

- `src/scoring.py`
  - Added risk-level mapping.
  - Added crack-time formatting and estimate helpers.
  - Added `build_score_result`.

- `src/report_builder.py`
  - Added strict JSON report payload builder.
  - Added chatbot payload builder.
  - Added email report builder with text and HTML output.

- `src/groq_client.py`
  - Added Groq report generation with local fallback.
  - Added Groq chatbot generation with local fallback.
  - Added safe system instructions.

- `src/email_service.py`
  - Added SMTP email sending.
  - Added missing-settings checks and error responses.

- `src/awareness_demo.py`
  - Added safe in-app awareness demo.
  - Demo displays warnings only inside Streamlit and does not modify system state.

### Data and Prompt Files Added

- `data/common_pins.json`
  - Added initial common PIN dictionary for educational dictionary attack simulation.

- `prompts/pin_report_prompt.txt`
  - Added strict JSON report prompt and safety rules.

- `prompts/chatbot_prompt.txt`
  - Added security-awareness chatbot behavior rules.

### Project Support Files Added

- `requirements.txt`
  - Added Streamlit, Pandas, Plotly, Groq, python-dotenv, and pytest dependencies.

- `README.md`
  - Added project overview, setup, safety scope, environment variables, run command, and folder structure.

- `.gitignore`
  - Added environment, virtualenv, cache, and Streamlit secrets exclusions.

- `sample.env`
  - Added local environment variable template.

- `.streamlit/config.toml`
  - Added baseline Streamlit theme and headless server setting.

### Tests Added

- `tests/test_encryption.py`
  - Added tests for Caesar shift, substitution, SHA-256 reduced hash, and transform dispatcher.

- `tests/test_attacks.py`
  - Added tests for brute-force, dictionary, and combined attack paths.

- `tests/test_scoring.py`
  - Added tests for risk levels, time formatting, and score result.

### Verification

- Ran `python -m compileall .` from the nested `hit-and-check` repository.
  - Result: source modules and tests compiled successfully.
- Ran `python -m py_compile app.py`.
  - Result: `app.py` compiled successfully.
- Attempted `pytest -q`.
  - Result: not available in the current environment because `pytest` is not installed yet.
  - Next step: install dependencies with `pip install -r requirements.txt`, then run `pytest -q`.

## 2026-05-03: Test Import Configuration

### Files Added

- `pytest.ini`
  - Added `pythonpath = .` so tests can import the local `src` package when `pytest -q` is run from the repository root.
  - Added `testpaths = tests` so pytest only collects the intended test folder.
