from src.config import APP_NAME


def build_report_payload(analysis: dict) -> dict:
    attack = analysis["attack_result"]
    score = analysis["score_result"]
    user = analysis["user"]
    pin_data = analysis["pin_data"]

    return {
        "app_name": APP_NAME,
        "analysis_type": "pin_strength_report",
        "user": {
            "name": user["name"],
            "email": user.get("email", ""),
        },
        "pin_data": {
            "pin_length": 4,
            "character_set": "numeric_only",
            "encrypted_pin": pin_data["encrypted_pin"],
            "encryption_method": pin_data["encryption_method"],
            "real_pin_included": False,
        },
        "attack_result": {
            "attack_type": attack["attack_type"],
            "total_possible_combinations": attack["total_possible_combinations"],
            "attempts_to_crack": attack["attempts_to_crack"],
            "crack_position_percentage": attack["crack_position_percentage"],
            "estimated_crack_time_seconds": score["estimated_crack_times"]["Basic local script"]["seconds"],
        },
        "risk_metrics": {
            "strength_score_out_of_100": score["strength_score_out_of_100"],
            "hack_probability_out_of_100": score["hack_probability_out_of_100"],
            "risk_level": score["risk_level"],
        },
        "instructions": {
            "tone": "clear, educational, non-technical where possible",
            "include_recommendations": True,
            "include_attack_explanation": True,
            "do_not_reveal_real_pin": True,
        },
    }


def build_chat_payload(user_question: str, analysis: dict) -> dict:
    attack = analysis["attack_result"]
    score = analysis["score_result"]
    return {
        "app_name": APP_NAME,
        "chat_type": "security_awareness_assistant",
        "user_question": user_question,
        "context": {
            "pin_length": 4,
            "attack_type": attack["attack_type"],
            "attempts_to_crack": attack["attempts_to_crack"],
            "risk_level": score["risk_level"],
        },
        "rules": {
            "do_not_request_real_passwords": True,
            "do_not_store_sensitive_data": True,
            "answer_for_education_only": True,
        },
    }


def build_email_report(analysis: dict, ai_report: dict) -> dict:
    attack = analysis["attack_result"]
    score = analysis["score_result"]
    user = analysis["user"]

    subject = f"Hit & Check Security Awareness Report for {user['name']}"
    text = f"""
Hello {user['name']},

Here is your Hit & Check educational PIN security report.

Risk Level: {score['risk_level']}
Strength Score: {score['strength_score_out_of_100']}/100
Hack Probability: {score['hack_probability_out_of_100']}%
Attack Type: {attack['attack_type']}
Attempts to Crack: {attack['attempts_to_crack']}
Total Possible Combinations: {attack['total_possible_combinations']}
Estimated Crack Time: {score['estimated_crack_time_label']}

Summary:
{ai_report.get('summary', 'A 4-digit numeric PIN has a small search space and can be tested quickly in a simulation.')}

Recommendations:
{chr(10).join('- ' + item for item in ai_report.get('recommendations', []))}

Educational note: This report is for awareness only. Do not use real banking PINs in this app.
"""
    html_recommendations = "".join(f"<li>{item}</li>" for item in ai_report.get("recommendations", []))
    html = f"""
<html>
  <body style="margin:0;padding:0;background:#f4f6f8;font-family:Arial,Helvetica,sans-serif;color:#17202a;">
    <div style="max-width:640px;margin:0 auto;padding:24px;">
      <div style="background:#ffffff;border:1px solid #d9e2ec;border-radius:8px;padding:24px;">
        <h1 style="font-size:22px;margin:0 0 12px;">Hit & Check Security Awareness Report</h1>
        <p>Hello {user['name']},</p>
        <p>This is an educational report based on your demo PIN simulation.</p>
        <h2 style="font-size:18px;">Key Metrics</h2>
        <ul>
          <li><strong>Risk Level:</strong> {score['risk_level']}</li>
          <li><strong>Strength Score:</strong> {score['strength_score_out_of_100']}/100</li>
          <li><strong>Hack Probability:</strong> {score['hack_probability_out_of_100']}%</li>
          <li><strong>Attack Type:</strong> {attack['attack_type']}</li>
          <li><strong>Attempts to Crack:</strong> {attack['attempts_to_crack']}</li>
          <li><strong>Total Combinations:</strong> {attack['total_possible_combinations']}</li>
          <li><strong>Estimated Crack Time:</strong> {score['estimated_crack_time_label']}</li>
        </ul>
        <h2 style="font-size:18px;">Summary</h2>
        <p>{ai_report.get('summary', 'A 4-digit numeric PIN has a small search space and can be tested quickly in a simulation.')}</p>
        <h2 style="font-size:18px;">Recommendations</h2>
        <ul>{html_recommendations}</ul>
        <p style="font-size:13px;color:#52616b;">Educational note: Do not use real banking PINs in this app.</p>
      </div>
    </div>
  </body>
</html>
"""
    return {"subject": subject, "text": text.strip(), "html": html.strip()}

