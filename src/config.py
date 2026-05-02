import os
from dataclasses import dataclass

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover
    load_dotenv = None

try:
    import streamlit as st
except ImportError:  # pragma: no cover
    st = None

if load_dotenv is not None:
    load_dotenv()


APP_NAME = "Hit & Check"

ENCRYPTION_METHODS = [
    "Caesar Digit Shift",
    "Digit Substitution Cipher",
    "SHA-256 Reduced Demo Hash",
]

ATTACK_TYPES = [
    "Brute Force",
    "Dictionary Attack",
    "Combined Attack",
]


@dataclass(frozen=True)
class Settings:
    groq_api_key: str = ""
    groq_model: str = "llama-3.1-8b-instant"
    smtp_host: str = ""
    smtp_port: int = 587
    smtp_username: str = ""
    smtp_password: str = ""
    smtp_from_email: str = ""
    smtp_from_name: str = APP_NAME
    app_public_url: str = ""
    enable_email: bool = True
    enable_groq: bool = True


def _read_secret(name: str, default: str = "") -> str:
    if st is not None:
        try:
            value = st.secrets.get(name)
            if value is not None:
                return str(value)
        except Exception:
            pass
    return os.getenv(name, default)


def _read_bool(name: str, default: bool) -> bool:
    value = _read_secret(name, str(default)).strip().lower()
    return value in {"1", "true", "yes", "on"}


def get_settings() -> Settings:
    return Settings(
        groq_api_key=_read_secret("GROQ_API_KEY"),
        groq_model=_read_secret("GROQ_MODEL", "llama-3.1-8b-instant"),
        smtp_host=_read_secret("SMTP_HOST"),
        smtp_port=int(_read_secret("SMTP_PORT", "587")),
        smtp_username=_read_secret("SMTP_USERNAME"),
        smtp_password=_read_secret("SMTP_PASSWORD"),
        smtp_from_email=_read_secret("SMTP_FROM_EMAIL"),
        smtp_from_name=_read_secret("SMTP_FROM_NAME", APP_NAME),
        app_public_url=_read_secret("APP_PUBLIC_URL"),
        enable_email=_read_bool("ENABLE_EMAIL", True),
        enable_groq=_read_bool("ENABLE_GROQ", True),
    )
