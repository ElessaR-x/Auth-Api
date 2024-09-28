# auth_utils.py
from fastapi import HTTPException, status, Depends
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from models import TokenData, UserInDB
from utils import get_user, fake_users_db
import datetime

# OAuth2 şeması
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Secret key and algorithm settings
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

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

# Kullanıcının rolünü kontrol etme
def check_role(current_user: UserInDB, required_role: str):
    if current_user.role != required_role:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")

# Kullanıcının minimum role sahip olup olmadığını kontrol eden yardımcı fonksiyon
def check_minimum_role(current_user: UserInDB, allowed_roles: list):
    if current_user.role not in allowed_roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")