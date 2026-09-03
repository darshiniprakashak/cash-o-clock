import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Cash-O-Clock API")

# Configure CORS so Streamlit can interact with FastAPI safely
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SnoozeRequest(BaseModel):
    penalty_amount: float = 10.0

@app.get("/")
def read_root():
    return {"status": "Cash-O-Clock Backend Running!"}

@app.post("/api/alarm-off")
def turn_alarm_off():
    return {"status": "success", "message": "Alarm turned off! You are awake!"}

@app.post("/api/snooze")
def snooze_alarm(payload: SnoozeRequest):
    return {
        "status": "snoozed",
        "penalty": payload.penalty_amount,
        "message": f"Snoozed! Penalty charged: ₹{payload.penalty_amount}"
    }

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)