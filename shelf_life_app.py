import streamlit as st
from datetime import datetime, timedelta
import re

st.title("📦 Shelf-Life Calculator")

# --- Inputs ---
start_date = st.date_input("Manufacturing Date (A1)", datetime.today())
expiry_input = st.text_input("Expiry (B1: Date or 30D / 10W / 6M)")

expiry_date = None

# --- Determine expiry date ---
if expiry_input:
    try:
        # Case 1: expiry_input is a date (YYYY-MM-DD)
        expiry_date = datetime.strptime(expiry_input, "%Y-%m-%d").date()
    except:
        # Case 2: expiry_input is duration text (like 30D, 10W, 6M)
        match = re.match(r"(\d+)([DdWwMm])", expiry_input.strip())
        if match:
            value, unit = int(match.group(1)), match.group(2).upper()
            if unit == "D":
                expiry_date = start_date + timedelta(days=value)
            elif unit == "W":
                expiry_date = start_date + timedelta(weeks=value)
            elif unit == "M":
                # Approximate months as 30 days each
                expiry_date = start_date + timedelta(days=value*30)

# --- Calculate results ---
if expiry_date:
    today = datetime.today().date()
    total_days = (expiry_date - start_date).days
    remaining_days = (expiry_date - today).days
    remaining_weeks = remaining_days / 7
    remaining_months = remaining_days / 30

    if remaining_days < 0:
        percent = 0
        emoji = "😡"  # expired
    else:
        percent = max(0, min(100, 100 - ((today - start_date).days / total_days * 100)))
        emoji = "😊" if percent > 70 else "😢"

    # --- Display results ---
    st.subheader("📊 Shelf-Life Status")
    st.write(f"**Expiry Date:** {expiry_date}")
    st.write(f"**Remaining Shelf-Life (%):** {percent:.2f}% {emoji}")
    st.write(f"**Days Remaining:** {remaining_days}")
    st.write(f"**Weeks Remaining:** {remaining_weeks:.1f}")
    st.write(f"**Months Remaining:** {remaining_months:.1f}")
