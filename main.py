from fastapi import FastAPI
from src.Admin.admin import router as admin_router
from src.Reseller.reseller import router as reseller_router
from src.Owner.owner import router as owner_router
from src.Auth.auth import router as auth_router
from src.Customer.customer import router as customer_router

app = FastAPI()

# Router'ları projeye dahil etme
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(admin_router, prefix="/admin", tags=["Admin"])
app.include_router(reseller_router, prefix="/reseller", tags=["Reseller"])
app.include_router(owner_router, prefix="/owner", tags=["Owner"])
app.include_router(customer_router, prefix="/customer", tags=["Customer"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)