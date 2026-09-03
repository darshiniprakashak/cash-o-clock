with col_snooze:
    snooze_btn = f"💸 SNOOZE (PAY ₹{st.session_state.penalty_amount:.0f})"
    if st.button(snooze_btn, type="primary", use_container_width=True):
        # Attempt backend ping, but proceed regardless so UI never breaks
        try:
            requests.post(
                f"{BACKEND_URL}/snooze",
                json={
                    "penalty_amount": float(st.session_state.penalty_amount),
                    "upi_id": st.session_state.upi_id
                },
                timeout=5
            )
        except Exception:
            pass  # Fallback gracefully if API is slow or route mismatched
        
        # Always update UI and generate receipt/QR locally
        st.session_state.total_penalty += float(st.session_state.penalty_amount)
        st.session_state.snooze_count += 1
        st.session_state.last_receipt = {
            "amount": st.session_state.penalty_amount,
            "upi_id": st.session_state.upi_id,
            "ref": f"REF_{int(time.time())}"
        }
        st.session_state.is_ringing = False
        st.session_state.wake_success = False
        st.rerun()