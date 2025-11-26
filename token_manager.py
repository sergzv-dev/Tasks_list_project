from jose import jwt, JWTError
from datetime import datetime, timedelta

SECRET_KEY = "supersecret"
ALGORITHM = "HS256"

def create_token(username: str):
    expire = datetime.utcnow() + timedelta(minutes=30)
    payload = {'sub': username, 'exp': expire}
    return jwt.encode(payload, SECRET_KEY, ALGORITHM)