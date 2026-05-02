from src.encryption import caesar_digit_shift, digit_substitution_cipher, sha256_reduced_hash, transform_pin


def test_caesar_digit_shift():
    assert caesar_digit_shift("1234") == "4567"
    assert caesar_digit_shift("7890") == "0123"


def test_digit_substitution_cipher():
    assert digit_substitution_cipher("0123") == "7390"


def test_sha256_reduced_hash_is_four_digits():
    value = sha256_reduced_hash("1234")
    assert len(value) == 4
    assert value.isdigit()


def test_transform_pin_dispatch():
    assert transform_pin("1234", "Caesar Digit Shift") == "4567"
    assert transform_pin("0123", "Digit Substitution Cipher") == "7390"

