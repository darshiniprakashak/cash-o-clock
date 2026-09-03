import streamlit as st
import streamlit.components.v1 as components
import requests
import qrcode
import datetime
import time
from io import BytesIO

# =========================================================
# PAGE SETTINGS
# =========================================================

st.set_page_config(
    page_title="Cash-O-Clock",
    page_icon="⏰",
    layout="centered"
)

BACKEND_URL = "http://127.0.0.1:8000"

# =========================================================
# QR CODE FUNCTION
# =========================================================

def generate_qr(upi_url):
    qr = qrcode.QRCode(
        version=1,
        box_size=8,
        border=2
    )
    qr.add_data(upi_url)
    qr.make(fit=True)
    img = qr.make_image(
        fill_color="black",
        back_color="white"
    )
    buf = BytesIO()
    img.save(buf)
    return buf.getvalue()

# =========================================================
# SESSION STATE
# =========================================================

if "total_loss" not in st.session_state:
    st.session_state.total_loss = 0

if "snooze_count" not in st.session_state:
    st.session_state.snooze_count = 0

if "is_ringing" not in st.session_state:
    st.session_state.is_ringing = False

if "last_receipt" not in st.session_state:
    st.session_state.last_receipt = None

if "wake_success" not in st.session_state:
    st.session_state.wake_success = None

if "app_started" not in st.session_state:
    st.session_state.app_started = False


# =========================================================
# COLOR PALETTE (REFERENCE IMAGE BASED)
# =========================================================

COLOR_BG = "#0B1021"
COLOR_CARD = "#151C33"
COLOR_YELLOW = "#FFD166"
COLOR_ORANGE = "#FB8500"
COLOR_BLUE = "#4EA8DE"
COLOR_WHITE = "#FFFFFF"
COLOR_CORAL = "#E07A5F"

st.markdown(
    f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@500;700;900&display=swap');

        * {{
            font-family: 'Fredoka', sans-serif !important;
            -webkit-text-stroke: 0px transparent !important;
        }}

        .stApp, [data-testid="stAppViewContainer"], .main {{
            background-color: {COLOR_BG} !important;
            background-image: none !important;
        }}

        [data-testid="stHeader"] {{
            background: transparent !important;
            z-index: 10;
        }}

        [data-testid="stToolbar"] {{
            display: none !important;
        }}

        footer {{
            visibility: hidden !important;
        }}

        .block-container {{
            padding-top: 30px;
            padding-bottom: 30px;
            position: relative;
            z-index: 5;
            background: transparent !important;
        }}

        /* Typography */
        h1, h2, h3, h4, h5, h6 {{
            color: {COLOR_YELLOW} !important;
            font-size: 2.1rem !important;
            font-weight: 900 !important;
        }}

        p, label, span {{
            color: {COLOR_WHITE} !important;
        }}

        /* Widget Labels */
        div[data-testid="stWidgetLabel"] label,
        div[data-testid="stWidgetLabel"] p {{
            color: {COLOR_YELLOW} !important;
            font-size: 1.4rem !important;
            font-weight: 800 !important;
            margin-bottom: 8px !important;
        }}

        /* Text and Time Inputs */
        div[data-testid="stTextInput"] div,
        div[data-testid="stTimeInput"] div,
        div[data-baseweb="input"],
        div[data-baseweb="base-input"],
        input {{
            background-color: {COLOR_CARD} !important;
            background: {COLOR_CARD} !important;
            color: {COLOR_WHITE} !important;
            -webkit-text-fill-color: {COLOR_WHITE} !important;
            border-radius: 14px !important;
        }}

        div[data-baseweb="input"] {{
            border: 2px solid {COLOR_BLUE} !important;
            box-shadow: 0px 0px 10px rgba(78,168,222,0.2) !important;
            padding: 4px 8px !important;
        }}

        input[data-baseweb="input"],
        div[data-testid="stTextInput"] input,
        div[data-testid="stTimeInput"] input {{
            background-color: transparent !important;
            background: transparent !important;
            font-size: 1.35rem !important;
            font-weight: 900 !important;
        }}

        div[data-testid="stTimeInput"] svg {{
            fill: {COLOR_YELLOW} !important;
            width: 24px !important;
            height: 24px !important;
        }}

        /* Sliders */
        div[data-testid="stSlider"] p,
        div[data-testid="stSlider"] div {{
            font-size: 1.25rem !important;
            font-weight: 800 !important;
            color: {COLOR_WHITE} !important;
        }}
        
        div[data-testid="stSlider"] [data-testid="stMarkdownContainer"] p {{
            font-size: 1.5rem !important;
            font-weight: 900 !important;
            color: {COLOR_YELLOW} !important;
        }}

        span[data-baseweb="slider"] {{
            background-color: {COLOR_YELLOW} !important;
        }}

        /* Buttons */
        .stButton > button {{
            background-color: {COLOR_CARD} !important;
            border: 2px solid {COLOR_YELLOW} !important;
            color: {COLOR_YELLOW} !important;
            border-radius: 14px !important;
            font-weight: 900 !important;
            font-size: 1.25rem !important;
            box-shadow: 0px 0px 10px rgba(255,209,102,0.2) !important;
            padding: 10px 16px !important;
        }}

        .stButton > button p {{
            color: {COLOR_YELLOW} !important;
            font-size: 1.25rem !important;
            font-weight: 900 !important;
        }}

        .stButton > button[kind="primary"] {{
            background-color: {COLOR_CORAL} !important;
            border: 2px solid {COLOR_YELLOW} !important;
            box-shadow: 0px 0px 12px rgba(224,122,95,0.4) !important;
        }}

        .stButton > button[kind="primary"] p {{
            color: {COLOR_WHITE} !important;
        }}
    </style>
    """,
    unsafe_allow_html=True
)

# =========================================================
# FRONT PAGE
# =========================================================

if not st.session_state.app_started:

    st.markdown(
        f"""
        <div style="text-align:center; margin-top:50px;">
            <div style="font-size:68px; font-weight:900; color:{COLOR_YELLOW};">
                Cash-O-Clock
            </div>
            <div style="font-size:24px; font-weight:700; color:{COLOR_WHITE}; margin-top:10px;">
                The app that makes sleep expensive.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div style="text-align:center; font-size:140px; line-height:1; margin:40px 0;">
            ⏰
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div style="text-align:center; font-size:26px; font-weight:900; color:{COLOR_YELLOW}; margin-bottom:40px;">
            Snooze less. Wake up faster. Save your money.
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button("LAUNCH CASH-O-CLOCK", type="primary", use_container_width=True):
        st.session_state.app_started = True
        st.rerun()

# =========================================================
# MAIN APP
# =========================================================

else:

    st.markdown(
        f"""
        <div style="text-align:center;">
            <div style="font-size:56px; font-weight:900; color:{COLOR_YELLOW};">
                ⏰ Cash-O-Clock
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    # DASHBOARD
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            f"""
            <div style="background:{COLOR_CARD}; border:2px solid {COLOR_BLUE}; border-radius:18px; padding:20px; text-align:center;">
                <div style="font-size:38px;">💸</div>
                <div style="color:{COLOR_YELLOW}; font-weight:900; font-size:16px;">TOTAL PENALTY PAID</div>
                <div style="color:{COLOR_WHITE}; font-size:38px; font-weight:900;">₹{st.session_state.total_loss}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div style="background:{COLOR_CARD}; border:2px solid {COLOR_BLUE}; border-radius:18px; padding:20px; text-align:center;">
                <div style="font-size:38px;">😴</div>
                <div style="color:{COLOR_YELLOW}; font-weight:900; font-size:16px;">NO. OF SNOOZES</div>
                <div style="color:{COLOR_WHITE}; font-size:38px; font-weight:900;">{st.session_state.snooze_count}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # RECEIPT
    if st.session_state.last_receipt:
        receipt = st.session_state.last_receipt

        st.error(
            f"💸 **TRANSACTION INITIATED!**\n\n"
            f"• **Amount:** ₹{receipt['amount']}\n\n"
            f"• **Recipient:** {receipt['recipient']}\n\n"
            f"• **Ref Code:** `{receipt.get('transaction_ref')}`"
        )

        if "upi_link" in receipt:
            qr_img = generate_qr(receipt["upi_link"])

            st.image(
                qr_img,
                caption="Scan with GPay / PhonePe / Paytm to authorize payment",
                width=220
            )

            st.markdown(
                f"[👉 **Click here to pay directly via UPI App**]({receipt['upi_link']})"
            )

    # SUCCESS
    if st.session_state.wake_success:
        st.success(f"🎉 **VICTORY!** {st.session_state.wake_success}")

    st.divider()

    # SETUP SCREEN
    if not st.session_state.is_ringing:

        st.markdown(
            f"""
            <div style="background:{COLOR_CARD}; border:2px solid {COLOR_YELLOW}; border-radius:18px; padding:22px;">
                <h3 style="color:{COLOR_YELLOW}; margin:0;">⚙️ Setup Alarm</h3>
                <p style="color:{COLOR_WHITE}; font-size:1.2rem; font-weight:700; margin-top:6px;">Set your alarm and choose your snooze cost.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.write("")

        penalty = st.select_slider(
            "💰 Snooze Penalty Amount:",
            options=[5, 10, 20, 50, 100],
            value=5,
            format_func=lambda x: f"₹{x}"
        )

        target_upi = st.text_input(
            "📱 Destination UPI ID (Receiver Account):",
            value="yourname@okaxis"
        )

        st.divider()

        st.markdown(
            f"""
            <h3 style="color:{COLOR_YELLOW};">
                ⏰ Set Alarm Time
            </h3>
            """,
            unsafe_allow_html=True
        )

        alarm_time = st.time_input(
            "Set Alarm Time:",
            value=datetime.time(6, 30)
        )

        st.session_state.current_penalty = penalty
        st.session_state.current_target = target_upi

        col_set, col_demo = st.columns(2)

        with col_set:
            if st.button("🔔 Activate Alarm", use_container_width=True):
                st.info(f"⏳ Alarm set for {alarm_time.strftime('%I:%M %p')}. Checking time...")
                now = datetime.datetime.now().time()
                if now.hour == alarm_time.hour and now.minute == alarm_time.minute:
                    st.session_state.is_ringing = True
                    st.rerun()

        with col_demo:
            if st.button("⚡ DEMO MODE: Ring Alarm Instantly", type="primary", use_container_width=True):
                st.session_state.is_ringing = True
                st.session_state.last_receipt = None
                st.session_state.wake_success = None
                st.rerun()

    # RINGING SCREEN
    else:

        st.markdown(
            f"""
            <div style="background:{COLOR_CARD}; border:2.5px solid {COLOR_ORANGE}; border-radius:20px; padding:25px; text-align:center;">
                <div style="font-size:130px; line-height:1;">⏰</div>
                <div style="color:{COLOR_YELLOW}; font-size:42px; font-weight:900;">
                    🚨 WAKE UP OR PAY UP! 🚨
                </div>
                <div style="color:{COLOR_WHITE}; font-size:22px; font-weight:800; margin-top:10px;">
                    Your sleep is getting expensive! 💸
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        components.html(
            """
            <audio autoplay>
                <source src="https://assets.mixkit.co/active_storage/sfx/2869/2869-preview.mp3" type="audio/mpeg">
            </audio>
            """,
            height=0
        )

        penalty_amt = st.session_state.get("current_penalty", 5)
        target_dest = st.session_state.get("current_target", "yourname@okaxis")

        st.markdown(
            f"""
            <div style="background:{COLOR_CARD}; border:2px solid {COLOR_YELLOW}; border-radius:18px; padding:20px; text-align:center; margin-top:20px;">
                <div style="color:{COLOR_WHITE}; font-size:22px; font-weight:800;">😴 Want to snooze?</div>
                <div style="color:{COLOR_YELLOW}; font-size:44px; font-weight:900;">₹{penalty_amt}</div>
                <div style="color:{COLOR_WHITE}; font-size:18px; font-weight:700;">That's the price of going back to sleep! 💸</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.write("")

        col_snooze, col_off = st.columns(2)

        with col_snooze:
            if st.button(f"😴 SNOOZE (PAY ₹{penalty_amt})", type="primary", use_container_width=True):
                try:
                    payload = {
                        "penalty": penalty_amt,
                        "target_upi": target_dest
                    }
                    res = requests.post(f"{BACKEND_URL}/api/snooze", json=payload)

                    if res.status_code == 200:
                        data = res.json()
                        st.session_state.total_loss += data["amount"]
                        st.session_state.snooze_count += 1
                        st.session_state.is_ringing = False
                        st.session_state.last_receipt = data
                        st.session_state.wake_success = None
                        st.rerun()
                    else:
                        st.error(f"Payment request failed: {res.status_code}")

                except requests.exceptions.ConnectionError:
                    st.error("Backend offline! Start uvicorn server in terminal.")

        with col_off:
            if st.button("⏰ ALARM OFF (I'M AWAKE)", type="secondary", use_container_width=True):
                try:
                    res = requests.post(f"{BACKEND_URL}/api/alarm-off")
                    if res.status_code == 200:
                        data = res.json()
                        st.session_state.is_ringing = False
                        st.session_state.last_receipt = None
                        st.session_state.wake_success = data["message"]
                        st.balloons()
                        st.rerun()
                    else:
                        st.error(f"Alarm off request failed: {res.status_code}")

                except requests.exceptions.ConnectionError:
                    st.error("Backend offline!")