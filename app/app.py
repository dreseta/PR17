import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from models.recommendation_model import SegmentRecommender
from routing.segment_connector import get_shortest_path_between_segments, get_path_coordinates
from routing.surface_detection import detect_surface_type

# Load your data
df = pd.read_json('data/segments.json')  # Should contain columns as described

# Initialize recommender
recommender = SegmentRecommender(df)

st.title("🚴‍♂️ Kje danes kolesarim?")
st.markdown("Interaktivno orodje za izbiro optimalne kolesarske poti po Sloveniji")

# Sidebar inputs
region = st.selectbox("Izberi regijo", sorted(df['region']))#.unique()))
length = st.slider("Dolžina poti (v km)", 2, 100, 20)
difficulty = st.selectbox("Težavnost", ['Zelo lahka', 'Lahka', 'Srednja', 'Težka', 'Zelo težka'])

difficulty_map = {
    'Zelo lahka': 2,
    'Lahka': 6,
    'Srednja': 15,
    'Težka': 25,
    'Zelo težka': 50,
}

user_input = {
    'distance': length * 1000,
    'climb_score': difficulty_map[difficulty]
}

# Filter by region before recommending
filtered_df = df[df['region'] == region].reset_index(drop=True)
recommender = SegmentRecommender(filtered_df)
recommended = recommender.recommend(user_input)

st.subheader("📍 Priporočeni segmenti")
st.write(recommended[['name', 'distance', 'climb_score', 'effort_count']])

# Map display
st.subheader("🗺️ Priporočena pot")
segment_coords = [row['start_latlng'] for _, row in recommended.iterrows()]
path, G = get_shortest_path_between_segments(segment_coords)
path_coords = get_path_coordinates(path, G)

m = folium.Map(location=segment_coords[0], zoom_start=10)
folium.PolyLine(locations=path_coords, color="blue", weight=4).add_to(m)

# Add start/end markers
for i, coord in enumerate(segment_coords):
    folium.Marker(location=coord, popup=f"Segment {i+1}").add_to(m)

st_data = st_folium(m, width=800)

# Surface type detection
st.subheader("🛣️ Tipi podlage")
for _, row in recommended.iterrows():
    surface = detect_surface_type(row['start_latlng'], row['end_latlng'])
    st.write(f"Segment **{row['name']}**: {surface}")
