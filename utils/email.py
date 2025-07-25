import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
SENDER_EMAIL = "SoulScribe.alerts@gmail.com"

def send_email(to, subject, body):
    message = Mail(
        from_email=SENDER_EMAIL,
        to_emails=to,
        subject=subject,
        html_content=body  # <-- now supports HTML!
    )
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        sg.send(message)
        print(f"📧 Email sent to {to}")
    except Exception as e:
        print(f"❌ SendGrid Error: {e}")
