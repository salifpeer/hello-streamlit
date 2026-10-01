
import streamlit as st
import math
import folium
from streamlit_geolocation import streamlit_geolocation
from streamlit_folium import st_folium


WORKPLACE_LATITUDE = 34.0018086229816
WORKPLACE_LONGITUDE = 74.79407001364466
ALLOWED_RADIUS = 100


def calculate_distance(
    lat1,
    lon1,
    lat2,
    lon2
):

    R = 6371000

    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)

    delta_lat = math.radians(
        lat2 - lat1
    )

    delta_lon = math.radians(
        lon2 - lon1
    )

    a = (
        math.sin(delta_lat / 2) ** 2
        + math.cos(lat1)
        * math.cos(lat2)
        * math.sin(delta_lon / 2) ** 2
    )

    c = 2 * math.atan2(
        math.sqrt(a),
        math.sqrt(1 - a)
    )

    return R * c


def check_location():

    location = streamlit_geolocation()

    latitude = location.get(
        "latitude"
    )

    longitude = location.get(
        "longitude"
    )

    accuracy = location.get(
        "accuracy"
    )

    if latitude is None or longitude is None:

        st.info(
            "Waiting for your device location..."
        )

        return None

    distance = calculate_distance(
        latitude,
        longitude,
        WORKPLACE_LATITUDE,
        WORKPLACE_LONGITUDE
    )

    map_object = folium.Map(
        location=[
            WORKPLACE_LATITUDE,
            WORKPLACE_LONGITUDE
        ],
        zoom_start=17
    )

    folium.Marker(
        [
            WORKPLACE_LATITUDE,
            WORKPLACE_LONGITUDE
        ],
        tooltip="Authorized Workplace",
        popup="Authorized Workplace",
        icon=folium.Icon(
            color="blue",
            icon="building"
        )
    ).add_to(map_object)

    folium.Circle(
        location=[
            WORKPLACE_LATITUDE,
            WORKPLACE_LONGITUDE
        ],
        radius=ALLOWED_RADIUS,
        tooltip=f"Allowed Area: {ALLOWED_RADIUS} meters",
        popup=f"Employees can check in within {ALLOWED_RADIUS} meters.",
        fill=True
    ).add_to(map_object)

    folium.Marker(
        [
            latitude,
            longitude
        ],
        tooltip="Your Current Location",
        popup=f"Your location\nDistance: {distance:.2f} meters",
        icon=folium.Icon(
            color="red",
            icon="user"
        )
    ).add_to(map_object)

    bounds = [
        [
            WORKPLACE_LATITUDE,
            WORKPLACE_LONGITUDE
        ],
        [
            latitude,
            longitude
        ]
    ]

    map_object.fit_bounds(
        bounds
    )

    st_folium(
        map_object,
        width=700,
        height=450,
        returned_objects=[]
    )

    st.write(
        f"**Your latitude:** `{latitude}`"
    )

    st.write(
        f"**Your longitude:** `{longitude}`"
    )

    st.write(
        f"**Distance from workplace:** `{distance:.2f} meters`"
    )

    if accuracy is not None:

        st.write(
            f"**GPS accuracy:** approximately `{accuracy:.2f} meters`"
        )

    if distance <= ALLOWED_RADIUS:

        st.success(
            f"✅ You are inside the authorized area. Distance: {distance:.2f} meters."
        )

        return True

    st.error(
        f"❌ You are outside the authorized area. Distance: {distance:.2f} meters."
    )

    return False


def location_page():

    st.title(
        "📍 Check-In Location"
    )

    st.write(
        "Verify your location before checking in."
    )

    location_verified = check_location()

    if location_verified is True:

        if st.button(
            "Continue to Check In",
            type="primary"
        ):

            st.session_state.location_verified = True
            st.session_state.page = "dashboard"

            st.rerun()

    if st.button(
        "← Back to Dashboard", type="primary"
    ):

        st.session_state.location_verified = False
        st.session_state.page = "dashboard"

        st.rerun()
