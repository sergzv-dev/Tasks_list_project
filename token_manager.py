from jose import jwt, JWTError, ExpiredSignatureError
from datetime import datetime, timedelta
from fastapi import HTTPException
from models import TokenUser
import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

def create_token(user: TokenUser):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {'user_id': user.user_id, 'user_name': user.user_name, 'role': user.role, 'exp': expire}
    return jwt.encode(payload, SECRET_KEY, ALGORITHM)

def verify_token(token: str):
    try:
        pl = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except ExpiredSignatureError:
        raise HTTPException(401, "Token expired")
    except JWTError:
        raise HTTPException(401, "Invalid token")

    return TokenUser(user_id = pl.get('user_id'), user_name = pl.get('user_name'), role = pl.get('role'))