import requests

url = "https://download.geofabrik.de/north-america/us/texas-latest.osm.pbf"
out_file = "texas-latest.osm.pbf"

with requests.get(url, stream=True) as r:
    r.raise_for_status()
    with open(out_file, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)

print(f"Downloaded {out_file}")
