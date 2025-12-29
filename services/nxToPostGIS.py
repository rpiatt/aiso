import json
import pickle
import networkx as nx
import geopandas as gpd
import pandas as pd

from shapely.geometry import Point, LineString
from sqlalchemy import create_engine, text

PICKLE_PATH = ""
DB_URL = ""

NODES_TABLE = ""
EDGES_TABLE = ""