import json
import time
from pathlib import Path

from src.encryption import transform_pin


TOTAL_PIN_COMBINATIONS = 10000
DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def generate_pin_space() -> list[str]:
    return [f"{value:04d}" for value in range(TOTAL_PIN_COMBINATIONS)]


def load_common_pins() -> list[str]:
    path = DATA_DIR / "common_pins.json"
    if not path.exists():
        return ["0000", "1111", "1234", "1212", "7777", "1004", "2000", "4444", "2222", "6969"]
    return json.loads(path.read_text(encoding="utf-8"))


def _build_result(
    attack_type: str,
    encrypted_pin: str,
    method: str,
    attempts: int,
    cracked_pin: str | None,
    elapsed_seconds: float,
) -> dict:
    return {
        "attack_type": attack_type,
        "encrypted_pin": encrypted_pin,
        "encryption_method": method,
        "total_possible_combinations": TOTAL_PIN_COMBINATIONS,
        "attempts_to_crack": attempts,
        "cracked": cracked_pin is not None,
        "cracked_pin": cracked_pin,
        "crack_position_percentage": round((attempts / TOTAL_PIN_COMBINATIONS) * 100, 2),
        "elapsed_seconds": round(elapsed_seconds, 6),
    }


def brute_force_attack(encrypted_pin: str, method: str) -> dict:
    started_at = time.perf_counter()
    attempts = 0
    for candidate in generate_pin_space():
        attempts += 1
        if transform_pin(candidate, method) == encrypted_pin:
            elapsed = time.perf_counter() - started_at
            return _build_result("Brute Force", encrypted_pin, method, attempts, candidate, elapsed)
    elapsed = time.perf_counter() - started_at
    return _build_result("Brute Force", encrypted_pin, method, attempts, None, elapsed)


def dictionary_attack(encrypted_pin: str, method: str) -> dict:
    started_at = time.perf_counter()
    attempts = 0
    for candidate in load_common_pins():
        attempts += 1
        if transform_pin(candidate, method) == encrypted_pin:
            elapsed = time.perf_counter() - started_at
            return _build_result("Dictionary Attack", encrypted_pin, method, attempts, candidate, elapsed)
    elapsed = time.perf_counter() - started_at
    return _build_result("Dictionary Attack", encrypted_pin, method, attempts, None, elapsed)


def combined_attack(encrypted_pin: str, method: str) -> dict:
    started_at = time.perf_counter()
    attempts = 0
    tried = set()

    for candidate in load_common_pins():
        tried.add(candidate)
        attempts += 1
        if transform_pin(candidate, method) == encrypted_pin:
            elapsed = time.perf_counter() - started_at
            return _build_result("Combined Attack", encrypted_pin, method, attempts, candidate, elapsed)

    for candidate in generate_pin_space():
        if candidate in tried:
            continue
        attempts += 1
        if transform_pin(candidate, method) == encrypted_pin:
            elapsed = time.perf_counter() - started_at
            return _build_result("Combined Attack", encrypted_pin, method, attempts, candidate, elapsed)

    elapsed = time.perf_counter() - started_at
    return _build_result("Combined Attack", encrypted_pin, method, attempts, None, elapsed)


def run_attack(encrypted_pin: str, method: str, attack_type: str) -> dict:
    if attack_type == "Brute Force":
        return brute_force_attack(encrypted_pin, method)
    if attack_type == "Dictionary Attack":
        return dictionary_attack(encrypted_pin, method)
    if attack_type == "Combined Attack":
        return combined_attack(encrypted_pin, method)
    raise ValueError(f"Unsupported attack type: {attack_type}")

