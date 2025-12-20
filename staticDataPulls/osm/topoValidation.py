import geopandas as gpd
import networkx as nx
from shapely import Point, LineString

waysGdf = gpd.read_parquet("ways.parquet")
nodesGdf = gpd.read_parquet("nodes.parquet")

nodesGdf = nodesGdf.set_crs(3082, allow_override=True)
waysGdf = waysGdf.set_crs(3082, allow_override=True)


G = nx.Graph()

for _, row in nodesGdf.iterrows():
    nid = row["id"]
    G.add_node(
        nid,
        x=row.geometry.x,
        y=row.geometry.y,
        geom=row.geometry,
        **{k: v for k, v in row.items() if k not in ["geometry", "id"]}
    )
    
for _, row in waysGdf.iterrows():
    wid = row["id"]
    nodeList = row["nodes"]

    if not isinstance(nodeList, (list, tuple)) or len(nodeList) < 2:
        continue

