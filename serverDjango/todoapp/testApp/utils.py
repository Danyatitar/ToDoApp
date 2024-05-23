from datetime import datetime, timedelta
from typing import Optional

import bcrypt
from django.core.exceptions import ValidationError
from django.core.signing import BadSignature, TimestampSigner
from django.http import JsonResponse
from jwt import decode as jwt_decode
from jwt import encode as jwt_encode

from .models import User

SECRET_KEY = "todo-app-secret"
ALGORITHM = "HS256"
SIGNER = TimestampSigner(SECRET_KEY)

def hash_password(password: str) -> str:
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt_encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> Optional[dict]:
    try:
        payload = jwt_decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except:
        return None

def sign_data(data: dict, max_age: Optional[int] = None) -> str:
    try:
        signed_data = SIGNER.sign(data)
        if max_age:
            signed_data += ":" + str(max_age)
        return signed_data
    except:
        return None

def unsign_data(signed_data: str) -> Optional[dict]:
    try:
        data = SIGNER.unsign(signed_data, max_age=60 * 60 * 24)  # 1 day max_age
        return data
    except BadSignature:
        return None

def check_user(request):
    cookie_value = request.COOKIES.get('token')
    payload = decode_token(cookie_value)
    try:
            existing_user = User.objects.get(id=payload["id"])
            return existing_user
    except User.DoesNotExist:
        return JsonResponse({"detail": "User doesn't exist"}, status=400)
