from jose import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException
from models import TokenUser

SECRET_KEY = 'supersecret'
ALGORITHM = 'HS256'

def create_token(user: TokenUser):
    expire = datetime.utcnow() + timedelta(minutes=30)
    payload = {'user_id': user.user_id, 'user_name': user.user_name, 'role': user.role, 'exp': expire}
    return jwt.encode(payload, SECRET_KEY, ALGORITHM)

def verify_token(token: str):
    pl = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    if pl.get('user_id') is None: raise HTTPException(status_code=401, detail='Invalid token')
    return TokenUser(user_id = pl.get('user_id'), user_name = pl.get('user_name'), role = pl.get('role'))