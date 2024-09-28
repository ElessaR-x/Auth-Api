from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import BaseModel
from datetime import timedelta, datetime

from starlette.datastructures import FormData

from models import UserInDB, TokenData, RegisterForm, LoginForm
from utils import get_user, save_user, fake_users_db
from passlib.context import CryptContext

# Router oluşturma
router = APIRouter()

# OAuth2 şeması
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Secret key and algorithm settings
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


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


# Kullanıcı kaydı (register)
@router.post("/register", tags=["Authentication"], summary="Kullanıcı kaydı")
async def register(register_form: RegisterForm):
    user = get_user(fake_users_db, register_form.username)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    hashed_password = pwd_context.hash(register_form.password)
    new_user = UserInDB(
        username=register_form.username,
        full_name=register_form.full_name,
        email=register_form.email,
        hashed_password=hashed_password,
        hwid=register_form.hwid,
        license_expiration=None  # Lisans süresi olmadan kayıt
    )
    save_user(fake_users_db, new_user)
    return {"message": "User registered successfully"}


# Giriş (login) işlemi
@router.post("/login", tags=["Authentication"], summary="Kullanıcı girişi")
async def login_for_access_token(request: Request, form_data: LoginForm):


    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username, password, or hwid",
            headers={"WWW-Authenticate": "Bearer"},
        )

    hwid = verify_hwid(fake_users_db, form_data.username, form_data.hwid)
    if not hwid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect hwid",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# Token kontrolü (check)
class TokenCheckRequest(BaseModel):
    token: str


@router.post("/token-check", tags=["Authentication"], summary="Token kontrolü")
async def token_check(request: TokenCheckRequest):
    try:
        payload = jwt.decode(request.token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if not username:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid or expired")
        return {"status": "Authorized", "user": username}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid or expired")
