from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import create_access_token, TOKEN_EXPIRES
from app.dependencies import get_db, get_current_user
from app.schemas.auth import Token, UserLogin
from app.schemas.user_schema import UserResponse
from app.services import user_service

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/login", response_model=Token)
def login(data: UserLogin, db: Session = Depends(get_db)):
    user = user_service.authenticate_user(db, data.email, data.password)

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    token = create_access_token(data={"sub": str(user.id)})

    return {"access_token": token, "token_type": "bearer", "token_expires": TOKEN_EXPIRES}


@router.get("/my_profile", response_model=UserResponse)
def get_my_profile(current_user = Depends(get_current_user)):
    return current_user
