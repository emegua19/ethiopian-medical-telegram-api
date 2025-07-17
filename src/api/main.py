# src/api/main.py

from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from .database import SessionLocal
from . import crud, schemas

app = FastAPI(title="Ethiopian Medical Telegram API")

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# === Endpoints ===

@app.get("/api/reports/top-products", response_model=list[schemas.Detection])
def get_top_detections(limit: int = Query(10, ge=1), db: Session = Depends(get_db)):
    return crud.get_top_detections(db, limit)

@app.get("/api/channels/{channel_name}/activity", response_model=schemas.ChannelActivity)
def get_channel_activity(channel_name: str, db: Session = Depends(get_db)):
    return crud.get_channel_activity(db, channel_name)

@app.get("/api/search/messages", response_model=list[schemas.Message])
def search_messages(query: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    return crud.search_messages(db, query)

@app.get("/")
def root():
    return {"message": "🩺 Telegram Medical API is live!"}