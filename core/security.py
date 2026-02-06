import os
from passlib.context import CryptContext
from dotenv import load_dotenv
from datetime import datetime,timedelta,timezone
from jose import jwt, JWTError

load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "change-me")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")


pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_password(password:str):
    return pwd_context.hash(password)


def verify_password(plaintext_password:str, hashed_password:str):
    return pwd_context.verify(plaintext_password, hashed_password)

def create_token(data: dict):
    datacopy_to_encode = data.copy()
    expire = datetime.now(tz=timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    datacopy_to_encode.update({"exp": expire})
    return jwt.encode(datacopy_to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

def decode_token(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except JWTError:
        return None
    
