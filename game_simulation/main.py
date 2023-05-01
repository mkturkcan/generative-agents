import json
import networkx as nx
from agents.agent import Agent
from locations.locations import Locations
from utils.text_generation import summarize_simulation
import sys
import logging

logging.basicConfig(filename='simulation.log', encoding='utf-8', level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

# Set default value for prompt_meta if not defined elsewhere
prompt_meta = '### Instruction:\n{}\n### Response:'

# Initialize global time and simulation variables
global_time = 0
repeats = 1

use_openai = True

# Load town areas and people from JSON file
with open('simulation_config.json', 'r') as f:
    town_data = json.load(f)

town_people = town_data['town_people']
town_areas = town_data['town_areas']

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

# Initialize agents and locations
agents = []
locations = Locations()


for name, description in town_people.items():
    starting_location = description['starting_location']
    agents.append(Agent(name, description['description'], starting_location, world_graph, use_openai))

for name, description in town_areas.items():
    locations.add_location(name, description)

for repeat in range(repeats):

    logging.info(f"====================== REPEAT {repeat} ======================\n")
    logging.info(f"=== LOCATIONS AT START OF REPEAT {repeat} ===\n")
    logging.info(str(locations) + "\n")

    # Plan actions for each agent
    for agent in agents:
        agent.plan(global_time, prompt_meta)
        logging.info(f"{agent.name} plans: {agent.plans}\n")

    # Execute planned actions and update memories
    for agent in agents:
        # Execute action
        action = agent.execute_action(agents, locations.get_location(agent.location), global_time, town_areas, prompt_meta)
        logging.info(f"{agent.name} action: {action}\n")

        # Update memories
        for other_agent in agents:
            if other_agent != agent:
                memory = f'[Time: {global_time}. Person: {agent.name}. Memory: {action}]'
                other_agent.memories.append(memory)

                logging.info(f"{other_agent.name} remembers: {memory}\n")

        # Compress and rate memories for each agent
        for agent in agents:
            agent.compress_memories(global_time)
            agent.rate_memories(locations, global_time, prompt_meta)

            logging.info(f"{agent.name} memory ratings: {agent.memory_ratings}\n")

    # Rate locations and determine where agents will go next
    for agent in agents:
        place_ratings = agent.rate_locations(locations, global_time, prompt_meta)

        logging.info(f"=== UPDATED LOCATION RATINGS {global_time} FOR {agent.name}===\n")
        logging.info(f"{agent.name} location ratings: {place_ratings}\n")

        old_location = agent.location

        new_location_name = place_ratings[0][0]
        agent.move(new_location_name)

        logging.info(f"=== UPDATED LOCATIONS AT TIME {global_time} FOR {agent.name}===\n")
        logging.info(f"{agent.name} moved from {old_location} to {new_location_name}\n")

    # print(summarize_simulation(log_output=log_output))

    # Increment time
    global_time += 1
