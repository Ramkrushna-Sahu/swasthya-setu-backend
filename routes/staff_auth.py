# routes/staff_auth.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from models.schemas import Token, StaffCreate
from config.db import db
from config.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from middlewares.auth import get_current_hospital_user
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

router = APIRouter(prefix="/auth", tags=["Auth"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/staff/login", response_model=Token)
async def staff_login(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username.strip().lower()
    password = form_data.password

    if "@" not in username:
        raise HTTPException(400, "Use format: username@HOSPITAL_CODE")

    user_part, code = username.rsplit("@", 1)
    hospital = await db.hospitals.find_one({"hospital_code": code.upper()})
    if not hospital:
        raise HTTPException(404, "Hospital not found")

    user = await db.users.find_one({
        "hospital_id": str(hospital["_id"]),
        "username": user_part
    })
    if not user or not pwd_context.verify(password, user["password_hash"]):
        raise HTTPException(401, "Invalid credentials")

    access_token = jwt.encode({
        "hospital_id": str(hospital["_id"]),
        "hospital_name": hospital["hospital_name"],
        "username": user["username"],
        "role": user["role"],
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }, SECRET_KEY, algorithm=ALGORITHM)

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/staff/add")
async def add_staff(staff_data: StaffCreate, current_user=Depends(get_current_hospital_user)):
    if current_user.get("role") != "admin":
        raise HTTPException(403, "Only admin can add staff")

    exists = await db.users.find_one({
        "hospital_id": current_user["hospital_id"],
        "username": staff_data.username.lower()
    })
    if exists:
        raise HTTPException(400, "Username already exists")

    await db.users.insert_one({
        "hospital_id": current_user["hospital_id"],
        "username": staff_data.username.lower(),
        "password_hash": pwd_context.hash(staff_data.password),
        "name": staff_data.name,
        "role": staff_data.role.lower(),
        "is_active": True,
        "created_at": datetime.utcnow()
    })

    return {"success": True, "message": "Staff added successfully!"}