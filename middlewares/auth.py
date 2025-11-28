# middlewares/auth.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from config.config import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/staff/login")

async def get_current_hospital_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        hospital_id = payload.get("hospital_id")
        if not hospital_id:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        return payload  # return full payload
    except JWTError as e:
        raise HTTPException(status_code=401, detail="Invalid or expired token")