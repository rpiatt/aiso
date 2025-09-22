import osmium

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
