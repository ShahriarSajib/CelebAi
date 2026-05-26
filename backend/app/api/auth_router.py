from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.requests import Request
from sqlalchemy.orm import Session
from jose import jwt, JWTError
import os

from app.database.database import get_db
from app.models.user_model import User
from app.schemas.user_schema import UserRegister, UserLogin
from app.auth.hash import hash_password, verify_password
from app.auth.jwt_handler import create_access_token, create_email_token
from app.services.email_service import send_verification_email

from app.schemas.user_schema import (
    ForgotPasswordRequest,
    ResetPasswordRequest
)

from app.auth.jwt_handler import (
    create_reset_password_token
)

from app.services.email_service import (
    send_reset_password_email
)

# Load environment keys for token verification
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

router = APIRouter(prefix="/auth", tags=["Authentication"])

# --- Register Endpoint ---
@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(request: UserRegister, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == request.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    if db.query(User).filter(User.username == request.username).first():
        raise HTTPException(status_code=400, detail="Username already taken")

    new_user = User(
        username=request.username,
        email=request.email,
        password=hash_password(request.password),
        is_verified=False  # User is blocked from accessing routes until verification
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Generate secure verification hash token string
    token = create_email_token(new_user.email)
    
    # Asynchronously dispatch validation link to user inbox
    await send_verification_email(new_user.email, token)

    return {"message": "User created. Please verify your email."}

# --- Universal Hybrid Login (Handles JSON inputs AND the Green Authorize Button seamlessly) ---
@router.post("/login")
async def login(request: Request, body: UserLogin = None, db: Session = Depends(get_db)):
    email = None
    password = None
    content_type = request.headers.get("content-type", "")
    
    # 1. Mode A: Process standard Form-data layout payload (Swagger Green Button)
    if "application/x-www-form-urlencoded" in content_type:
        form_data = await request.form()
        email = form_data.get("username")  # Swagger OAuth2 maps email data to 'username'
        password = form_data.get("password")
        
    # 2. Mode B: Process standard structured JSON packaging body (Swagger Text Box)
    else:
        if body:
            email = body.email
            password = body.password
        else:
            try:
                body_bytes = await request.body()
                if body_bytes:
                    json_data = await request.json()
                    email = json_data.get("email") or json_data.get("username")
                    password = json_data.get("password")
            except Exception:
                raise HTTPException(status_code=400, detail="Invalid request format")

    if not email or not password:
        raise HTTPException(status_code=422, detail="Email and password fields are required")

    # Match system credentials against PostgreSQL user records
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    # PRODUCTION SECURITY GUARD: Block login session tokens if email verification is outstanding
    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Please verify your email first"
        )

    # Issue secure application session authorization token string
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# --- Verify Email Endpoint ---
@router.get("/verify-email")
def verify_email(token: str, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        token_type = payload.get("type")

        if token_type != "email_verification":
            raise HTTPException(status_code=400, detail="Invalid token")
            
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.is_verified:
        return {"message": "Email is already verified."}

    user.is_verified = True
    db.commit()
    return {"message": "Email verified successfully"}

@router.post("/forgot-password")
async def forgot_password(
    request: ForgotPasswordRequest,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email == request.email
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    token = create_reset_password_token(
        user.email
    )

    await send_reset_password_email(
        user.email,
        token
    )

    return {
        "message": "Password reset email sent"
    }

@router.post("/reset-password")
def reset_password(
    request: ResetPasswordRequest,
    db: Session = Depends(get_db)
):

    try:

        payload = jwt.decode(
            request.token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        email = payload.get("sub")

        token_type = payload.get("type")

        if token_type != "password_reset":
            raise HTTPException(
                status_code=400,
                detail="Invalid token"
            )

    except JWTError:

        raise HTTPException(
            status_code=400,
            detail="Invalid or expired token"
        )

    user = db.query(User).filter(
        User.email == email
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    user.password = hash_password(
        request.new_password
    )

    db.commit()

    return {
        "message": "Password reset successful"
    }    
