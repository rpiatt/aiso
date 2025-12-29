import geopandas as gpd
import networkx as nx
from shapely.geometry import Point, LineString
import pickle

waysGdf = gpd.read_parquet("ways.parquet")
nodesGdf = gpd.read_parquet("nodes.parquet")

nodesGdf = nodesGdf.set_crs(4326, allow_override=True)
waysGdf = waysGdf.set_crs(4326, allow_override=True)

nodesGdf = nodesGdf.to_crs(epsg=3082)
waysGdf = waysGdf.to_crs(epsg=3082)

print('data loaded')

# print(waysGdf.geometry.iloc[0].coords[:5])

def snap(x, y, tol=0.1):
    return round(x / tol) * tol, round(y / tol) * tol


# print(waysGdf.columns)
# print(nodesGdf.columns)

G = nx.MultiGraph()

for _, row in waysGdf.iterrows():
    geom = row.geometry

    if geom is None or geom.geom_type != "LineString":
        continue

    coords = list(geom.coords)

    for (x1, y1), (x2, y2) in zip(coords[:-1], coords[1:]):
        u = snap(x1, y1)
        v = snap(x2, y2)

        segment = LineString([u, v])

        G.add_edge(
            u,
            v,
            segmentGeom=segment,
            way_id=row["id"],
            power=row.get("power", None),
            voltage=row.get("voltage", None),
            circuits=row.get("circuits", None),
            length=segment.length
        )

print('edges graphed')

#for node in G.nodes:
#    G.nodes[node]['x'] = node[0]
#    G.nodes[node]['y'] = node[1]
#    G.nodes[node]['geom'] = Point(node)

nx.set_node_attributes(G, {n: n[0] for n in G.nodes}, "x")
nx.set_node_attributes(G, {n: n[1] for n in G.nodes}, "y")
nx.set_node_attributes(G, {n: Point(n) for n in G.nodes}, "geom")

print('node attributes set')


print("Nodes:", G.number_of_nodes())
print("Edges:", G.number_of_edges())
print("Connected components:", nx.number_connected_components(G))

with open("topoGraph.pkl", "wb") as f:
    pickle.dump(G, f)
