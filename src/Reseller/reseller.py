from fastapi import APIRouter, Depends, HTTPException, status
from models import License, UserInDB
from utils import save_license, fake_licenses_db, get_current_user, check_role

# Router oluşturma
router = APIRouter()


# Reseller lisans oluşturma işlemi (limitli)
@router.post("/create_license", tags=["Reseller"], summary="Reseller lisans oluşturma")
async def reseller_create_license(license: License, current_user: UserInDB = Depends(get_current_user)):
    check_role(current_user, "reseller")

    # Reseller için lisans üretme limiti kontrolü
    license_count = 5  # Örneğin reseller için 5 lisans limiti
    if license_count >= 5:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="License creation limit reached.")

    save_license(fake_licenses_db, license)
    return {"message": "License created successfully", "license": license.key}