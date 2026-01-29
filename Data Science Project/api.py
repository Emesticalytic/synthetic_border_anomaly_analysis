"""
UK Border Anomaly Detection - REST API
Real-time ML prediction service for border security screening
"""

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict
import joblib
import numpy as np
import pandas as pd
from datetime import datetime
import logging
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="UK Border Anomaly Detection API",
    description="Real-time ML prediction service for border security screening",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load models
MODEL_PATH = "models/"
MODELS = {}

def load_models():
    """Load all trained models"""
    try:
        model_files = {
            'ensemble': 'ensemble_model.pkl',
            'xgboost': 'xgboost_model.pkl',
            'random_forest': 'random_forest_model.pkl',
            'isolation_forest': 'isolation_forest_model.pkl'
        }
        
        for name, filename in model_files.items():
            path = os.path.join(MODEL_PATH, filename)
            if os.path.exists(path):
                MODELS[name] = joblib.load(path)
                logger.info(f"Loaded {name} model successfully")
            else:
                logger.warning(f"Model file not found: {path}")
        
        if not MODELS:
            logger.error("No models loaded!")
        else:
            logger.info(f"Total models loaded: {len(MODELS)}")
            
    except Exception as e:
        logger.error(f"Error loading models: {str(e)}")
        raise

# Input schema
class PassengerData(BaseModel):
    """Passenger information for anomaly detection"""
    
    # Basic information
    passenger_id: str = Field(..., description="Unique passenger identifier")
    arrival_port: str = Field(..., description="Airport code (e.g., LHR, LGW, MAN)")
    arrival_date: str = Field(..., description="Date in YYYY-MM-DD format")
    
    # Travel details
    origin_country: str = Field(..., description="Country of origin")
    booking_lead_days: int = Field(..., ge=0, le=365, description="Days between booking and travel")
    ticket_type: str = Field(..., description="one_way, return, or multi_city")
    
    # Behavioral features
    previous_visits: int = Field(..., ge=0, description="Number of previous UK visits")
    travel_frequency: float = Field(..., ge=0, description="Visits per year")
    previous_overstays: int = Field(0, ge=0, description="Number of previous overstays")
    
    # Risk indicators
    high_risk_country: bool = Field(False, description="From high-risk country")
    cash_amount: float = Field(0, ge=0, description="Cash declared (GBP)")
    
    # Optional
    age: Optional[int] = Field(None, ge=0, le=120, description="Passenger age")
    gender: Optional[str] = Field(None, description="M, F, or Other")
    
    @validator('arrival_date')
    def validate_date(cls, v):
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError('Date must be in YYYY-MM-DD format')
    
    class Config:
        schema_extra = {
            "example": {
                "passenger_id": "P123456789",
                "arrival_port": "LHR",
                "arrival_date": "2026-02-15",
                "origin_country": "United States",
                "booking_lead_days": 45,
                "ticket_type": "return",
                "previous_visits": 3,
                "travel_frequency": 1.5,
                "previous_overstays": 0,
                "high_risk_country": False,
                "cash_amount": 500.0,
                "age": 35,
                "gender": "M"
            }
        }

# Output schema
class PredictionResponse(BaseModel):
    """Anomaly detection prediction response"""
    passenger_id: str
    is_anomaly: bool
    anomaly_score: float
    risk_level: str
    confidence: float
    model_used: str
    timestamp: str
    recommendations: List[str]
    feature_importance: Optional[Dict[str, float]] = None

# Health check
@app.get("/", tags=["Health"])
async def root():
    """API health check endpoint"""
    return {
        "service": "UK Border Anomaly Detection API",
        "status": "operational",
        "version": "1.0.0",
        "models_loaded": len(MODELS),
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health", tags=["Health"])
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy" if MODELS else "unhealthy",
        "models": list(MODELS.keys()),
        "timestamp": datetime.now().isoformat()
    }

# Feature engineering function
def engineer_features(data: PassengerData) -> pd.DataFrame:
    """Convert passenger data to model features"""
    
    # Parse date
    arrival_date = datetime.strptime(data.arrival_date, '%Y-%m-%d')
    
    # Create feature dictionary
    features = {
        'booking_lead_days': data.booking_lead_days,
        'previous_visits': data.previous_visits,
        'travel_frequency': data.travel_frequency,
        'previous_overstays': data.previous_overstays,
        'cash_amount': data.cash_amount,
        'high_risk_country': int(data.high_risk_country),
        'arrival_month': arrival_date.month,
        'arrival_day_of_week': arrival_date.weekday(),
        'is_weekend': int(arrival_date.weekday() >= 5),
        'is_one_way': int(data.ticket_type == 'one_way'),
        'booking_risk_score': min(100, (365 - data.booking_lead_days) / 3.65),
    }
    
    # Engineered features
    features['visit_overstay_ratio'] = (
        data.previous_overstays / max(1, data.previous_visits)
    )
    features['cash_per_day'] = data.cash_amount / max(1, data.booking_lead_days)
    
    return pd.DataFrame([features])

# Prediction endpoint
@app.post("/predict", response_model=PredictionResponse, tags=["Prediction"])
async def predict_anomaly(
    passenger: PassengerData,
    model_name: str = "ensemble"
):
    """
    Predict if a passenger is an anomaly
    
    - **model_name**: Model to use (ensemble, xgboost, random_forest, isolation_forest)
    """
    try:
        # Validate model selection
        if model_name not in MODELS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Model '{model_name}' not available. Choose from: {list(MODELS.keys())}"
            )
        
        # Engineer features
        features_df = engineer_features(passenger)
        
        # Get model
        model = MODELS[model_name]
        
        # Make prediction
        if hasattr(model, 'predict_proba'):
            prediction = model.predict(features_df)[0]
            probabilities = model.predict_proba(features_df)[0]
            anomaly_score = probabilities[1] if len(probabilities) > 1 else probabilities[0]
            confidence = max(probabilities)
        else:
            # For unsupervised models
            prediction = model.predict(features_df)[0]
            anomaly_score = abs(model.score_samples(features_df)[0])
            confidence = min(1.0, anomaly_score / 2)
            prediction = -1 if prediction == -1 else 0  # Normalize to 0/1
        
        is_anomaly = bool(prediction == 1 or prediction == -1)
        
        # Determine risk level
        if anomaly_score >= 0.8:
            risk_level = "CRITICAL"
        elif anomaly_score >= 0.6:
            risk_level = "HIGH"
        elif anomaly_score >= 0.4:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"
        
        # Generate recommendations
        recommendations = []
        if is_anomaly:
            recommendations.append("Flag for secondary screening")
            if passenger.previous_overstays > 0:
                recommendations.append("Review previous overstay history")
            if passenger.booking_lead_days < 7:
                recommendations.append("Investigate short booking lead time")
            if passenger.high_risk_country:
                recommendations.append("Enhanced document verification required")
            if passenger.cash_amount > 10000:
                recommendations.append("Verify source of funds")
        else:
            recommendations.append("Standard processing")
        
        # Build response
        response = PredictionResponse(
            passenger_id=passenger.passenger_id,
            is_anomaly=is_anomaly,
            anomaly_score=float(anomaly_score),
            risk_level=risk_level,
            confidence=float(confidence),
            model_used=model_name,
            timestamp=datetime.now().isoformat(),
            recommendations=recommendations
        )
        
        logger.info(f"Prediction for {passenger.passenger_id}: {risk_level} (score: {anomaly_score:.3f})")
        
        return response
        
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction failed: {str(e)}"
        )

# Batch prediction endpoint
@app.post("/predict/batch", tags=["Prediction"])
async def predict_batch(
    passengers: List[PassengerData],
    model_name: str = "ensemble"
):
    """
    Predict anomalies for multiple passengers
    """
    results = []
    
    for passenger in passengers:
        try:
            result = await predict_anomaly(passenger, model_name)
            results.append(result.dict())
        except Exception as e:
            logger.error(f"Batch prediction error for {passenger.passenger_id}: {str(e)}")
            results.append({
                "passenger_id": passenger.passenger_id,
                "error": str(e)
            })
    
    return {
        "total": len(passengers),
        "processed": len(results),
        "results": results,
        "timestamp": datetime.now().isoformat()
    }

# Model info endpoint
@app.get("/models", tags=["Models"])
async def list_models():
    """List available models and their details"""
    model_info = {}
    
    for name, model in MODELS.items():
        model_info[name] = {
            "name": name,
            "type": type(model).__name__,
            "loaded": True
        }
    
    return {
        "available_models": model_info,
        "default_model": "ensemble",
        "timestamp": datetime.now().isoformat()
    }

# Startup event
@app.on_event("startup")
async def startup_event():
    """Load models on startup"""
    logger.info("Starting UK Border Anomaly Detection API...")
    load_models()
    logger.info("API ready to serve predictions")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
