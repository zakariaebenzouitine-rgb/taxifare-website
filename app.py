import streamlit as st
import requests
from datetime import datetime

# --- Title ---
st.title("🚕 Taxi Fare Prediction App")

st.markdown("""
This simple app lets you predict the **taxi fare price** based on the trip details.
You just need to fill in the ride parameters, and we'll call the prediction API for you.
""")

# --- 1. Collect user inputs ---
st.header("Enter your ride details:")

pickup_datetime = st.date_input(
    "📅 Date and time of the pickup",
    value=datetime(2023, 1, 1, 12, 0)
)

pickup_longitude = st.number_input("📍 Pickup longitude", value=-73.985428, format="%.6f")
pickup_latitude = st.number_input("📍 Pickup latitude", value=40.748817, format="%.6f")
dropoff_longitude = st.number_input("🎯 Dropoff longitude", value=-73.985428, format="%.6f")
dropoff_latitude = st.number_input("🎯 Dropoff latitude", value=40.761432, format="%.6f")
passenger_count = st.number_input("👥 Passenger count", min_value=1, max_value=8, value=1, step=1)

# --- 2. Build the parameters dictionary ---
params = {
    "pickup_datetime": pickup_datetime.strftime("%Y-%m-%d %H:%M:%S"),
    "pickup_longitude": pickup_longitude,
    "pickup_latitude": pickup_latitude,
    "dropoff_longitude": dropoff_longitude,
    "dropoff_latitude": dropoff_latitude,
    "passenger_count": passenger_count
}

# --- 3. Call the API ---
url = "https://taxifare.lewagon.ai/predict"  # or replace with your own API endpoint

if st.button("🔮 Predict Fare"):
    st.write("Calling the API...")

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # raises an error for bad responses
        prediction = response.json()

        # --- 4. Retrieve the prediction ---
        fare = prediction.get("fare", None)

        if fare is not None:
            st.success(f"💰 The predicted fare is **${fare:.2f}**")
        else:
            st.error("❌ Could not retrieve prediction from the API response.")

    except requests.exceptions.RequestException as e:
        st.error(f"API call failed: {e}")
