from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class User(BaseModel):
    username: str
    full_name: Optional[str] = None
    email: Optional[str] = None
    disabled: Optional[bool] = None
    hwid: Optional[str] = None
    role: str = "customer"  # Kullanıcı rolü (customer, reseller, admin, owner)

class UserInDB(User):
    hashed_password: str
    license_expiration: Optional[datetime] = None

class RegisterForm(BaseModel):
    username: str
    password: str
    full_name: Optional[str] = None
    email: Optional[str] = None
    license_key: str
    hwid: str

class LoginForm(BaseModel):
    username: str
    password: str
    hwid: str

class License(BaseModel):
    key: str
    duration_days: int

class RenewLicense(BaseModel):
    username: str
    password: str
    license_key: str

class TransferLicense(BaseModel):
    transfer_username: str
    transfer_duration: int

class ResetPassword(BaseModel):
    current_password: str
    new_password: str

class AdminAction(BaseModel):
    username: str
    action: str  # ban, unban, hwid_reset, add_time, remove_time, freeze_time
    time_days: Optional[int] = None  # Süre ekleme/çıkarma için (isteğe bağlı)