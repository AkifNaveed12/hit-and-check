from src.attacks import brute_force_attack, combined_attack, dictionary_attack
from src.encryption import transform_pin


def test_brute_force_attack_finds_pin():
    encrypted = transform_pin("0003", "Caesar Digit Shift")
    result = brute_force_attack(encrypted, "Caesar Digit Shift")
    assert result["cracked"] is True
    assert result["cracked_pin"] == "0003"
    assert result["attempts_to_crack"] == 4


def test_dictionary_attack_finds_common_pin():
    encrypted = transform_pin("1234", "Caesar Digit Shift")
    result = dictionary_attack(encrypted, "Caesar Digit Shift")
    assert result["cracked"] is True
    assert result["cracked_pin"] == "1234"


def test_combined_attack_finds_non_dictionary_pin():
    encrypted = transform_pin("9876", "Digit Substitution Cipher")
    result = combined_attack(encrypted, "Digit Substitution Cipher")
    assert result["cracked"] is True
    assert result["cracked_pin"] == "9876"

