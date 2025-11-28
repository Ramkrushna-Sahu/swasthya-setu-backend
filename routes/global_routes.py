# routes/global_routes.py  ← Head enters this from frontend
from fastapi import APIRouter
from models.schemas import GlobalEventData
from config.db import db

router = APIRouter(prefix="/global", tags=["Global"])

@router.post("/update")
async def update_global(data: GlobalEventData):
    await db.global_events.replace_one({}, data.dict(), upsert=True)
    return {"msg": "Global events updated"}

@router.get("")
async def get_global():
    data = await db.global_events.find_one({})
    return data or GlobalEventData().dict()