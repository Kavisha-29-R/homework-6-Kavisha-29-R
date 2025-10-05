# Task 2:
#   Create a streamlit app where a user enters longitude and latitude and it creates a map with with a little icon over the spot that you selected. 
#   Again, post the python code for your app as well as a gif screen capture of it running.


import streamlit as st
import pandas as pd
import pydeck as pdk

# --- App title ---
st.title("🌍 Longitude & Latitude Map Viewer")

st.write("Enter coordinates below to display a marker on the map:")

# --- Input fields ---
col1, col2 = st.columns(2)
with col1:
    latitude = st.number_input("Latitude", value=0.0, format="%.6f")
with col2:
    longitude = st.number_input("Longitude", value=0.0, format="%.6f")

# --- Create a small dataframe for the coordinates ---
data = pd.DataFrame({"lat": [latitude], "lon": [longitude]})

# --- Check that values are valid ---
if latitude != 0.0 or longitude != 0.0:
    st.success(f"📍 Marker placed at ({latitude}, {longitude})")

    # --- Define the map view ---
    view_state = pdk.ViewState(
        latitude=latitude,
        longitude=longitude,
        zoom=8,
        pitch=0,
    )

    # --- Define the layer (simple red dot marker) ---
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=data,
        get_position='[lon, lat]',
        get_color='[200, 30, 0, 160]',
        get_radius=20000,
    )

    # --- Create and show the deck.gl map ---
    map = pdk.Deck(
        map_style="light",  # public map style (no API key)
        initial_view_state=view_state,
        layers=[layer],
    )

    st.pydeck_chart(map)
else:
    st.info("Please enter a latitude and longitude to display the map.")
