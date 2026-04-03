from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import create_access_token, TOKEN_EXPIRES
from app.api.deps import get_db, get_current_user
from app.schemas import Token, UserLogin, UserResponse, UserCreate, UserUpdate
from app.crud import create_user, update_user, authenticate_user
from app.worker.tasks import send_email_welcome

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        new_user = create_user(db, user)
        try:
            send_email_welcome.delay(user.email)
        except Exception as e:
            print("Celery error:", e)
        return new_user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/token", response_model=Token)
def login(data: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, data.email, data.password)

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    token = create_access_token(data={"sub": str(user.email)})

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

