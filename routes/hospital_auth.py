# routes/hospital_auth.py  ← REPLACE 100%
from fastapi import APIRouter, HTTPException, status
from models.schemas import HospitalRegister
from config.db import db
from passlib.context import CryptContext
from datetime import datetime

router = APIRouter(prefix="/hospital", tags=["Hospital Auth"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/register")
async def register_hospital(data: HospitalRegister):
    # 1. Check duplicate
    if await db.hospitals.find_one({"hospital_code": data.hospital_code.upper()}):
        raise HTTPException(
            status_code=400,
            detail="Hospital code already exists. Choose another."
        )

    # 2. Safe password
    safe_password = data.admin_password[:72]

    # 3. Insert hospital
    hospital_result = await db.hospitals.insert_one({
        "hospital_name": data.hospital_name,
        "hospital_code": data.hospital_code.upper(),
        "location": data.location or "Not provided",
        "created_at": datetime.utcnow()
    })

    hospital_id_str = str(hospital_result.inserted_id)  # ← Convert immediately

    # 4. Create admin user
    await db.users.insert_one({
        "hospital_id": hospital_id_str,        # ← STRING, NOT ObjectId
        "username": data.admin_username.lower(),
        "password_hash": pwd_context.hash(safe_password),
        "role": "admin",
        "is_active": True,
        "created_at": datetime.utcnow()
    })

    # 5. RETURN ONLY PRIMITIVES — NO Pydantic, NO ObjectId → 100% SAFE
    return {
        "success": True,
        "message": "Hospital registered successfully!",
        "hospital_code": data.hospital_code.upper(),
        "admin_login": f"{data.admin_username.lower()}@{data.hospital_code.upper()}",
        "password_hint": "Use the password you just set"
    }