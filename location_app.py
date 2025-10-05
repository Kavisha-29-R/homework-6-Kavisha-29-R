# Task 2:
#   Create a streamlit app where a user enters longitude and latitude and it creates a map with with a little icon over the spot that you selected. 
#   Again, post the python code for your app as well as a gif screen capture of it running.


import streamlit as st
import pandas as pd
import pydeck as pdk

# Set page config to wide mode
st.set_page_config(
    page_title="Longitude & Latitude Map Viewer",
    layout="wide",  # <-- makes the app use full browser width
    initial_sidebar_state="collapsed"
)

st.title("🌍 Longitude & Latitude Map Viewer")

st.write("Enter coordinates below to display a marker on the map:")

# --- Initialize session state ---
if "latitude_input" not in st.session_state:
    st.session_state.latitude_input = "00.0000"
if "longitude_input" not in st.session_state:
    st.session_state.longitude_input = "00.0000"

# --- Clear buttons ---
col1, col2 = st.columns(2)
with col1:
    if st.button("Clear Latitude"):
        st.session_state.latitude_input = ""
with col2:
    if st.button("Clear Longitude"):
        st.session_state.longitude_input = ""

# --- Input fields ---
col1, col2 = st.columns(2)
with col1:
    lat_text = st.text_input(
        "Latitude",
        value=st.session_state.latitude_input,
        key="latitude_input_box",
        placeholder="Enter latitude..."
    )
with col2:
    lon_text = st.text_input(
        "Longitude",
        value=st.session_state.longitude_input,
        key="longitude_input_box",
        placeholder="Enter longitude..."
    )

# --- Save the current text back into session state ---
st.session_state.latitude_input = lat_text
st.session_state.longitude_input = lon_text

# --- Validate inputs ---
try:
    latitude = float(lat_text)
    longitude = float(lon_text)
    valid = True
except ValueError:
    st.error("Please enter valid numeric values for latitude and longitude.")
    valid = False

# --- Show map if inputs are valid ---
if valid:
    data = pd.DataFrame({"lat": [latitude], "lon": [longitude]})

    st.success(f"📍 Marker placed at ({latitude}, {longitude})")

    view_state = pdk.ViewState(
        latitude=latitude,
        longitude=longitude,
        zoom=8,
        pitch=0,
    )

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=data,
        get_position='[lon, lat]',
        get_color='[200, 30, 0, 160]',
        get_radius=20000,
    )

    map_chart = pdk.Deck(
        map_style="light",
        initial_view_state=view_state,
        layers=[layer],
    )

    st.pydeck_chart(map_chart)
