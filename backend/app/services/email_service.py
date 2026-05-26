import os
from dotenv import load_dotenv
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import EmailStr

load_dotenv()

# Set up connection configurations matching your .env data parameters
conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_PORT=int(os.getenv("MAIL_PORT", 587)),
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_FROM_NAME=os.getenv("MAIL_FROM_NAME", "CelebrityAI"),
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

fm = FastMail(conf)

async def send_verification_email(email: EmailStr, token: str):
    # Dynamic verification layout targeting your FastAPI server base domain
    verify_link = f"http://localhost:8000/auth/verify-email?token={token}"
    
    html_content = f"""
    <h3>Welcome to CelebrityAI!</h3>
    <p>Thank you for registering. Please click the link below to verify your account:</p>
    <p><a href="{verify_link}" style="padding: 10px 20px; background-color: #4F46E5; color: white; text-decoration: none; border-radius: 5px;">Verify Email Address</a></p>
    <br>
    <p>If you did not request this, please ignore this email.</p>
    """

    message = MessageSchema(
        subject="Verify your CelebrityAI account",
        recipients=[email],
        body=html_content,
        subtype="html"
    )

    await fm.send_message(message)

async def send_reset_password_email(
    email: EmailStr,
    token: str
):

    reset_link = f"http://localhost:5173/reset-password?token={token}"

    message = MessageSchema(
        subject="Reset your password",
        recipients=[email],
        body=f"Click here to reset password: {reset_link}",
        subtype="html"
    )

    await fm.send_message(message)    
