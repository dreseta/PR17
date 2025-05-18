import json
import pandas as pd

def parse_latlng(latlng):
    if latlng and isinstance(latlng, list) and len(latlng) == 2:
        return latlng[0], latlng[1]
    return None, None

def flatten_json_to_csv(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    rows = []
    for segment in data:
        start_lat, start_lon = parse_latlng(segment.get("start_latlng"))
        end_lat, end_lon = parse_latlng(segment.get("end_latlng"))

        row = {
            "id": segment.get("id"),
            "name": segment.get("name"),
            "region": segment.get("region", "unknown"),
            "distance": segment.get("distance", 0),
            "climb_score": segment.get("climb_score", 0),
            "effort_count": segment.get("effort_count", 0),
            "start_latlng_lat": start_lat,
            "start_latlng_lon": start_lon,
            "end_latlng_lat": end_lat,
            "end_latlng_lon": end_lon,
            "average_grade": segment.get("average_grade"),
            "maximum_grade": segment.get("maximum_grade"),
            "total_elevation_gain": segment.get("total_elevation_gain"),
            "surface_type": segment.get("surface_type", "unknown")
        }

        rows.append(row)

    df = pd.DataFrame(rows)
    df.to_csv(output_file, index=False)
    print(f"Saved {len(df)} segments to {output_file}")

# Example usage
if __name__ == "__main__":
    flatten_json_to_csv("data/segments.json", "data/cleaned_segments.csv")
