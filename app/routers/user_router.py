from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import create_access_token, TOKEN_EXPIRES
from app.dependencies import get_db, get_current_user
from app.schemas.auth import Token, UserLogin
from app.schemas.user_schema import UserResponse, UserCreate, UserUpdate
from app.services import user_service
from app.services.user_service import create_user, update_user

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        new_user = create_user(db, user)
        return new_user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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


@router.patch("/my_profile", response_model=UserResponse)
def update_my_profile(update_data: UserUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    try:
        user = update_user(current_user, update_data, db)
        return user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

