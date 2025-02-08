

from utils.text_generation import summarize_simulation
from utils.time import global_time
from utils.logs import log_output
from utils.states import locations, whole_simulation_output, town_areas, town_people, world_graph
from utils.configs import repeats, log_locations, print_locations, use_openai
from agents.agent import Agent

# Initialize agents and locations
for name, description in town_areas.items():
    locations.add_location(name, description)

for name, description in town_people.items():
    starting_location = description['starting_location']
    agent = Agent(name, description['description'], starting_location, world_graph, use_openai)
    locations.get_location(starting_location).add_people(agent)

for repeat in range(repeats):
    if log_locations:
        log_output += f"=== LOCATIONS AT START OF REPEAT {repeat} ===\n"
        log_output += str(locations) + "\n"
        if print_locations:
            print(f"=== LOCATIONS AT START OF REPEAT {repeat} ===")
            print(str(locations) + "\n")
    
    # Plan actions for each location and agent
    for location_key in locations.get_locations():
        print(f"====================== {location_key} REPEAT {repeat} ======================\n")
        log_output[location_key] =  f"====================== {location_key} REPEAT {repeat} ======================\n"
        location = locations.get_location(location_key)
        for agent in location.get_people():
            agent.tick()
        print(log_output[location_key])
        print(summarize_simulation(log_output=log_output[location_key]))

        whole_simulation_output += log_output[location_key]
        print(f"----------------------- SUMMARY FOR REPEAT {repeat} -----------------------")

    global_time += 1

# Write log output to file
with open('simulation_log.txt', 'w') as f:
    f.write(whole_simulation_output)