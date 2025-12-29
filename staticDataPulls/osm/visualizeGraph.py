import pickle
import networkx as nx
import matplotlib.pyplot as plt

with open("graph.pkl", "rb") as f:
    G = pickle.load(f)

print("Graph type: ", type(G))
print(nx.info(G))

