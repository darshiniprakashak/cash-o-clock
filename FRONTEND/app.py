import os
import requests
import streamlit as st
import qrcode
from PIL import Image

st.set_page_config(page_title="Cash-O-Clock", page_icon="⏰", layout="centered")

# Read dynamic backend URL (defaults to local, overridden by Streamlit Secrets)
RAW_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
BACKEND_URL = RAW_URL.rstrip("/")

st.title("⏰ Cash-O-Clock")
st.caption("The alarm clock that hurts your wallet when you snooze.")

# Initialize session state variables
if "is_ringing" not in st.session_state:
    st.session_state.is_ringing = True
if "wake_success" not in st.session_state:
    st.session_state.wake_success = None

# Show success notification if alarm was disabled
if st.session_state.wake_success:
    st.balloons()
    st.success(st.session_state.wake_success)

if st.session_state.is_ringing:
    st.error("🚨 ALARM IS RINGING! WAKE UP! 🚨")
    
    col_off, col_snooze = st.columns(2)

    with col_off:
        if st.button("⏰ ALARM OFF (I'M AWAKE)", type="secondary", use_container_width=True):
            try:
                res = requests.post(f"{BACKEND_URL}/api/alarm-off", timeout=10)
                if res.status_code == 200:
                    data = res.json()
                    st.session_state.is_ringing = False
                    st.session_state.wake_success = data.get("message", "Alarm Disabled!")
                    st.rerun()
                else:
                    st.error(f"Request failed: {res.status_code}")
            except requests.exceptions.ConnectionError:
                st.error(f"Cannot reach backend at: {BACKEND_URL}")
            except requests.exceptions.Timeout:
                st.error("Backend timed out. Render server might be starting up.")

    with col_snooze:
        if st.button("💸 SNOOZE (Pay ₹10)", type="primary", use_container_width=True):
            try:
                res = requests.post(
                    f"{BACKEND_URL}/api/snooze",
                    json={"penalty_amount": 10.0},
                    timeout=10
                )
                if res.status_code == 200:
                    data = res.json()
                    st.warning(data.get("message"))
                    
                    # Optional: Generate quick UPI QR code
                    upi_qr = qrcode.make("upi://pay?pa=dummy@upi&pn=CashOClock&am=10")
                    st.image(upi_qr.get_image(), caption="Scan to pay Snooze Penalty", width=200)
                else:
                    st.error(f"Snooze failed: {res.status_code}")
            except requests.exceptions.ConnectionError:
                st.error(f"Cannot reach backend at: {BACKEND_URL}")
            except requests.exceptions.Timeout:
                st.error("Backend timed out. Please try again.")