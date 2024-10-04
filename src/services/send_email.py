import smtplib
from src.core.config import settings
from email.message import EmailMessage
from jinja2 import Environment, FileSystemLoader


# Description params
# action = {"create_account", "activate_account", reset_password}
def set_message_body(
    language: str = "en", action: str = "activate_account", template_vars: dict = None
):
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template(f"emails/{language}/{action}.html")
    return template.render(template_vars)


def send_email(params: dict):
    content_body = set_message_body(
        language=params.get("language"),
        action=params.get("action"),
        template_vars=params.get("params"),
    )
    msg = EmailMessage()
    msg["Subject"] = params.get("subject")
    msg["From"] = settings.SMTP_SENDER_MAIL
    msg["To"] = params.get("email")
    msg.set_content(content_body)
    msg.replace_header("Content-Type", "text/html")

    # Login to the Gmail SMTP server
    with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
        server.ehlo()  # Can be omitted
        server.starttls()
        server.login(settings.SMTP_SENDER_MAIL, settings.SMTP_PASSWORD)

        # Send the email
        server.send_message(msg)

        # Logout of the SMTP server
        server.quit()
