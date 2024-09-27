from fastapi import APIRouter, Depends, HTTPException, status
from models import UserInDB
from utils import get_user, save_user, fake_users_db
from auth.auth_utils import get_current_user, check_role

# Router oluşturma
router = APIRouter()

# Owner kullanıcı rolü değiştirme
@router.post("/change_role", tags=["Owner"], summary="Kullanıcı rolü değiştirme")
async def change_user_role(username: str, new_role: str, current_user: UserInDB = Depends(get_current_user)):
    check_role(current_user, "owner")

    user = get_user(fake_users_db, username)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user.role = new_role
    save_user(fake_users_db, user)
    return {"message": f"User {username}'s role has been changed to {new_role}"}