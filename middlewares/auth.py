# middlewares/auth.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from config.config import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/staff/login")

async def get_current_hospital_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        hospital_id: str = payload.get("hospital_id")
        role: str = payload.get("role")
        if not hospital_id:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {
            "hospital_id": hospital_id,
            "role": role,
            "username": payload.get("username"),
            "hospital_name": payload.get("hospital_name")
        }
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")