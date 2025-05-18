import streamlit as st
import pandas as pd
import pydeck as pdk
from recommendation import recommend_segments
from connect_segments import connect_segments
from osm_surface import get_surface_type

# Load cleaned segment dataset (with all 1526 segments)
@st.cache_data
def load_data():
    return pd.read_csv("data/cleaned_segments.csv")

df = load_data()

st.title("🚴‍♂️ Bike Segment Recommender - Slovenia")

st.sidebar.header("Customize Your Ride")
selected_region = st.sidebar.selectbox("Select Region", sorted(df['region'].unique()))
desired_length = st.sidebar.slider("Desired Length (km)", 1, 100, 25)
difficulty = st.sidebar.selectbox("Climb Difficulty", ["Any", "Easy", "Moderate", "Hard", "Extreme"])
preferred_surface = st.sidebar.selectbox("Surface Type", ["Any", "Asphalt", "Gravel", "Trail"])

if st.sidebar.button("Recommend Route"):
    # Step 1: Recommend segments
    recommended = recommend_segments(df, selected_region, desired_length, difficulty, preferred_surface)
    st.write(recommended)

    # Step 2: Connect segments
    route = connect_segments(recommended)

    # Step 3: Visualize route
    st.subheader("Recommended Route")
    if not route.empty:
        st.map(route[['lat', 'lon']])
        st.dataframe(route)
    else:
        st.error("No matching route found.")

st.subheader("All Segments Map")
st.pydeck_chart(
    pdk.Deck(
        map_style="mapbox://styles/mapbox/outdoors-v11",
        initial_view_state=pdk.ViewState(
            latitude=46.15,
            longitude=14.995,
            zoom=7,
            pitch=40,
        ),
        layers=[
            pdk.Layer(
                'ScatterplotLayer',
                data=df,
                get_position='[start_latlng_lon, start_latlng_lat]',
                get_radius=100,
                get_fill_color='[200, 30, 0, 160]',
                pickable=True,
            ),
        ],
    )
)
