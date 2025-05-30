import pandas as pd

def recommend_segments(df, region, desired_length, difficulty):
    # Filtriraj po regiji
    filtered = df[df['region'] == region].copy()

    # Filtriraj po težavnosti
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

    # Sortiraj po razdalji (v metrih)
    filtered = filtered.sort_values(by='distance')

    selected = []
    total_distance = 0

    # Izberi segmente dokler skupna dolžina ne preseže želene dolžine
    for _, row in filtered.iterrows():
        if total_distance + row['distance'] <= desired_length * 1000:
            selected.append(row)
            total_distance += row['distance']

    # Prevedi iz seznama Series v DataFrame
    if selected:
        selected_df = pd.DataFrame(selected).reset_index(drop=True)
    else:
        selected_df = pd.DataFrame(columns=df.columns)

    return selected_df
