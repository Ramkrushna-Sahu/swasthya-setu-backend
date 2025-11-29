# In your routes/global.py or main.py

from fastapi import APIRouter, Depends
from models.schemas import GlobalEventData
from middlewares.auth import get_current_hospital_user  # ← only "head" role
from config.db import db
router = APIRouter(prefix="/global", tags=["Global Events"])

@router.post("/update")
async def update_global_events(
    data: GlobalEventData,
    current_user = Depends(get_current_hospital_user)
):
    # Save to MongoDB (or Redis for real-time)
    print(data)
    await db.global_events.update_one(
        {"active": True},
        {"$set": data.dict(exclude_unset=True)},  # ← This ignores null/empty fields
        upsert=True
    )
    return {"success": True, "message": "National alert updated & broadcasted to all hospitals"}