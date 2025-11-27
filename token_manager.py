from jose import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException

SECRET_KEY = 'supersecret'
ALGORITHM = 'HS256'

def create_token(username: str):
    expire = datetime.utcnow() + timedelta(minutes=30)
    payload = {'sub': username, 'exp': expire}
    return jwt.encode(payload, SECRET_KEY, ALGORITHM)

def verify_token(token: str):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username = payload.get('sub')
    if username is None: raise HTTPException(status_code=401, detail='Invalid token')
    return {'user': username}