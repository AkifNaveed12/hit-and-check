import re


EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def validate_pin(pin: str) -> str | None:
    if not pin:
        return "Demo PIN is required."
    if not pin.isdigit():
        return "Demo PIN must contain digits only."
    if len(pin) != 4:
        return "Demo PIN must be exactly 4 digits."
    return None


def validate_email(email: str, required: bool = False) -> str | None:
    cleaned = email.strip()
    if not cleaned and not required:
        return None
    if not cleaned and required:
        return "Email address is required."
    if not EMAIL_PATTERN.match(cleaned):
        return "Enter a valid email address."
    return None

