# auth_utils.py
from fastapi import HTTPException, status, Depends
from jose import jwt
from models import TokenData, UserInDB
from utils import get_user, fake_users_db, pwd_context, SECRET_KEY, ALGORITHM
from datetime import timedelta, datetime




# Kullanıcının girdiği lisans keyin süresini bitiş tarihine çevirme
def convert_expired_date(license_duration_days: int):
    # Geçerli tarihi al
    current_date = datetime.datetime.now()

    # Lisans süresini integer olarak al


    # Geçerlilik süresini bugünden itibaren hesapla
    expiration_date = current_date + datetime.timedelta(days=license_duration_days)

    # Tarih ve saat formatını belirle
    formatted_expiration_date = expiration_date.strftime("%d-%m-%Y %H:%M:%S")

    return formatted_expiration_date


  
# Token oluşturma işlevi
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Parola doğrulama
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

# HWID kontrolü
def verify_hwid(db, username: str, hwid: str):
    user = get_user(db, username)

    if not user.hwid == hwid:
        return False

    return user

# Kullanıcı kimlik doğrulama
def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False

    return user
