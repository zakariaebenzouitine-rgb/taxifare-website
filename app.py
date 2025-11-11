import streamlit as st
import requests
from datetime import datetime

'''
# TaxiFareModel front
'''

st.markdown('''
Remember that there are several ways to output content into your web page...

Either as with the title by just creating a string (or an f-string). Or as with this paragraph using the `st.` functions
''')

'''
## Here we would like to add some controllers in order to ask the user to select the parameters of the ride

1. Let's ask for:
- date and time
- pickup longitude
- pickup latitude
- dropoff longitude
- dropoff latitude
- passenger count
'''

'''
## Once we have these, let's call our API in order to retrieve a prediction

See ? No need to load a `model.joblib` file in this app, we do not even need to know anything about Data Science in order to retrieve a prediction...

🤔 How could we call our API ? Off course... The `requests` package 💡
'''
st.header("Enter your ride details:")

pickup_datetime = st.date_input(
    "Date and time of the pickup",
    value=datetime(2023, 1, 1, 12, 0)
)

pickup_longitude = st.number_input("Pickup longitude", value=-73.985428, format="%.6f")
pickup_latitude = st.number_input("Pickup latitude", value=40.748817, format="%.6f")
dropoff_longitude = st.number_input("Dropoff longitude", value=-73.985428, format="%.6f")
dropoff_latitude = st.number_input("Dropoff latitude", value=40.761432, format="%.6f")
passenger_count = st.number_input("Passenger count", min_value=1, max_value=8, value=1, step=1)

url = 'https://taxifare.lewagon.ai/predict'

# if url == 'https://taxifare.lewagon.ai/predict':

#     st.markdown('Maybe you want to use your own API for the prediction, not the one provided by Le Wagon...')

# '''

# 2. Let's build a dictionary containing the parameters for our API...

# 3. Let's call our API using the `requests` package...

# 4. Let's retrieve the prediction from the **JSON** returned by the API...

# ## Finally, we can display the prediction to the user
# '''
params = {
    "pickup_datetime": pickup_datetime.strftime("%Y-%m-%d %H:%M:%S"),
    "pickup_longitude": pickup_longitude,
    "pickup_latitude": pickup_latitude,
    "dropoff_longitude": dropoff_longitude,
    "dropoff_latitude": dropoff_latitude,
    "passenger_count": passenger_count
}

if st.button("🔮 Predict Fare"):
    st.write("Calling the API...")

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # raises an error for bad responses
        prediction = response.json()

        # --- 4. Retrieve the prediction ---
        fare = prediction.get("fare", None)

        if fare is not None:
            st.success(f"The predicted fare is **${fare:.2f}**")
        else:
            st.error("Could not retrieve prediction from the API response.")

    except requests.exceptions.RequestException as e:
        st.error(f"API call failed: {e}")
