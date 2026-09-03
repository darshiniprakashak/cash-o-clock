import os
import requests
import streamlit as st
import qrcode
from PIL import Image

# 1. Page Configuration
st.set_page_config(
    page_title="Cash-O-Clock", 
    page_icon="⏰", 
    layout="centered"
)

# 2. Dynamic Backend URL Configuration
# Safely reads from Streamlit Secrets or Environment Variables, defaulting to localhost
RAW_URL = st.secrets.get("BACKEND_URL", os.getenv("BACKEND_URL", "http://localhost:8000"))
BACKEND_URL = RAW_URL.rstrip("/")

# 3. Session State Initialization
if "is_ringing" not in st.session_state:
    st.session_state.is_ringing = False
if "wake_success" not in st.session_state:
    st.session_state.wake_success = None
if "penalty_amount" not in st.session_state:
    st.session_state.penalty_amount = 10.0

# --- APP HEADER ---
st.title("⏰ Cash-O-Clock")
st.caption("The alarm clock that hurts your wallet when you snooze.")
st.divider()

# =============================================================
# SCREEN 1: ALARM RINGING SCREEN (Triggered when alarm goes off)
# =============================================================
if st.session_state.is_ringing:
    st.error("🚨 ALARM IS RINGING! WAKE UP! 🚨")
    
    # Sound effect alert/audio cue
    st.audio("https://www.soundjay.com/clock/alarm-clock-1.mp3", autoplay=True)

    col_off, col_snooze = st.columns(2)

    with col_off:
        if st.button("⏰ ALARM OFF (I'M AWAKE)", type="secondary", use_container_width=True):
            try:
                res = requests.post(f"{BACKEND_URL}/api/alarm-off", timeout=10)
                if res.status_code == 200:
                    data = res.json()
                    st.session_state.is_ringing = False
                    st.session_state.wake_success = data.get("message", "Great job waking up on time!")
                    st.rerun()
                else:
                    st.error(f"Backend error ({res.status_code})")
            except requests.exceptions.ConnectionError:
                st.error(f"Cannot reach backend at: {BACKEND_URL}")
            except requests.exceptions.Timeout:
                st.error("Request timed out. Please try again.")

    with col_snooze:
        snooze_label = f"💸 SNOOZE (Pay ₹{st.session_state.penalty_amount})"
        if st.button(snooze_label, type="primary", use_container_width=True):
            try:
                res = requests.post(
                    f"{BACKEND_URL}/api/snooze",
                    json={"penalty_amount": st.session_state.penalty_amount},
                    timeout=10
                )
                if res.status_code == 200:
                    data = res.json()
                    st.warning(data.get("message", "Snoozed! Penalty applies."))
                    
                    # Generate UPI Payment QR Code
                    upi_uri = f"upi://pay?pa=cashoclock@upi&pn=CashOClock&am={st.session_state.penalty_amount}"
                    upi_qr = qrcode.make(upi_uri)
                    
                    st.markdown("### Scan & Pay Penalty")
                    st.image(upi_qr.get_image(), caption=f"Scan using Google Pay/PhonePe to pay ₹{st.session_state.penalty_amount}", width=220)
                else:
                    st.error(f"Snooze failed: {res.status_code}")
            except requests.exceptions.ConnectionError:
                st.error(f"Cannot reach backend at: {BACKEND_URL}")
            except requests.exceptions.Timeout:
                st.error("Request timed out.")

# =============================================================
# SCREEN 2: WELCOME / DASHBOARD SCREEN (Default View)
# =============================================================
else:
    # Display success state if alarm was successfully turned off
    if st.session_state.wake_success:
        st.balloons()
        st.success(st.session_state.wake_success)
        st.session_state.wake_success = None  # Reset after showing

    st.subheader("👋 Welcome to your Dashboard")
    st.write("Set your wake-up time and configure your snooze penalty to stay disciplined.")

    with st.container():
        st.markdown("### ⚙️ Alarm Settings")
        
        col_time, col_penalty = st.columns(2)
        
        with col_time:
            alarm_time = st.time_input("Set Alarm Time")
            
        with col_penalty:
            penalty = st.number_input(
                "Snooze Penalty (₹)", 
                min_value=5.0, 
                max_value=1000.0, 
                value=float(st.session_state.penalty_amount),
                step=5.0
            )
            st.session_state.penalty_amount = penalty

    st.divider()

    # Simulator trigger for demonstration/testing
    st.markdown("### 🧪 Test & Demo")
    if st.button("🔔 Trigger Alarm (Simulate Ringing)", type="primary", use_container_width=True):
        st.session_state.is_ringing = True
        st.rerun()

    # Footer/Status info
    st.caption(f"Connected Backend: `{BACKEND_URL}`")