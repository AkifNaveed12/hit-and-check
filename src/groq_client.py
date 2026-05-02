import json

from src.config import get_settings


def _fallback_report(payload: dict) -> dict:
    risk = payload["risk_metrics"]["risk_level"]
    score = payload["risk_metrics"]["strength_score_out_of_100"]
    probability = payload["risk_metrics"]["hack_probability_out_of_100"]
    attempts = payload["attack_result"]["attempts_to_crack"]

    return {
        "summary": f"This demo PIN received a {risk} risk rating after being matched in {attempts} simulated attempts.",
        "strength_score": score,
        "risk_level": risk,
        "hack_probability": probability,
        "attack_explanation": "A 4-digit numeric PIN has only 10,000 possible values, so an attacker can test the full space quickly in an unrestricted simulation.",
        "estimated_crack_time": "Less than 1 second for many local scripts in this educational model.",
        "key_findings": [
            "The numeric-only search space is small.",
            "Short PINs depend heavily on lockout controls for protection.",
            "Common or patterned PINs are easier to guess early.",
        ],
        "recommendations": [
            "Avoid simple sequences and repeated digits.",
            "Avoid birth years, public dates, and obvious patterns.",
            "Use longer passwords where systems allow them.",
            "Enable multi-factor authentication and account lockout protections.",
        ],
        "educational_note": "This report is for awareness only and should not be used with real banking PINs.",
    }


def generate_pin_report(payload: dict) -> dict:
    settings = get_settings()
    if not settings.enable_groq or not settings.groq_api_key:
        return _fallback_report(payload)

    try:
        from groq import Groq

        client = Groq(api_key=settings.groq_api_key)
        response = client.chat.completions.create(
            model=settings.groq_model,
            messages=[
                {
                    "role": "system",
                    "content": "Return only valid JSON matching the requested security awareness report contract. Do not include markdown.",
                },
                {"role": "user", "content": json.dumps(payload)},
            ],
            temperature=0.2,
        )
        content = response.choices[0].message.content
        return json.loads(content)
    except Exception:
        return _fallback_report(payload)


def generate_chat_response(payload: dict) -> str:
    settings = get_settings()
    question = payload["user_question"]
    if not settings.enable_groq or not settings.groq_api_key:
        return (
            "I can answer in local fallback mode: use demo PINs only, avoid predictable patterns, "
            "and rely on lockout controls plus multi-factor authentication where available."
        )

    try:
        from groq import Groq

        client = Groq(api_key=settings.groq_api_key)
        context = payload.get("context", {})
        user_prompt = f"""
User question:
{question}

Current educational simulation context:
- PIN length: {context.get("pin_length", "unknown")}
- Attack type: {context.get("attack_type", "unknown")}
- Attempts to crack in simulation: {context.get("attempts_to_crack", "unknown")}
- Risk level: {context.get("risk_level", "unknown")}

Answer the user's question directly using this context where helpful.
"""
        response = client.chat.completions.create(
            model=settings.groq_model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a security awareness assistant. Do not ask for real passwords, PINs, OTPs, "
                        "or recovery codes. Do not provide harmful instructions. Keep answers practical."
                    ),
                },
                {"role": "user", "content": user_prompt.strip()},
            ],
            temperature=0.3,
            max_tokens=500,
        )
        content = response.choices[0].message.content
        if content:
            return content.strip()
    except Exception as exc:
        return (
            "I could not reach the AI chatbot service. "
            f"Technical detail: {exc}. "
            "Safe guidance: use longer secrets where possible, avoid predictable patterns, "
            "enable MFA, and keep recovery options up to date."
        )

    return (
        "The AI chatbot returned an empty response. "
        "Safe guidance: use longer secrets where possible, avoid predictable patterns, and enable MFA."
    )
