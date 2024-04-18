from datetime import datetime, timedelta
from typing import Optional

import bcrypt
from fastapi import Cookie
from jwt import PyJWTError
from jwt import decode as jwt_decode
from jwt import encode as jwt_encode

SECRET_KEY = "todo-app-secret"
ALGORITHM = "HS256"

def hash_password(password: str) -> str:
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password

def verify_password(plain_password: str, hashed_password: str) -> bool:
    
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password )

def create_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt_encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(token: str):
    try:
        payload = jwt_decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except PyJWTError:
        return None
    
def get_token_from_cookie(token: Optional[str] = Cookie(None)):
    return token  