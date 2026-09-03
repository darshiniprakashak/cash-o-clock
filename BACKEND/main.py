from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import urllib.parse
import uuid

app = FastAPI(title="Cash-O-Clock Live Transaction API")

DEFAULT_DESTINATION_UPI = "yourname@okaxis"

class SnoozeRequest(BaseModel):
    penalty: int
    target_upi: Optional[str] = DEFAULT_DESTINATION_UPI

@app.get("/")
def health_check():
    return {"status": "Cash-O-Clock API Active"}

@app.post("/api/snooze")
def process_snooze(data: SnoozeRequest):
    if data.penalty < 5 or data.penalty > 100:
        raise HTTPException(status_code=400, detail="Penalty must be between ₹5 and ₹100.")

    target = data.target_upi if data.target_upi else DEFAULT_DESTINATION_UPI

    # Generates standard NPCI UPI link required for QR generation
    params = {
        "pa": target,
        "pn": "Cash-O-Clock Fine",
        "am": str(data.penalty),
        "cu": "INR",
        "tn": f"Snooze Penalty Fee (₹{data.penalty})"
    }
    upi_link = f"upi://pay?{urllib.parse.urlencode(params)}"

    return {
        "status": "success",
        "amount": data.penalty,
        "recipient": target,
        "upi_link": upi_link,
        "transaction_ref": f"REF_{uuid.uuid4().hex[:8].upper()}"
    }

@app.post("/api/alarm-off")
def process_alarm_off():
    return {"message": "Alarm turned off on time! Zero funds debited."}