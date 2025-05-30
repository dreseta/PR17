import streamlit as st
import pandas as pd
import polyline
import json
import folium
from streamlit_folium import st_folium

from recommendation import recommend_segments  

json_path = "data/segments.json"

@st.cache_data
def load_segments(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        segments = json.load(f)

    data = []
    for seg in segments:
        if "map" in seg and "polyline" in seg["map"]:
            polyline_str = seg["map"]["polyline"]
            path = polyline.decode(polyline_str)
        else:
            polyline_str = ""
            path = []

        region = seg.get("region", [])
        if isinstance(region, list) and region:
            region = region[0]
        else:
            region = None

        data.append({
            "id": seg.get("id"),
            "name": seg.get("name"),
            "distance": seg.get("distance"),  # v metrih
            "average_grade": seg.get("average_grade"),
            "maximum_grade": seg.get("maximum_grade"),
            "total_elevation_gain": seg.get("total_elevation_gain"),
            "climb_score": seg.get("climb_score", 0),
            "region": region,
            "polyline": polyline_str,
            "path": path,
            "start_latlng_lat": seg.get("start_latlng", [None, None])[0],
            "start_latlng_lon": seg.get("start_latlng", [None, None])[1],
        })

    df = pd.DataFrame(data)
    return df

df = load_segments(json_path)

st.title("🚴‍♂️ Bike Segment Recommender - Slovenia")

st.sidebar.header("Customize Your Ride")
selected_region = st.sidebar.selectbox("Select Region", sorted(df['region'].dropna().unique()))
desired_length = st.sidebar.slider("Desired Length (km)", 1, 100, 25)
difficulty = st.sidebar.selectbox("Climb Difficulty", ["Any", "Easy", "Moderate", "Hard", "Extreme"])

# Inicializiraj stanje za recommend v session_state
if "show_recommendations" not in st.session_state:
    st.session_state.show_recommendations = False

if st.sidebar.button("Recommend Route"):
    st.session_state.show_recommendations = True

if st.session_state.show_recommendations:
    recommended = recommend_segments(df, selected_region, desired_length, difficulty)

    if not recommended.empty:
        st.subheader("Priporočeni segmenti na zemljevidu")

        sredina_lat = recommended["start_latlng_lat"].mean()
        sredina_lon = recommended["start_latlng_lon"].mean()
        m = folium.Map(location=[sredina_lat, sredina_lon], zoom_start=12)

        for _, row in recommended.iterrows():
            folium.PolyLine(row["path"], color="red", weight=4, opacity=0.8).add_to(m)

        st_folium(m, width=700, height=500)

        st.dataframe(recommended[[
            "name", "distance", "average_grade", "maximum_grade",
            "total_elevation_gain", "region"
        ]])
    else:
        st.warning("Ni bilo najdenih priporočenih segmentov.")
else:
    st.subheader("Prazni zemljevid")

    m_empty = folium.Map(location=[46.15, 14.995], zoom_start=7)
    st_folium(m_empty, width=700, height=500)

    st.write("Kliknite na gumb 'Recommend Route' v stranskem meniju za prikaz priporočil.")

def create_all_segments_map(df):
    # Za sredino zemljevida vzamemo povprečje vseh začetnih lokacij
    sredina_lat = df["start_latlng_lat"].dropna().mean()
    sredina_lon = df["start_latlng_lon"].dropna().mean()
    m = folium.Map(location=[sredina_lat, sredina_lon], zoom_start=8)

    for _, row in df.iterrows():
        if row["path"]:  # če pot ni prazna
            folium.PolyLine(row["path"], color="blue", weight=2.5, opacity=0.7).add_to(m)

    return m

# Predpostavljam, da imaš naložen df z vsemi segmenti
m_all_segments = create_all_segments_map(df)
st.subheader("Vsi segmenti v Sloveniji")
st_folium(m_all_segments, width=700, height=500)
    
