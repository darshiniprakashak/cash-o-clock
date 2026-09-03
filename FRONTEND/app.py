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

# 2. Dynamic Backend URL Configuration
try:
    RAW_URL = st.secrets.get("BACKEND_URL", os.getenv("BACKEND_URL", "https://cash-o-clock.onrender.com"))
except Exception:
    RAW_URL = os.getenv("BACKEND_URL", "https://cash-o-clock.onrender.com")

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
    st.markdown(
        """
        <div style="text-align: center; padding-top: 30px; padding-bottom: 20px;">
            <h1 style="font-size: 3rem; margin-bottom: 0px;">Cash-O-Clock</h1>
            <p style="font-size: 1.2rem; font-weight: bold; margin-top: 10px; margin-bottom: 30px;">
                The app that makes sleep expensive.
            </p>
            <div style="font-size: 80px; margin-bottom: 30px;">
                ⏰
            </div>
            <p style="font-size: 1.3rem; font-weight: bold; margin-bottom: 40px;">
                Snooze less. Wake up faster. Save your money.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("LAUNCH CASH-O-CLOCK", type="primary", use_container_width=True):
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
                requests.post(f"{BACKEND_URL}/alarm-off", timeout=3)
            except Exception:
                pass  # Graceful fallback
            
            st.session_state.is_ringing = False
            st.session_state.wake_success = True
            st.session_state.last_receipt = None
            st.rerun()

    with col_snooze:
        snooze_btn = f"💸 SNOOZE (PAY ₹{st.session_state.penalty_amount:.0f})"
        if st.button(snooze_btn, type="primary", use_container_width=True):
            ref_code = f"REF_{int(time.time())}"
            try:
                res = requests.post(
                    f"{BACKEND_URL}/snooze",
                    json={
                        "penalty_amount": float(st.session_state.penalty_amount),
                        "upi_id": st.session_state.upi_id
                    },
                    timeout=3
                )
                if res.status_code == 200:
                    data = res.json()
                    ref_code = data.get("ref_code", ref_code)
            except Exception:
                pass  # Graceful fallback guarantees demo never breaks

            st.session_state.total_penalty += float(st.session_state.penalty_amount)
            st.session_state.snooze_count += 1
            st.session_state.last_receipt = {
                "amount": st.session_state.penalty_amount,
                "upi_id": st.session_state.upi_id,
                "ref": ref_code
            }
            st.session_state.is_ringing = False
            st.session_state.wake_success = False
            st.rerun()

# =============================================================
# SCREEN 3: MAIN DASHBOARD & SETUP PAGE
# =============================================================
else:
    st.title("Cash-O-Clock 🎯")
    
    if st.session_state.wake_success:
        st.balloons()
        st.success("🏆 VICTORY! Alarm turned off on time! Zero funds debited.")

    col_stat1, col_stat2 = st.columns(2)
    with col_stat1:
        st.metric(label="Total Penalty Paid", value=f"₹{st.session_state.total_penalty:.0f}")
    with col_stat2:
        st.metric(label="No. of Snoozes", value=st.session_state.snooze_count)

    st.write("---")

    if st.session_state.last_receipt:
        st.error("🚨 SNOOZE PENALTY TRIGGERED!")
        receipt = st.session_state.last_receipt
        st.write(f"**Amount:** ₹{receipt['amount']:.0f}")
        st.write(f"**Recipient:** `{receipt['upi_id']}`")
        st.write(f"**Reference:** `{receipt['ref']}`")
        
        upi_link = f"upi://pay?pa={receipt['upi_id']}&pn=CashOClock&am={receipt['amount']}"
        qr_img = qrcode.make(upi_link)
        buf = io.BytesIO()
        qr_img.save(buf)
        st.image(buf.getvalue(), caption="Scan with Google Pay / PhonePe / Paytm", width=220)
        st.markdown(f"[👉 Click here to pay directly via UPI App]({upi_link})")
        st.write("---")

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
