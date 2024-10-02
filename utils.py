# utils.py
from models import UserInDB, License, TokenData
from typing import Optional
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, status, Depends
from jose import JWTError, jwt
# OAuth2 şeması
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Secret key and algorithm settings
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Kullanıcının rolünü kontrol etme
def check_role(current_user: UserInDB, required_role: str):
    if current_user.role != required_role:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")


# Kullanıcının minimum role sahip olup olmadığını kontrol eden yardımcı fonksiyon
def check_minimum_role(current_user: UserInDB, allowed_roles: list):
    if current_user.role not in allowed_roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
  

# get_current_user: Token doğrulama ve kullanıcıyı doğrulama fonksiyonu
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception

    return user

# Fake user database
fake_users_db = {
    "arda": {
        "username": "arda",
        "full_name": "Arda",
        "email": "arda@example.com",
        "hashed_password": "$2a$10$DaM3/xzpzN/VscepzEF0O.ko3hEDVPQZtbpcjUrAFuSZvTllB4Emq",  # bcrypt hashed password for "arda"
        "disabled": False,
        "hwid": "xx",
        "license_expiration": "2024-11-29T07:57:54",
        "role": "owner"
    },

    "sezer": {
            "username": "sezer",
            "full_name": "sezer",
            "email": "sezer@example.com",
            "hashed_password": "$2a$10$DaM3/xzpzN/VscepzEF0O.ko3hEDVPQZtbpcjUrAFuSZvTllB4Emq",  # bcrypt hashed password for "arda"
            "disabled": False,
            "hwid": "xx",
            "license_expiration": "2024-07-29T07:57:54",
            "role": "admin"
        }
}

# Fake license database
fake_licenses_db = {
    "ABC123": {"key": "ABC123", "duration_days": 30},  # Örnek bir lisans
    "DEF456": {"key": "DEF456", "duration_days": 60},
}

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")




def get_user(db, username: str) -> Optional[UserInDB]:
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def save_user(db, user: UserInDB):
    db[user.username] = {
        "username": user.username,
        "full_name": user.full_name,
        "email": user.email,
        "hashed_password": user.hashed_password,
        "license_expiration": user.license_expiration,
        "role": user.role,
        "hwid": user.hwid,
        "disabled": False,
    }


def get_license(db, license_key: str) -> Optional[License]:
    if license_key in db:
        license_data = db[license_key]
        return License(**license_data)


def save_license(db, license: License):
    # Lisans kaydetme fonksiyonu
    db[license.key] = {"key": license.key, "duration_days": license.duration_days}