from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException

from app.core.security import decode_token
from app.core.database import SessionLocal
from sqlalchemy.orm import Session
from app.models import User


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/toke") # get token from header

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    payload = decode_token(token)

    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token - Login again")

    user_email = payload.get("sub")

    user = db.query(User).filter(User.email == user_email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user
