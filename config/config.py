# config/config.py
import os
from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "swasthyasetu-secret-2025-final")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440   # 24 hours
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://localhost:3000")