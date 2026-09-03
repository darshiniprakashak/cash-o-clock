import os
import io
import time
import requests
import qrcode
import streamlit as st
from PIL import Image

# 1. Page Configuration
st.set_page_config(
    page_title="Cash-O-Clock 🎯", 
    page_icon="⏰", 
    layout="centered"
)

# 2. Dynamic Backend URL Configuration (Streamlit Secrets -> Environment -> Fallback)
try:
    RAW_URL = st.secrets.get("BACKEND_URL", os.getenv("BACKEND_URL", "http://localhost:8000"))
except Exception:
    RAW_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

BACKEND_URL = RAW_URL.rstrip("/")

# 3. Session State Initialization
if "page" not in st.session_state:
    st.session_state.page = "welcome"
if "is_ringing" not in st.session_state:
    st.session_state.is_ringing = False
if "total_penalty" not in st.session_state:
    st.session_state.total_penalty = 0.0
if "snooze_count" not in st.session_state:
    st.session_state.snooze_count = 0
if "penalty_amount" not in st.session_state:
    st.session_state.penalty_amount = 5.0
if "upi_id" not in st.session_state:
    st.session_state.upi_id = "yourname@okaxis"
if "wake_success" not in st.session_state:
    st.session_state.wake_success = False
if "last_receipt" not in st.session_state:
    st.session_state.last_receipt = None

# =============================================================
# SCREEN 1: WELCOME LANDING PAGE
# =============================================================
if st.session_state.page == "welcome":
    st.title("Cash-O-Clock 🎯")
    st.caption("The alarm clock that hurts your wallet when you snooze.")
    st.write("---")
    
    st.markdown("### Stop Paying with Your Time. Start Paying with Your Cash.")
    st.write(
        "Cash-O-Clock weaponizes financial consequences to force you out of bed. "
        "Hit snooze, and your money instantly goes to your designated receiver via UPI."
    )
    
    if st.button("🚀 LAUNCH CASH-O-CLOCK", type="primary", use_container_width=True):
        st.session_state.page = "dashboard"
        st.rerun()

# =============================================================
# SCREEN 2: ACTIVE ALARM RINGING SCREEN
# =============================================================
elif st.session_state.is_ringing:
    st.error("🚨 WAKE UP OR PAY UP! 🚨")
    st.warning("Your sleep is getting expensive! 💸")
    
    st.metric(label="Mandatory Snooze Cost", value=f"₹{st.session_state.penalty_amount:.0f}")
    
    col_off, col_snooze = st.columns(2)

    with col_off:
        if st.button("⏰ ALARM OFF (I'M AWAKE)", type="secondary", use_container_width=True):
            try:
                res = requests.post(f"{BACKEND_URL}/api/alarm-off", timeout=10)
                if res.status_code == 200:
                    st.session_state.is_ringing = False
                    st.session_state.wake_success = True
                    st.session_state.last_receipt = None
                    st.rerun()
                else:
                    st.error(f"Error: {res.status_code}")
            except requests.exceptions.ConnectionError:
                st.error(f"Cannot reach backend at: {BACKEND_URL}")

    with col_snooze:
        snooze_btn = f"💸 SNOOZE (PAY ₹{st.session_state.penalty_amount:.0f})"
        if st.button(snooze_btn, type="primary", use_container_width=True):
            try:
                res = requests.post(
                    f"{BACKEND_URL}/api/snooze",
                    json={
                        "penalty_amount": float(st.session_state.penalty_amount),
                        "upi_id": st.session_state.upi_id
                    },
                    timeout=10
                )
                if res.status_code == 200:
                    data = res.json()
                    st.session_state.total_penalty += float(st.session_state.penalty_amount)
                    st.session_state.snooze_count += 1
                    st.session_state.last_receipt = {
                        "amount": st.session_state.penalty_amount,
                        "upi_id": st.session_state.upi_id,
                        "ref": data.get("ref_code", f"REF_{int(time.time())}")
                    }
                    st.session_state.is_ringing = False
                    st.session_state.wake_success = False
                    st.rerun()
                else:
                    st.error(f"Snooze failed: {res.status_code}")
            except requests.exceptions.ConnectionError:
                st.error(f"Cannot reach backend at: {BACKEND_URL}")

# =============================================================
# SCREEN 3: MAIN DASHBOARD & SETUP PAGE
# =============================================================
else:
    st.title("Cash-O-Clock 🎯")
    
    # Victory Banner
    if st.session_state.wake_success:
        st.balloons()
        st.success("🏆 VICTORY! Alarm turned off on time! Zero funds debited.")

    # Real-Time Metrics Header
    col_stat1, col_stat2 = st.columns(2)
    with col_stat1:
        st.metric(label="Total Penalty Paid", value=f"₹{st.session_state.total_penalty:.0f}")
    with col_stat2:
        st.metric(label="No. of Snoozes", value=st.session_state.snooze_count)

    st.write("---")

    # Payment Receipt / UPI QR Card (Displays after Snooze)
    if st.session_state.last_receipt:
        st.error("🚨 SNOOZE PENALTY TRIGGERED!")
        receipt = st.session_state.last_receipt
        st.write(f"**Amount:** ₹{receipt['amount']:.0f}")
        st.write(f"**Recipient:** `{receipt['upi_id']}`")
        st.write(f"**Reference:** `{receipt['ref']}`")
        
        # QR Generation
        upi_link = f"upi://pay?pa={receipt['upi_id']}&pn=CashOClock&am={receipt['amount']}"
        qr_img = qrcode.make(upi_link)
        buf = io.BytesIO()
        qr_img.save(buf)
        st.image(buf.getvalue(), caption="Scan with Google Pay / PhonePe / Paytm", width=220)
        st.markdown(f"[👉 Click here to pay directly via UPI App]({upi_link})")
        st.write("---")

    # Configuration Form
    st.subheader("⚙️ Alarm Configuration")
    
    st.session_state.penalty_amount = st.slider(
        "Snooze Penalty Amount (₹)", 
        min_value=5, 
        max_value=100, 
        value=int(st.session_state.penalty_amount),
        step=5
    )
    
    st.session_state.upi_id = st.text_input(
        "Destination UPI ID", 
        value=st.session_state.upi_id
    )
    
    alarm_time = st.time_input("Target Alarm Time")

    col_act, col_demo = st.columns(2)
    with col_act:
        if st.button("🔔 Activate Alarm", type="secondary", use_container_width=True):
            st.info(f"Alarm scheduled for {alarm_time}. Keep this tab open!")
            
    with col_demo:
        if st.button("⚡ DEMO MODE: Ring Alarm Instantly", type="primary", use_container_width=True):
            st.session_state.is_ringing = True
            st.session_state.wake_success = False
            st.rerun()