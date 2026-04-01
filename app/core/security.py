from datetime import datetime, timedelta

from jose import jwt, JWTError
from passlib.context import CryptContext
from app.core.config import settings

SECRECT_KEY = settings.secret_key
ALGORITHM = "HS256"
TOKEN_EXPIRES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#hash password
def hasd_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

#create JWT
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()

    expire = datetime.now() + (expires_delta or timedelta(minutes=TOKEN_EXPIRES))

    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRECT_KEY, algorithm=ALGORITHM)


#decode JWT
def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRECT_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None