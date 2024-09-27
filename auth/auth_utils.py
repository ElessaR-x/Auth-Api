# auth_utils.py
from fastapi import HTTPException, status, Depends
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from models import TokenData, UserInDB
from utils import get_user, fake_users_db

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

# Kullanıcının rolünü kontrol etme
def check_role(current_user: UserInDB, required_role: str):
    if current_user.role != required_role:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")

# Kullanıcının minimum role sahip olup olmadığını kontrol eden yardımcı fonksiyon
def check_minimum_role(current_user: UserInDB, allowed_roles: list):
    if current_user.role not in allowed_roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")