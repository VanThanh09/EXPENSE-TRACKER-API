from app.core.security import verify_password
from app.models import User
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.core import security

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).one_or_none()

    if not user:
        return None

    if not verify_password(password, user.password):
        return None

    return user

def create_user(db: Session, user_data):
    existing_user = db.query(User).filter(User.email == user_data.email).one_or_none()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hash_pw = security.hash_password(user_data.password)

    new_user = User(name = user_data.name,email=user_data.email, password=hash_pw)

    db.add(new_user)
    db.commit()
    db.refresh(new_user) # take new data from db

    return new_user


def update_user(user: User, update_data, db: Session):
    f_update_data = update_data.dict(exclude_unset=True) # delete the key have none value
    print(f_update_data)

    if f_update_data.get('email') and user.email != f_update_data['email']:

        existing_email = db.query(User).filter(User.email == f_update_data['email']).one_or_none()

        if existing_email:
            raise HTTPException(status_code=400, detail="Email already registered")

    if f_update_data.get('password'):
        hash_pw = security.hash_password(f_update_data['password'])
        f_update_data['password'] = hash_pw

    for key, value in f_update_data.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user