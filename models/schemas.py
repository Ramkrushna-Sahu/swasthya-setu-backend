from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime

# === Global Data (entered by Head) ===
class FestivalData(BaseModel):
    festival: str
    start_date: str
    duration_days: int
    crowd_impact: str
    injury_risk: str
    respiratory_impact: str
    notes: str

class PollutionData(BaseModel):
    aqi: int
    pm2_5: int
    pm10: int
    category: str
    start_date: str
    duration_days: int
    notes: str

class EpidemicData(BaseModel):
    disease: str
    severity: str
    spread_level: str
    expected_surge_percent: int
    notes: str

class GlobalEventData(BaseModel):
    festival_data: Optional[FestivalData] = None
    pollution_data: Optional[PollutionData] = None
    epidemic_data: Optional[EpidemicData] = None

# === Hospital Real-Time Metrics ===
class HospitalMetrics(BaseModel):
    patients_today: int
    available_beds: int
    icu_occupancy: int
    oxygen_stock: str
    staff_on_duty: int
    aqi_level: int
    respiratory_cases: int
    ventilators_available: int
    last_updated: str

# === Surge Prediction ===
class SurgeDay(BaseModel):
    date: str
    expected_patients: int
    confidence: int
    alert: str
    reason: Optional[str] = None

class SurgePrediction(BaseModel):
    next_7_days: List[SurgeDay]
    factors: List[str]

# === Recommendations & Advisories ===
class PriorityAction(BaseModel):
    action: str
    priority: str
    deadline: str

class Recommendations(BaseModel):
    staffing: str
    supplies: str
    advisory: str
    priority_actions: List[PriorityAction]
    resource_allocation: Dict[str, str]

class Advisory(BaseModel):
    id: str
    title: str
    type: str
    severity: str
    message: str
    date: str
    target_audience: str
    action_required: str

# === Auth Models ===
class HospitalRegister(BaseModel):
    hospital_name: str
    hospital_code: str        # e.g. AIIMS-DEL
    location: Optional[str] = None
    admin_username: str
    admin_password: str

class StaffCreate(BaseModel):
    name: str
    username: str
    password: str
    role: str                 # admin, doctor, staff, analyst

class Token(BaseModel):
    access_token: str
    token_type: str