# routes/staff_auth.py
from fastapi import APIRouter, Depends, HTTPException, status
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
    print(username, password)
    if "@" not in username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid format. Use: username@HOSPITAL_CODE"
        )

    user_part, hospital_code = username.rsplit("@", 1)

    hospital = await db.hospitals.find_one({"hospital_code": hospital_code.upper()})
    if not hospital:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hospital not found"
        )

    user = await db.users.find_one({
        "hospital_id": str(hospital["_id"]),
        "username": user_part
    })
    print(user)
    if not user or not pwd_context.verify(password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    access_token = jwt.encode({
        "hospital_id": str(hospital["_id"]),
        "hospital_name": hospital["hospital_name"],
        "username": user["username"],
        "role": user["role"],
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }, SECRET_KEY, algorithm=ALGORITHM)

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/staff/add")
async def add_staff(
    staff_data: StaffCreate,
    current_user=Depends(get_current_hospital_user)
):
    # This dependency automatically returns 401 if token is invalid
    if not current_user or current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only hospital admin can add staff members"
        )

    # Check if username already exists
    exists = await db.users.find_one({
        "hospital_id": current_user["hospital_id"],
        "username": staff_data.username.strip().lower()
    })
    if exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists in this hospital"
        )

    # Create new staff member
    await db.users.insert_one({
        "hospital_id": current_user["hospital_id"],
        "username": staff_data.username.strip().lower(),
        "password_hash": pwd_context.hash(staff_data.password),
        "name": staff_data.name.strip(),
        "role": staff_data.role.strip().lower(),
        "is_active": True,
        "created_at": datetime.utcnow()
    })

    return {
        "success": True,
        "message": f"{staff_data.role.capitalize()} '{staff_data.name}' added successfully!",
        "username": staff_data.username.strip().lower()
    }