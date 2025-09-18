"""
Krishi Sakhi Backend - FastAPI Application
AI-Powered Farming Assistant for Kerala Farmers
"""

from fastapi import FastAPI, HTTPException, Depends, status, UploadFile, File
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
from typing import List, Optional
import sqlite3
import json
import os
from datetime import datetime, timedelta, timezone
import hashlib
import jwt
from pydantic import BaseModel
import asyncio

# Import our modules
from models.database import init_db, get_db_connection
from services.ai_service import AIService
from services.weather_service import WeatherService
from utils.translations import get_translation

# Initialize services
ai_service = AIService()
weather_service = WeatherService()
security = HTTPBearer()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    init_db()
    yield
    # Shutdown
    pass

app = FastAPI(
    title="Krishi Sakhi API",
    description="AI-Powered Farming Assistant for Kerala Farmers",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class FarmerCreate(BaseModel):
    name: str
    phone: str
    email: str
    password: str
    location: str
    language: str = "en"

class FarmerLogin(BaseModel):
    phone: str
    password: str

class FarmCreate(BaseModel):
    name: str
    location: str
    land_size: float
    soil_type: str
    irrigation_type: str
    crop_types: List[str]

class ActivityCreate(BaseModel):
    farm_id: int
    activity_type: str
    description: str
    date: str
    crop_name: Optional[str] = None
    quantity: Optional[float] = None
    cost: Optional[float] = None
    notes: Optional[str] = None

class DiseaseDetection(BaseModel):
    image_path: str
    farm_id: int
    crop_name: str

class ChatMessage(BaseModel):
    message: str
    language: str = "en"
    farmer_id: Optional[int] = None

# JWT utilities
SECRET_KEY = "krishi-sakhi-secret-key-change-in-production"
ALGORITHM = "HS256"

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=30)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        farmer_id_str = payload.get("sub")
        if farmer_id_str is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        farmer_id = int(farmer_id_str)
        return farmer_id
    except (jwt.PyJWTError, ValueError) as e:
        raise HTTPException(status_code=401, detail="Invalid token")

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

# Auth endpoints
@app.post("/api/auth/register")
async def register(farmer: FarmerCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if farmer exists
    cursor.execute("SELECT id FROM farmers WHERE phone = ? OR email = ?", 
                   (farmer.phone, farmer.email))
    if cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="Farmer already exists")
    
    # Create farmer
    hashed_password = hash_password(farmer.password)
    cursor.execute("""
        INSERT INTO farmers (name, phone, email, password_hash, location, language)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (farmer.name, farmer.phone, farmer.email, hashed_password, 
          farmer.location, farmer.language))
    
    farmer_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    token = create_access_token({"sub": str(farmer_id)})
    return {"access_token": token, "token_type": "bearer", "farmer_id": farmer_id}

@app.post("/api/auth/login")
async def login(credentials: FarmerLogin):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, password_hash FROM farmers WHERE phone = ?
    """, (credentials.phone,))
    
    farmer = cursor.fetchone()
    conn.close()
    
    if not farmer or hash_password(credentials.password) != farmer[1]:
        # For demo purposes, allow any password
        cursor = get_db_connection().cursor()
        cursor.execute("SELECT id FROM farmers WHERE phone = ?", (credentials.phone,))
        demo_farmer = cursor.fetchone()
        if demo_farmer:
            token = create_access_token({"sub": str(demo_farmer[0])})
            return {"access_token": token, "token_type": "bearer", "farmer_id": demo_farmer[0]}
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token({"sub": str(farmer[0])})
    return {"access_token": token, "token_type": "bearer", "farmer_id": farmer[0]}

# Demo login endpoint
@app.post("/api/auth/demo-login")
async def demo_login():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create demo farmer if not exists
    cursor.execute("SELECT id FROM farmers WHERE phone = ?", ("+919876543210",))
    farmer = cursor.fetchone()
    
    if not farmer:
        cursor.execute("""
            INSERT INTO farmers (name, phone, email, password_hash, location, language)
            VALUES (?, ?, ?, ?, ?, ?)
        """, ("Demo Farmer", "+919876543210", "demo@krishisakhi.com", 
              hash_password("demo123"), "Kottayam", "en"))
        farmer_id = cursor.lastrowid
    else:
        farmer_id = farmer[0]
    
    conn.commit()
    conn.close()
    
    token = create_access_token({"sub": str(farmer_id)})
    return {"access_token": token, "token_type": "bearer", "farmer_id": farmer_id}

# Farmer endpoints
@app.get("/api/farmers/profile")
async def get_profile(farmer_id: int = Depends(verify_token)):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, name, phone, email, location, language, created_at
        FROM farmers WHERE id = ?
    """, (farmer_id,))
    
    farmer = cursor.fetchone()
    conn.close()
    
    if not farmer:
        raise HTTPException(status_code=404, detail="Farmer not found")
    
    return {
        "id": farmer[0],
        "name": farmer[1],
        "phone": farmer[2],
        "email": farmer[3],
        "location": farmer[4],
        "language": farmer[5],
        "created_at": farmer[6]
    }

# Farm endpoints
@app.post("/api/farms")
async def create_farm(farm: FarmCreate, farmer_id: int = Depends(verify_token)):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO farms (farmer_id, name, location, land_size, soil_type, irrigation_type, crop_types)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (farmer_id, farm.name, farm.location, farm.land_size, 
          farm.soil_type, farm.irrigation_type, json.dumps(farm.crop_types)))
    
    farm_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return {"farm_id": farm_id, "message": "Farm created successfully"}

@app.get("/api/farms")
async def get_farms(farmer_id: int = Depends(verify_token)):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, name, location, land_size, soil_type, irrigation_type, crop_types, created_at
        FROM farms WHERE farmer_id = ?
    """, (farmer_id,))
    
    farms = cursor.fetchall()
    conn.close()
    
    return [{
        "id": farm[0],
        "name": farm[1],
        "location": farm[2],
        "land_size": farm[3],
        "soil_type": farm[4],
        "irrigation_type": farm[5],
        "crop_types": json.loads(farm[6]) if farm[6] else [],
        "created_at": farm[7]
    } for farm in farms]

# Activity endpoints
@app.post("/api/activities")
async def create_activity(activity: ActivityCreate, farmer_id: int = Depends(verify_token)):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Verify farm belongs to farmer
    cursor.execute("SELECT farmer_id FROM farms WHERE id = ?", (activity.farm_id,))
    farm = cursor.fetchone()
    if not farm or farm[0] != farmer_id:
        conn.close()
        raise HTTPException(status_code=403, detail="Farm not found or access denied")
    
    cursor.execute("""
        INSERT INTO activities (farm_id, activity_type, description, date, crop_name, quantity, cost, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (activity.farm_id, activity.activity_type, activity.description, 
          activity.date, activity.crop_name, activity.quantity, activity.cost, activity.notes))
    
    activity_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return {"activity_id": activity_id, "message": "Activity recorded successfully"}

@app.get("/api/activities")
async def get_activities(farmer_id: int = Depends(verify_token), farm_id: Optional[int] = None):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if farm_id:
        # Verify farm belongs to farmer
        cursor.execute("SELECT farmer_id FROM farms WHERE id = ?", (farm_id,))
        farm = cursor.fetchone()
        if not farm or farm[0] != farmer_id:
            conn.close()
            raise HTTPException(status_code=403, detail="Farm not found or access denied")
        
        cursor.execute("""
            SELECT a.id, a.activity_type, a.description, a.date, a.crop_name, 
                   a.quantity, a.cost, a.notes, f.name as farm_name
            FROM activities a
            JOIN farms f ON a.farm_id = f.id
            WHERE a.farm_id = ?
            ORDER BY a.date DESC
        """, (farm_id,))
    else:
        cursor.execute("""
            SELECT a.id, a.activity_type, a.description, a.date, a.crop_name, 
                   a.quantity, a.cost, a.notes, f.name as farm_name
            FROM activities a
            JOIN farms f ON a.farm_id = f.id
            WHERE f.farmer_id = ?
            ORDER BY a.date DESC
        """, (farmer_id,))
    
    activities = cursor.fetchall()
    conn.close()
    
    return [{
        "id": activity[0],
        "activity_type": activity[1],
        "description": activity[2],
        "date": activity[3],
        "crop_name": activity[4],
        "quantity": activity[5],
        "cost": activity[6],
        "notes": activity[7],
        "farm_name": activity[8]
    } for activity in activities]

# AI endpoints
@app.post("/api/ai/detect-disease")
async def detect_disease(detection: DiseaseDetection, farmer_id: int = Depends(verify_token)):
    try:
        # Verify farm belongs to farmer
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT farmer_id FROM farms WHERE id = ?", (detection.farm_id,))
        farm = cursor.fetchone()
        if not farm or farm[0] != farmer_id:
            conn.close()
            raise HTTPException(status_code=403, detail="Farm not found or access denied")
        conn.close()
        
        result = await ai_service.detect_disease(detection.image_path, detection.crop_name)
        
        # Store detection result
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO disease_detections (farm_id, crop_name, disease_name, confidence, 
                                          symptoms, treatment, image_path)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (detection.farm_id, detection.crop_name, result['disease'], result['confidence'],
              json.dumps(result['symptoms']), json.dumps(result['treatment']), detection.image_path))
        
        conn.commit()
        conn.close()
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/ai/chat")
async def ai_chat(message: ChatMessage):
    try:
        response = await ai_service.chat_response(message.message, message.language)
        return {"response": response, "language": message.language}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Weather endpoints
@app.get("/api/weather")
async def get_weather(location: str, farmer_id: int = Depends(verify_token)):
    try:
        weather_data = await weather_service.get_weather_forecast(location)
        advisory = await weather_service.get_farming_advisory(weather_data, location)
        
        return {
            "weather": weather_data,
            "advisory": advisory
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Knowledge base endpoints
@app.get("/api/knowledge/crops")
async def get_crops_info(language: str = "en"):
    # Sample crop data for Kerala
    crops_data = {
        "en": {
            "Rice": {
                "description": "Staple food crop of Kerala",
                "seasons": "Kharif, Rabi, Summer",
                "yield": "4-6 tons/hectare",
                "varieties": ["Jyothi", "Uma", "Thriveni", "JGL 1798"]
            },
            "Coconut": {
                "description": "Primary plantation crop",
                "seasons": "Year-round",
                "yield": "80-150 nuts/palm/year",
                "varieties": ["West Coast Tall", "Chandra Kalpa", "Kera Chandra"]
            },
            "Black Pepper": {
                "description": "King of spices",
                "seasons": "May-June planting",
                "yield": "2-5 kg/vine",
                "varieties": ["Panniyur-1", "Subhakara", "Pournami"]
            }
        },
        "ml": {
            "നെല്ല്": {
                "description": "കേരളത്തിന്റെ പ്രധാന ഭക്ഷ്യവിള",
                "seasons": "ഖരിഫ്, റബി, സമ്മർ",
                "yield": "4-6 ടൺ/ഹെക്ടർ",
                "varieties": ["ജ്യോതി", "ഉമ", "ത്രിവേണി", "JGL 1798"]
            },
            "തെങ്ങ്": {
                "description": "പ്രാഥമിക തോട്ടവിള",
                "seasons": "വർഷം മുഴുവൻ",
                "yield": "80-150 കായ്/തെങ്ങ്/വർഷം",
                "varieties": ["വെസ്റ്റ് കോസ്റ്റ് ടാൾ", "ചന്ദ്ര കൽപ", "കേര ചന്ദ്ര"]
            },
            "കുരുമുളക്": {
                "description": "മസാലകളുടെ രാജാവ്",
                "seasons": "മേയ്-ജൂൺ നടീൽ",
                "yield": "2-5 കിലോ/വൈൻ",
                "varieties": ["പന്നിയൂർ-1", "സുഭാകര", "പൗർണ്ണമി"]
            }
        }
    }
    return crops_data.get(language, crops_data.get("en", {}))

@app.get("/api/knowledge/diseases")
async def get_diseases_info(language: str = "en"):
    # Sample disease data
    diseases_data = {
        "en": {
            "Rice Blast": {
                "crop": "Rice",
                "symptoms": ["Diamond-shaped lesions", "White to gray centers", "Neck rot"],
                "treatment": ["Tricyclazole fungicide", "Resistant varieties", "Proper drainage"],
                "prevention": ["Avoid excessive nitrogen", "Water management", "Disease-free seeds"]
            },
            "Coconut Leaf Rot": {
                "crop": "Coconut",
                "symptoms": ["Yellow to brown spots", "Wilting leaves", "Premature fall"],
                "treatment": ["Copper fungicide", "Remove affected leaves", "Air circulation"],
                "prevention": ["Avoid overhead irrigation", "Proper spacing", "Regular sanitation"]
            }
        },
        "ml": {
            "നെല്ല് ബ്ലാസ്റ്റ്": {
                "crop": "നെല്ല്",
                "symptoms": ["ഡയമണ്ട് ആകൃതിയിലുള്ള പരുക്കുകൾ", "വെളുത്ത മുതൽ ചാര നിറത്തിലുള്ള കേന്ദ്രം", "കഴുത്ത് ക്ഷയം"],
                "treatment": ["ട്രൈസൈക്ലാസോൾ കീടനാശിനി", "പ്രതിരോധ ഇനങ്ങൾ", "നല്ല വാരിനീക്കൽ"],
                "prevention": ["അമിത നൈട്രജൻ ഒഴിവാക്കുക", "ജല മാനേജ്മെന്റ്", "രോഗരഹിത വിത്തുകൾ"]
            },
            "തെങ്ങ് ഇല ക്ഷയം": {
                "crop": "തെങ്ങ്",
                "symptoms": ["മഞ്ഞ മുതൽ തവിട്ട് നിറത്തിലുള്ള പരുക്കുകൾ", "വാടിയ ഇലകൾ", "അകാല ഇലപൊഴിയൽ"],
                "treatment": ["കോപ്പർ കീടനാശിനി", "ബാധിത ഇലകൾ നീക്കം ചെയ്യുക", "വായു സഞ്ചാരം"],
                "prevention": ["മുകളിൽ നിന്നുള്ള നീരാവി ഒഴിവാക്കുക", "ശരിയായ അകലം", "നിരന്തര ശുചിത്വം"]
            }
        }
    }
    return diseases_data.get(language, diseases_data.get("en", {}))

@app.get("/api/knowledge/schemes")
async def get_government_schemes(language: str = "en"):
    from utils.translations import get_government_schemes
    return get_government_schemes(language)

# Community endpoints
@app.get("/api/community/alerts")
async def get_community_alerts(location: Optional[str] = None, language: str = "en"):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if location:
        cursor.execute("""
            SELECT dd.disease_name, dd.confidence, dd.crop_name, f.location, 
                   dd.created_at, COUNT(*) as occurrences
            FROM disease_detections dd
            JOIN farms f ON dd.farm_id = f.id
            WHERE f.location LIKE ? AND dd.created_at >= date('now', '-30 days')
            GROUP BY dd.disease_name, dd.crop_name, f.location
            HAVING COUNT(*) >= 2
            ORDER BY occurrences DESC, dd.created_at DESC
        """, (f"%{location}%",))
    else:
        cursor.execute("""
            SELECT dd.disease_name, dd.confidence, dd.crop_name, f.location, 
                   dd.created_at, COUNT(*) as occurrences
            FROM disease_detections dd
            JOIN farms f ON dd.farm_id = f.id
            WHERE dd.created_at >= date('now', '-30 days')
            GROUP BY dd.disease_name, dd.crop_name, f.location
            HAVING COUNT(*) >= 2
            ORDER BY occurrences DESC, dd.created_at DESC
        """)
    
    alerts = cursor.fetchall()
    conn.close()
    
    return [{
        "disease": alert[0],
        "confidence": alert[1],
        "crop": alert[2],
        "location": alert[3],
        "date": alert[4],
        "occurrences": alert[5]
    } for alert in alerts]

# Analytics endpoints
@app.get("/api/analytics/dashboard")
async def get_dashboard_analytics(farmer_id: int = Depends(verify_token)):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get farm count
    cursor.execute("SELECT COUNT(*) FROM farms WHERE farmer_id = ?", (farmer_id,))
    farm_count = cursor.fetchone()[0]
    
    # Get recent activities count
    cursor.execute("""
        SELECT COUNT(*) FROM activities a
        JOIN farms f ON a.farm_id = f.id
        WHERE f.farmer_id = ? AND a.date >= date('now', '-30 days')
    """, (farmer_id,))
    recent_activities = cursor.fetchone()[0]
    
    # Get total cost this month
    cursor.execute("""
        SELECT COALESCE(SUM(a.cost), 0) FROM activities a
        JOIN farms f ON a.farm_id = f.id
        WHERE f.farmer_id = ? AND a.date >= date('now', 'start of month')
    """, (farmer_id,))
    monthly_cost = cursor.fetchone()[0]
    
    # Get activity types distribution
    cursor.execute("""
        SELECT a.activity_type, COUNT(*) FROM activities a
        JOIN farms f ON a.farm_id = f.id
        WHERE f.farmer_id = ? AND a.date >= date('now', '-30 days')
        GROUP BY a.activity_type
    """, (farmer_id,))
    activity_types = dict(cursor.fetchall())
    
    # Get monthly costs trend
    cursor.execute("""
        SELECT strftime('%Y-%m', a.date) as month, COALESCE(SUM(a.cost), 0) as total_cost
        FROM activities a
        JOIN farms f ON a.farm_id = f.id
        WHERE f.farmer_id = ? AND a.date >= date('now', '-12 months')
        GROUP BY month
        ORDER BY month
    """, (farmer_id,))
    monthly_trends = [{"month": row[0], "cost": row[1]} for row in cursor.fetchall()]
    
    conn.close()
    
    return {
        "farm_count": farm_count,
        "recent_activities": recent_activities,
        "monthly_cost": monthly_cost,
        "activity_distribution": activity_types,
        "cost_trends": monthly_trends
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)