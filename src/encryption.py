import hashlib


CAESAR_SHIFT = 3
SUBSTITUTION_MAP = {
    "0": "7",
    "1": "3",
    "2": "9",
    "3": "0",
    "4": "6",
    "5": "1",
    "6": "8",
    "7": "2",
    "8": "5",
    "9": "4",
}


def caesar_digit_shift(pin: str, shift: int = CAESAR_SHIFT) -> str:
    return "".join(str((int(digit) + shift) % 10) for digit in pin)


def digit_substitution_cipher(pin: str) -> str:
    return "".join(SUBSTITUTION_MAP[digit] for digit in pin)


def sha256_reduced_hash(pin: str) -> str:
    digest = hashlib.sha256(pin.encode("utf-8")).hexdigest()
    return f"{int(digest, 16) % 10000:04d}"


def transform_pin(pin: str, method: str) -> str:
    if method == "Caesar Digit Shift":
        return caesar_digit_shift(pin)
    if method == "Digit Substitution Cipher":
        return digit_substitution_cipher(pin)
    if method == "SHA-256 Reduced Demo Hash":
        return sha256_reduced_hash(pin)
    raise ValueError(f"Unsupported transformation method: {method}")

