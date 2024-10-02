from fastapi import FastAPI, Request
from src.Admin.admin import router as admin_router
from src.Reseller.reseller import router as reseller_router
from src.Owner.owner import router as owner_router
from src.Auth.auth import router as auth_router
from src.Customer.customer import router as customer_router
import uvicorn
import logging
import time

# Logging ayarlarını yapılandırma
logging.basicConfig(
    filename='app.log',  # Log dosyasının adı
    level=logging.INFO,  # Log seviyesi
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log formatı
)

app = FastAPI()

# Router'ları projeye dahil etme
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(admin_router, prefix="/admin", tags=["Admin"])
app.include_router(reseller_router, prefix="/reseller", tags=["Reseller"])
app.include_router(owner_router, prefix="/owner", tags=["Owner"])
app.include_router(customer_router, prefix="/customer", tags=["Customer"])

# Request middleware'i ekleyerek her isteği loglama
@app.middleware("http")
async def log_requests(request: Request, call_next):
    # İstek zamanı ve URL bilgilerini alalım
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    log_details = f"METHOD: {request.method} - URL: {request.url} - STATUS CODE: {response.status_code} - PROCESS TIME: {process_time:.2f}s"
    logging.info(log_details)
    return response

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
