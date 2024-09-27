from fastapi import APIRouter, Depends, HTTPException, status
from datetime import timedelta, datetime
from models import UserInDB
from utils import fake_users_db, get_user, save_user
from auth.auth_utils import get_current_user, check_minimum_role

# Router oluşturma
router = APIRouter()


# Kullanıcıyı banlama
@router.post("/ban", tags=["Admin"], summary="Kullanıcıyı banlama")
async def ban_user(username: str, current_user: UserInDB = Depends(get_current_user)):
    # Sadece admin ve owner bu işlemi yapabilir
    check_minimum_role(current_user, ["admin", "owner"])

    user = get_user(fake_users_db, username)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user.disabled = True
    save_user(fake_users_db, user)
    return {"message": f"User {username} has been banned."}


# Kullanıcının banını kaldırma
@router.post("/unban", tags=["Admin"], summary="Kullanıcının banını kaldırma")
async def unban_user(username: str, current_user: UserInDB = Depends(get_current_user)):
    check_minimum_role(current_user, ["admin", "owner"])

    user = get_user(fake_users_db, username)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user.disabled = False
    save_user(fake_users_db, user)
    return {"message": f"User {username} has been unbanned."}


# HWID sıfırlama
@router.post("/hwid_reset", tags=["Admin"], summary="HWID sıfırlama")
async def hwid_reset(username: str, current_user: UserInDB = Depends(get_current_user)):
    check_minimum_role(current_user, ["admin", "owner"])

    user = get_user(fake_users_db, username)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # HWID sıfırlama işlemi
    save_user(fake_users_db, user)
    return {"message": f"User {username}'s HWID has been reset."}


# Kullanıcıya süre ekleme
@router.post("/add_time", tags=["Admin"], summary="Kullanıcıya süre ekleme")
async def add_time(username: str, time_days: int, current_user: UserInDB = Depends(get_current_user)):
    check_minimum_role(current_user, ["admin", "owner"])

    user = get_user(fake_users_db, username)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if user.license_expiration:
        user.license_expiration = user.license_expiration + timedelta(days=time_days)
    else:
        user.license_expiration = datetime.utcnow() + timedelta(days=time_days)

    save_user(fake_users_db, user)
    return {"message": f"{time_days} days have been added to user {username}'s license."}


# Kullanıcının süresinden çıkarma
@router.post("/remove_time", tags=["Admin"], summary="Kullanıcının süresinden çıkarma")
async def remove_time(username: str, time_days: int, current_user: UserInDB = Depends(get_current_user)):
    check_minimum_role(current_user, ["admin", "owner"])

    user = get_user(fake_users_db, username)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if user.license_expiration:
        user.license_expiration = user.license_expiration - timedelta(days=time_days)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="User has no valid license to remove time from.")

    save_user(fake_users_db, user)
    return {"message": f"{time_days} days have been removed from user {username}'s license."}


# Kullanıcının süresini dondurma
@router.post("/freeze_time", tags=["Admin"], summary="Kullanıcının süresini dondurma")
async def freeze_time(username: str, current_user: UserInDB = Depends(get_current_user)):
    check_minimum_role(current_user, ["admin", "owner"])

    user = get_user(fake_users_db, username)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user.license_expiration = None
    save_user(fake_users_db, user)
    return {"message": f"User {username}'s license time has been frozen."}