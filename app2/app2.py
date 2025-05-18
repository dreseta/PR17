import streamlit as st
import pandas as pd
import pydeck as pdk
from recommendation import recommend_segments
from connect_segments import connect_segments
from osm_surface import get_surface_type

# Load cleaned segment dataset
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
    #st.write("Recommended Segments:", recommended)

    if not recommended.empty:
        # Step 2: Connect segments into a route
        route = connect_segments(recommended)
        st.write("Route columns:", route.columns.tolist())

        if not route.empty:
            # Step 3: Add 'path' column for each segment
            route["path"] = route.apply(
                lambda row: [[row['start_lon'], row['start_lat']],
                             [row['end_lon'], row['end_lat']]],
                axis=1
            )

            # Step 4: Visualize route
            st.subheader("Recommended Route on Map")
            st.pydeck_chart(
                pdk.Deck(
                    map_style="mapbox://styles/mapbox/outdoors-v11",
                    initial_view_state=pdk.ViewState(
                        latitude=route['start_lat'].iloc[0],
                        longitude=route['start_lon'].iloc[0],
                        zoom=10,
                        pitch=40,
                    ),
                    layers=[
                        pdk.Layer(
                            "PathLayer",
                            data=route,
                            get_path="path",
                            get_width=4,
                            get_color=[255, 0, 0],
                            opacity=0.8,
                        ),
                        pdk.Layer(
                            "ScatterplotLayer",
                            data=route,
                            get_position='[start_latlng_lon, start_latlng_lat]',
                            get_radius=100,
                            get_fill_color='[0, 255, 0, 160]',
                        ),
                    ],
                )
            )

            st.dataframe(route)
        else:
            st.error("Could not connect segments into a route.")
    else:
        st.warning("No recommended segments found.")

# Map of all segments (as start points)
st.subheader("All Segments in Slovenia")
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
                get_fill_color='[0, 30, 200, 160]',
                pickable=True,
            ),
        ],
    )
)
