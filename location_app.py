# Task 2:
#   Create a streamlit app where a user enters longitude and latitude and it creates a map with with a little icon over the spot that you selected. 
#   Again, post the python code for your app as well as a gif screen capture of it running.

# streamlit_point_map.py
import streamlit as st
import pydeck as pdk

st.set_page_config(layout="wide", page_title="Latitude/Longitude Map")

st.title("Place an icon by Latitude / Longitude")

col1, col2 = st.columns([1, 3])

with col1:
    lat = st.number_input("Latitude", value=0.0, format="%.6f")
    lon = st.number_input("Longitude", value=0.0, format="%.6f")
    zoom = st.slider("Zoom level", 1, 18, 5)
    icon_url = st.text_input("Icon image URL (optional)", value="https://upload.wikimedia.org/wikipedia/commons/8/88/Map_marker.svg")
    add_button = st.button("Show point on map")

with col2:
    st.write("Map preview")
    if add_button:
        # create an icon layer using IconLayer
        data = [{
            "name": "selected",
            "lat": lat,
            "lon": lon,
            "icon_url": icon_url,
            "size": 10
        }]
        ICON_LAYER = pdk.Layer(
            "IconLayer",
            data,
            get_icon="{'url': icon_url, 'width': 128, 'height': 128, 'anchorY': 128}",
            get_size=4,
            size_scale=15,
            pickable=True,
            get_position=["lon", "lat"]
        )
        view_state = pdk.ViewState(latitude=lat, longitude=lon, zoom=zoom, pitch=0)
        deck = pdk.Deck(layers=[ICON_LAYER], initial_view_state=view_state, map_style='mapbox/light-v9')
        st.pydeck_chart(deck)
    else:
        st.info("Enter coordinates and click 'Show point on map'")


