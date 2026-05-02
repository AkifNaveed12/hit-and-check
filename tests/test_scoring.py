from src.scoring import build_score_result, format_seconds, risk_level_from_score


def test_risk_level_from_score():
    assert risk_level_from_score(80) == "Low"
    assert risk_level_from_score(60) == "Medium"
    assert risk_level_from_score(30) == "High"
    assert risk_level_from_score(10) == "Critical"


def test_format_seconds():
    assert format_seconds(0.5) == "Less than 1 second"
    assert format_seconds(10) == "10.0 seconds"
    assert format_seconds(120) == "2.0 minutes"


def test_build_score_result():
    attack_result = {
        "attempts_to_crack": 5000,
        "total_possible_combinations": 10000,
    }
    result = build_score_result(attack_result)
    assert result["strength_score_out_of_100"] == 50
    assert result["hack_probability_out_of_100"] == 51
    assert result["risk_level"] == "Medium"

