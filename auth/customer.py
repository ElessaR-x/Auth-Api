from fastapi import APIRouter, Depends, HTTPException, status
from models import RenewLicense, UserInDB
from utils import save_license, fake_licenses_db, get_license, get_user, fake_users_db, save_user
from auth.auth_utils import get_current_user, check_role
from datetime import datetime, timedelta
# Router oluşturma
router = APIRouter()


# Customer lisans yenileme işlemi
@router.post("/renew_license", tags=["Customer"], summary="Customer lisans yenileme")
async def customer_renew_license(renew_form: RenewLicense):
    # check_role(current_user, "customer")

    user = get_user(fake_users_db, renew_form.username)
    license_expiration = user.license_expiration

    new_license = int(get_license(fake_licenses_db, renew_form.license_key).duration_days)



    try:
        if license_expiration and license_expiration > datetime.utcnow():
            # Lisans süresi geçerli, süresine ekleme yap
            user.license_expiration = license_expiration + timedelta(days=new_license)
        else:
            # Lisans süresi yok veya geçmiş, bugünden itibaren yeni süre başlat
            user.license_expiration = datetime.utcnow() + timedelta(days=new_license)

        save_user(fake_users_db, user)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User has no valid license.")

    if not get_license(fake_licenses_db, renew_form.license_key):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="License not found")

    return {"message": "License renewal successfully"}

