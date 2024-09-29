from fastapi import FastAPI
from auth.admin import router as admin_router
from auth.reseller import router as reseller_router
from auth.owner import router as owner_router
from auth.auth import router as auth_router
from auth.customer import router as customer_router

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