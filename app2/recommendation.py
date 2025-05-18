import pandas as pd

def recommend_segments(df, region, desired_length, difficulty, surface_type):
    filtered = df[df['region'] == region]

    if difficulty != "Any":
        difficulty_map = {
            "Easy": (0, 4),
            "Moderate": (4, 10),
            "Hard": (10, 20),
            "Extreme": (20, 999)
        }
        min_diff, max_diff = difficulty_map[difficulty]
        filtered = filtered[
            (filtered['climb_score'] >= min_diff) &
            (filtered['climb_score'] < max_diff)
        ]

    if surface_type != "Any":
        filtered = filtered[filtered['surface_type'] == surface_type]

    # Find combinations of segments closest to desired total length
    filtered = filtered.sort_values(by='distance')
    selected = pd.DataFrame()
    total = 0

    for _, row in filtered.iterrows():
        if total + row['distance'] <= desired_length * 1000:
            selected = pd.concat([selected, pd.DataFrame([row])])
            total += row['distance']

    return selected
