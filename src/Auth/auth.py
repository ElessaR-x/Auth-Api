from fastapi import APIRouter, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel
from datetime import timedelta, datetime
from models import UserInDB, TokenData, RegisterForm, LoginForm
from utils import get_user, save_user, fake_users_db, get_license , fake_licenses_db, ALGORITHM, SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES
from src.Auth.auth_utils import convert_expired_date, create_access_token, pwd_context, verify_hwid, authenticate_user


# Router oluşturma
router = APIRouter()

# OAuth2 şeması
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")




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

    license_duration_days = get_license(fake_licenses_db, license_key = register_form.license_key)

    print(license_duration_days.duration_days)

    license_expiration = convert_expired_date(license_duration_days.duration_days)

    # Convert string to datetime
    try:
        license_expiration = datetime.strptime(license_expiration, '%d-%m-%Y %H:%M:%S')
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid date format: {e}",
        )

    new_user = UserInDB(
        username=register_form.username,
        full_name=register_form.full_name,
        email=register_form.email,
        hashed_password=hashed_password,
        hwid=register_form.hwid,
        license_expiration=license_expiration  # Lisans süresi olmadan kayıt
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
