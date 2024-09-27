# utils.py
from models import UserInDB, License
from typing import Optional
from datetime import datetime, timedelta

# Fake user database
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$e/cnM/a5wr.pJkCeV7JzgOOvKvM/Usp0eXqeXvfRthAkm5q4vWxfO",
        # bcrypt hashed password for "password"
        "disabled": False,
        "license_expiration": None
    },
    "arda": {
        "username": "arda",
        "full_name": "Arda",
        "email": "arda@example.com",
        "hashed_password": "$2a$10$DaM3/xzpzN/VscepzEF0O.ko3hEDVPQZtbpcjUrAFuSZvTllB4Emq",  # bcrypt hashed password for "arda"
        "disabled": False,
        "license_expiration": None,
        "role": "owner"
    }
}

# Fake license database
fake_licenses_db = {
    "ABC123": {"key": "ABC123", "duration_days": 30},  # Örnek bir lisans
    "DEF456": {"key": "DEF456", "duration_days": 60},
}


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
        "disabled": False,
    }


def get_license(db, license_key: str) -> Optional[License]:
    if license_key in db:
        license_data = db[license_key]
        return License(**license_data)


def save_license(db, license: License):
    # Lisans kaydetme fonksiyonu
    db[license.key] = {"key": license.key, "duration_days": license.duration_days}