import os
from datetime import datetime, timedelta, timezone
from jose import jwt
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": int(expire.timestamp())}) # Universal timestamp standard
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_email_token(email: str) -> str:
    # Fixed: Uses modern timezone-aware UTC standard instead of utcnow()
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    
    payload = {
        "sub": email,
        "exp": int(expire.timestamp()), # Universal timestamp standard
        "type": "email_verification"
    }
    
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def create_reset_password_token(email: str):

    expire = datetime.utcnow() + timedelta(minutes=15)

    payload = {
        "sub": email,
        "exp": expire,
        "type": "password_reset"
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )    
