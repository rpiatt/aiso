import osmium
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, LineString
import pyarrow      # required for the .to_parquet() method; line 77-78

class PowerHandler(osmium.SimpleHandler):
    def __init__(self):
        super().__init__()
        self.nodes = []
        self.ways = []
        self.relations = []

    def node(self, n):
        if "power" in n.tags:
            self.nodes.append({
                "id": n.id,
                "lat": n.location.lat,
                "lon": n.location.lon,
                "tags": dict(n.tags)
            })

    def way(self, w):
        if "power" in w.tags:
            self.ways.append({
                "id": w.id,
                "nodes": [n.ref for n in w.nodes],
                "tags": dict(w.tags)
            })

    def relation(self, r):
        if "power" in r.tags:
            self.relations.append({
                "id": r.id,
                "members": [(m.type, m.ref, m.role) for m in r.members],
                "tags": dict(r.tags)
            })

# Run handler on Texas extract
handler = PowerHandler()
handler.apply_file("texas-latest.osm.pbf", locations=True)

print(f"Found {len(handler.nodes)} power nodes")
print(f"Found {len(handler.ways)} power ways")
print(f"Found {len(handler.relations)} power relations")

# --- Convert nodes list to DataFrame ---
nodes_df = pd.DataFrame(handler.nodes)
nodes_df["geometry"] = [Point(xy) for xy in zip(nodes_df.lon, nodes_df.lat)]
nodes_gdf = gpd.GeoDataFrame(nodes_df, geometry="geometry", crs="EPSG:3082")

# Build lookup: node_id -> (lon, lat)
node_lookup = {row["id"]: (row["lon"], row["lat"]) for _, row in nodes_df.iterrows()}

# --- Convert ways list to GeoDataFrame ---
def way_to_geometry(node_ids):
    coords = [node_lookup[nid] for nid in node_ids if nid in node_lookup]
    if len(coords) >= 2:
        return LineString(coords)
    return None  # skip degenerate ways

ways_df = pd.DataFrame(handler.ways)
ways_df["geometry"] = ways_df["nodes"].apply(way_to_geometry)
ways_df = ways_df.dropna(subset=["geometry"])

# Convert to GeoDataFrame
ways_gdf = gpd.GeoDataFrame(ways_df, geometry="geometry", crs="EPSG:3082")


# separate tags into columns
ways_gdf = pd.concat(
    [ways_gdf.drop(columns=["tags"]), ways_gdf["tags"].apply(pd.Series)],
    axis=1
)


nodes_gdf.to_parquet("nodes.parquet")
ways_gdf.to_parquet("ways.parquet")
