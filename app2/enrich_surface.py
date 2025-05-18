# enrich_surface.py
from osm_surface import get_surface_type
import pandas as pd

def enrich_with_surface(input_csv, output_csv):
    df = pd.read_csv(input_csv)
    surface_types = []
    for _, row in df.iterrows():
        surface = get_surface_type(row['start_latlng_lat'], row['start_latlng_lon'],
                                   row['end_latlng_lat'], row['end_latlng_lon'])
        print(surface)
        surface_types.append(surface)
    df['surface_type'] = surface_types
    df.to_csv(output_csv, index=False)
    print("Surface types added.")

if __name__ == "__main__":
    enrich_with_surface("data/cleaned_segments.csv", "data/segments_w_surface.csv")
