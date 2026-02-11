from django.core.mail import EmailMultiAlternatives
from django.conf import settings

def send_verification_email(to_email: str, code: str):
    subject = "Verify your email"
    text = f"Your verification code is: {code}\n\nThis code expires in 10 minutes."
    html = f"""
      <p>Your verification code is:</p>
      <h2 style="letter-spacing:2px">{code}</h2>
      <p>This code expires in <b>10 minutes</b>.</p>
    """

    msg = EmailMultiAlternatives(
        subject=subject,
        body=text,
        from_email=settings.EMAIL_HOST_USER,
        to=[to_email],
    )
    msg.attach_alternative(html, "text/html")
    msg.send()

