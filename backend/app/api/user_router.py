from fastapi import APIRouter, Depends
from app.auth.dependencies import get_current_user
from sqlalchemy.orm import Session
from fastapi import Depends
from app.database.database import get_db
from app.schemas.user_schema import UserUpdate
from app.schemas.user_schema import ChangePassword
from app.auth.hash import verify_password, hash_password
from fastapi import HTTPException

router = APIRouter(
    prefix="/user",
    tags=["User"]
)

# Explicitly enforcing Depends(get_current_user) forces the padlock icon to lock!
@router.get("/me")
def get_me(current_user=Depends(get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "is_verified": current_user.is_verified
    }

@router.put("/update-profile")
def update_profile(
    request: UserUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    if request.username:
        current_user.username = request.username

    if request.bio:
        current_user.bio = request.bio

    if request.profile_image:
        current_user.profile_image = request.profile_image

    db.commit()

    return {
        "message": "Profile updated successfully"
    }

@router.put("/change-password")
def change_password(
    request: ChangePassword,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    if not verify_password(
        request.old_password,
        current_user.password
    ):
        raise HTTPException(
            status_code=400,
            detail="Old password incorrect"
        )

    current_user.password = hash_password(
        request.new_password
    )

    db.commit()

    return {
        "message": "Password updated successfully"
    }    