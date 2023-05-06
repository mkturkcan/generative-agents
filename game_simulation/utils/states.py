import json
import networkx as nx
from locations.locations import Locations

# Load town areas and people from JSON file
with open('simulation_config.json', 'r') as f:
    town_data = json.load(f)

town_people = town_data['town_people']
town_areas = town_data['town_areas']

locations = Locations()

# Create world_graph
world_graph = nx.Graph()
last_town_area = None
for town_area in town_areas.keys():
    world_graph.add_node(town_area)
    world_graph.add_edge(town_area, town_area)  # Add an edge to itself
    if last_town_area is not None:
        world_graph.add_edge(town_area, last_town_area)
    last_town_area = town_area

# Add the edge between the first and the last town areas to complete the cycle
world_graph.add_edge(list(town_areas.keys())[0], last_town_area)

whole_simulation_output = ""


