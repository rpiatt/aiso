import math
import pandas as pd


# texas bbox
min_lat, max_lat = 26, 36.6
min_lon, max_lon = -107, -93
zoom = 18


# functions
def latlon_to_tile(lat, lon, zoom):
    lat_rad = math.radians(lat)
    n = 2 ** zoom
    x = int((lon + 180.0) / 360.0 * n)
    y = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
    return x, y


def tile_to_quadkey(x, y, zoom):
    quadkey = ""
    for i in range(zoom, 0, -1):
        digit = 0
        mask = 1 << (i - 1)
        if (x & mask) != 0:
            digit += 1
        if (y & mask) != 0:
            digit += 2
        quadkey += str(digit)
    return quadkey


# --- Compute tile ranges ---
x_min, y_max = latlon_to_tile(min_lat, min_lon, zoom)
x_max, y_min = latlon_to_tile(max_lat, max_lon, zoom)

# --- Generate quadkeys ---
quadkeys = [tile_to_quadkey(x, y, zoom)
            for x in range(x_min, x_max + 1)
            for y in range(y_min, y_max + 1)]

print(f"Number of quadkeys covering Texas: {len(quadkeys)}")

# --- Load global building links CSV ---
csv = pd.read_csv(r"https://minedbuildings.z5.web.core.windows.net/global-buildings/dataset-links.csv",
                  header=0)

# --- Filter to Texas quadkeys ---
texas_tiles = csv[csv["QuadKey"].isin(quadkeys)]
print(f"Number of files to download: {len(texas_tiles)}")

# --- Save filtered CSV ---
texas_tiles.to_csv("texas_buildings_links.csv", index=False)
print("Saved CSV: texas_buildings_links.csv")
