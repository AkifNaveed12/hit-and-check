import smtplib
from email.message import EmailMessage


def send_report_email(recipient: str, report: dict, settings) -> dict:
    if not settings.enable_email:
        return {"ok": False, "message": "Email sending is disabled."}

    required = [
        settings.smtp_host,
        settings.smtp_username,
        settings.smtp_password,
        settings.smtp_from_email,
    ]
    if not all(required):
        return {"ok": False, "message": "SMTP settings are missing. Check .env or Streamlit secrets."}

    message = EmailMessage()
    message["Subject"] = report["subject"]
    message["From"] = f"{settings.smtp_from_name} <{settings.smtp_from_email}>"
    message["To"] = recipient
    message.set_content(report["text"])
    message.add_alternative(report["html"], subtype="html")

    try:
        with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
            server.starttls()
            server.login(settings.smtp_username, settings.smtp_password)
            server.send_message(message)
        return {"ok": True, "message": "Email sent."}
    except Exception as exc:
        return {"ok": False, "message": f"Email failed: {exc}"}

