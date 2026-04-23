from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import time
import uuid
import os
import sys

# ─── Add project root to path so subpackages resolve correctly ────────────────
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.mongo_client import db_client
from database.redis_client import redis_client
from kafka_stream.producer import activity_producer

app = FastAPI(title="ShopSmart — Recommendation API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─── Data Models ──────────────────────────────────────────────────────────────
class UserEvent(BaseModel):
    user_id: str
    item_id: str
    action_type: str  # click, view, purchase

class UserLogin(BaseModel):
    email: str
    password: str

class UserSignup(BaseModel):
    name: str
    email: str
    password: str


# ─── Health Check ─────────────────────────────────────────────────────────────
@app.get("/health")
async def health():
    """
    Health probe endpoint required by Azure Container Apps.
    Returns status 'ok' if the API process is alive.
    """
    return {"status": "ok", "service": "api"}


# ─── Auth Endpoints ───────────────────────────────────────────────────────────
@app.post("/auth/signup")
async def signup(user: UserSignup):
    existing = db_client.get_user_by_email(user.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = {
        "user_id": f"user_{str(uuid.uuid4())[:8]}",
        "name": user.name,
        "email": user.email,
        "password": user.password,
        "avatar": "👤",
        "age": 25,
        "location": "Unknown"
    }
    db_client.create_user(new_user)
    new_user.pop("_id", None)
    return new_user


@app.post("/auth/login")
async def login(user: UserLogin):
    existing = db_client.get_user_by_email(user.email)
    if not existing or existing.get("password") != user.password:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    existing.pop("_id", None)
    return existing


# ─── Event Endpoint ───────────────────────────────────────────────────────────
@app.post("/event")
async def receive_event(event: UserEvent):
    """
    Receives a user interaction event (view/click/purchase),
    pushes it into the Kafka streaming pipeline for real-time processing,
    and also logs it to MongoDB for historical records.
    """
    event_data = event.model_dump()
    event_data["timestamp"] = time.time()

    # Stream to Kafka for real-time recommendation update
    activity_producer.send_event(event_data)

    # Persist to MongoDB for historical analysis
    db_client.insert_interactions([event_data])

    return {"status": "success", "message": "Event received and queued"}


# ─── Recommendations ──────────────────────────────────────────────────────────
@app.get("/recommendations/{user_id}")
async def get_recommendations(user_id: str):
    """
    Fetches pre-computed top-5 recommendations from Redis cache first.
    Falls back to MongoDB user profile if Redis is empty or unavailable.
    """
    # 1. Try Cache
    recs = redis_client.get_recommendations(user_id)
    if recs:
        return {"user_id": user_id, "recommendations": recs}

    # 2. Fallback to MongoDB persistence (already computed recommendations)
    users = db_client.get_all_users()
    for u in users:
        if u.get("user_id") == user_id:
            db_recs = u.get("recommendations", [])
            if db_recs:
                return {"user_id": user_id, "recommendations": db_recs}

    # 3. Final Fallback: Global Trending (Pre-computed by Worker)
    global_recs = redis_client.get_recommendations("global_trending")
    if global_recs:
        return {"user_id": user_id, "recommendations": global_recs[:5], "fallback": "trending"}

    return {"user_id": user_id, "recommendations": []}


# ─── Items ────────────────────────────────────────────────────────────────────
@app.get("/items")
async def get_items():
    """Returns the full product catalog from MongoDB."""
    items = db_client.get_all_items()
    return {"items": items}


@app.get("/items/{item_id}")
async def get_item(item_id: str):
    """Returns a single product's details."""
    item = db_client.get_item(item_id)
    if item:
        item.pop("_id", None)
        return item
    raise HTTPException(status_code=404, detail="Item not found")


# ─── Users ────────────────────────────────────────────────────────────────────
@app.get("/users")
async def get_users():
    """Returns all community member profiles."""
    users = db_client.get_all_users()
    return {"users": users}


@app.get("/users/{user_id}/history")
async def get_user_history(user_id: str):
    """Returns a user's recent interaction history."""
    interactions = db_client.get_all_interactions()
    user_interactions = [i for i in interactions if i.get("user_id") == user_id]
    user_interactions.sort(key=lambda x: x.get("timestamp", 0), reverse=True)
    return {"history": user_interactions[:10]}
