from fastapi import FastAPI, Depends, HTTPException, status, WebSocket
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
from datetime import datetime, timedelta
from pydantic import BaseModel
from .dashboard import router as dashboard_router
from .auth import get_current_admin_user
from .realtime_dashboard import handle_dashboard_websocket, dashboard_manager

app = FastAPI(title="PhotoHire API", description="Backend API for PhotoHire Photographer Booking App")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class User(BaseModel):
    email: str
    full_name: str
    user_type: str  # 'customer' or 'photographer'
    is_active: bool = True

class Photographer(BaseModel):
    user_id: str
    portfolio_urls: List[str]
    specialties: List[str]
    hourly_rate: float
    city: str
    current_location: Optional[dict]
    rating: Optional[float]

class Booking(BaseModel):
    id: str
    customer_id: str
    photographer_id: str
    booking_date: datetime
    duration_hours: float
    status: str  # 'pending', 'confirmed', 'completed', 'cancelled'
    location: dict
    total_amount: float

# Routes
@app.get("/")
async def root():
    return {"message": "Welcome to PhotoHire API"}

# User routes
@app.post("/users/", response_model=User)
async def create_user(user: User):
    # TODO: Implement user creation logic
    return user

# Photographer routes
@app.get("/photographers/")
async def get_photographers(city: Optional[str] = None):
    # TODO: Implement photographer listing logic
    return []

@app.get("/photographers/{photographer_id}")
async def get_photographer(photographer_id: str):
    # TODO: Implement single photographer fetch logic
    return {}

# Booking routes
@app.post("/bookings/")
async def create_booking(booking: Booking):
    # TODO: Implement booking creation logic
    return booking

@app.get("/bookings/{booking_id}")
async def get_booking(booking_id: str):
    # TODO: Implement booking fetch logic
    return {}

# Chat routes
@app.post("/chat/send")
async def send_message(sender_id: str, receiver_id: str, message: str):
    # TODO: Implement chat message sending logic
    return {"status": "sent"}

# Location routes
@app.post("/location/update")
async def update_location(photographer_id: str, latitude: float, longitude: float):
    # TODO: Implement location update logic
    return {"status": "updated"}

# WebSocket routes for dashboard
@app.websocket("/ws/dashboard/{client_type}")
async def dashboard_websocket(websocket: WebSocket, client_type: str):
    await handle_dashboard_websocket(websocket, client_type)

# Include dashboard routes
app.include_router(dashboard_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)