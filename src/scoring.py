ATTACK_SPEEDS = {
    "Basic local script": 50000,
    "Optimized local script": 500000,
    "Commodity GPU estimate": 5000000,
}


def risk_level_from_score(strength_score: int) -> str:
    if strength_score >= 75:
        return "Low"
    if strength_score >= 50:
        return "Medium"
    if strength_score >= 25:
        return "High"
    return "Critical"


def format_seconds(seconds: float) -> str:
    if seconds < 1:
        return "Less than 1 second"
    if seconds < 60:
        return f"{seconds:.1f} seconds"
    minutes = seconds / 60
    if minutes < 60:
        return f"{minutes:.1f} minutes"
    hours = minutes / 60
    return f"{hours:.1f} hours"


def estimate_crack_times(attempts: int) -> dict:
    return {
        label: {
            "seconds": round(attempts / speed, 6),
            "label": format_seconds(attempts / speed),
        }
        for label, speed in ATTACK_SPEEDS.items()
    }


def build_score_result(attack_result: dict) -> dict:
    attempts = attack_result["attempts_to_crack"]
    total = attack_result["total_possible_combinations"]
    position_ratio = min(attempts / total, 1)
    strength_score = max(1, min(100, round(position_ratio * 100)))
    hack_probability = max(1, min(100, 101 - strength_score))
    estimates = estimate_crack_times(attempts)

    return {
        "strength_score_out_of_100": strength_score,
        "hack_probability_out_of_100": hack_probability,
        "risk_level": risk_level_from_score(strength_score),
        "estimated_crack_times": estimates,
        "estimated_crack_time_label": estimates["Basic local script"]["label"],
    }

