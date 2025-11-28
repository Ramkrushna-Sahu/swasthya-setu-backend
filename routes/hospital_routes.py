# routes/hospital_routes.py  ← All dashboard APIs
from fastapi import APIRouter, Depends
from models.schemas import *
from controllers.ai_controller import generate_surge_prediction, generate_recommendations, generate_advisories
from middlewares.auth import get_current_hospital_user
from config.db import db

router = APIRouter(prefix="/hospital", tags=["Hospital"])

@router.get("/global", response_model=GlobalEventData)
async def get_global_events():
    data = await db.global_events.find_one({})
    return data or GlobalEventData()

@router.post("/metrics")
async def update_metrics(metrics: HospitalMetrics, auth=Depends(get_current_hospital_user)):
    await db.metrics.update_one(
        {"hospital_id": auth["hospital_id"]},
        {"$set": {"metrics": metrics.dict(), "updated_at": datetime.utcnow()}},
        upsert=True
    )
    return {"msg": "Metrics updated"}

@router.get("/metrics", response_model=HospitalMetrics)
async def get_metrics(auth=Depends(get_current_hospital_user)):
    doc = await db.metrics.find_one({"hospital_id": auth["hospital_id"]})
    return doc["metrics"] if doc else HospitalMetrics(**{
        "patients_today": 0, "available_beds": 0, "icu_occupancy": 0,
        "oxygen_stock": "Low", "staff_on_duty": 0, "aqi_level": 0,
        "respiratory_cases": 0, "ventilators_available": 0,
        "last_updated": datetime.utcnow().isoformat()
    })

@router.get("/prediction", response_model=SurgePrediction)
async def get_prediction(auth=Depends(get_current_hospital_user)):
    return await generate_surge_prediction(auth["hospital_id"])

@router.get("/recommendations", response_model=Recommendations)
async def get_recommendations(auth=Depends(get_current_hospital_user)):
    return await generate_recommendations(auth["hospital_id"])

@router.get("/advisories", response_model=List[Advisory])
async def get_advisories():
    return await generate_advisories()

@router.post("/ai-query")
async def ai_query(query: dict, auth=Depends(get_current_hospital_user)):
    from controllers.ai_controller import answer_custom_query
    return await answer_custom_query(query["question"], auth["hospital_id"])