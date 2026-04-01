from app.core.security import verify_password
from app.models.user import User
from sqlalchemy.orm import Session

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).one_or_none()

    if not user:
        return None

    if not verify_password(password, user.password):
        return None

    return user