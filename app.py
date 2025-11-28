# app.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.hospital_auth import router as hospital_auth_router
from routes.staff_auth import router as staff_auth_router
from routes.global_routes import router as global_router
from routes.hospital_routes import router as hospital_router

app = FastAPI(title="SwasthyaSetu Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(hospital_auth_router)
app.include_router(staff_auth_router)
app.include_router(global_router)
app.include_router(hospital_router)

@app.get("/")
def home():
    return {"message": "SwasthyaSetu Backend is LIVE!"}