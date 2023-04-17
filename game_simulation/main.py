import json
from agents.agent import Agent
from locations.locations import Locations
from utils.text_generation import summarize_simulation

# Load town areas and people from JSON file
with open('simulation_config.json', 'r') as f:
    town_data = json.load(f)

town_people = town_data['town_people']
town_areas = town_data['town_areas']

# Initialize agents and locations
agents = []
locations = Locations()

for name, description in town_people.items():
    starting_location = description['starting_location']
    agents.append(Agent(name, description['description'], starting_location))
for name, description in town_areas.items():
    locations.add_location(name, description)

# Set default value for prompt_meta if not defined elsewhere
prompt_meta = '### Instruction:\n{}\n### Response:'

# Initialize global time and simulation variables
global_time = 0
repeats = 5

log_locations = False
log_actions = True
log_plans = False
log_ratings = False
log_memories = False

print_locations = True
print_actions = True
print_plans = True
print_ratings = False
print_memories = False

# Start simulation loop
whole_simulation_output = ""

for repeat in range(repeats):
    #log_output for one repeat
    log_output = ""

    print(f"====================== REPEAT {repeat} ======================\n")
    log_output += f"====================== REPEAT {repeat} ======================\n"
    if log_locations:
        log_output += f"=== LOCATIONS AT START OF REPEAT {repeat} ===\n"
        log_output += str(locations) + "\n"
        if print_locations:
            print(f"=== LOCATIONS AT START OF REPEAT {repeat} ===")
            print(str(locations) + "\n")
    
    # Plan actions for each agent
    for agent in agents:
        agent.plan(global_time, prompt_meta)
        if log_plans:
            log_output += f"{agent.name} plans: {agent.plans}\n"
            if print_plans:
                print(f"{agent.name} plans: {agent.plans}")
    
    # Execute planned actions and update memories
    for agent in agents:
        # Execute action
        action = agent.execute_action(agents, locations.get_location(agent.location), global_time, town_areas, prompt_meta)
        if log_actions:
            log_output += f"{agent.name} action: {action}\n"
            if print_actions:
                print(f"{agent.name} action: {action}")

        # Update memories
        for other_agent in agents:
            if other_agent != agent:
                memory = f'[Time: {global_time}. Person: {agent.name}. Memory: {action}]'
                other_agent.memories.append(memory)
                if log_memories:
                    log_output += f"{other_agent.name} remembers: {memory}\n"
                    if print_memories:
                        print(f"{other_agent.name} remembers: {memory}")

        # Compress and rate memories for each agent
        for agent in agents:
            agent.compress_memories(global_time)
            agent.rate_memories(locations, global_time, prompt_meta)
            if log_ratings:
                log_output += f"{agent.name} memory ratings: {agent.memory_ratings}\n"
                if print_ratings:
                    print(f"{agent.name} memory ratings: {agent.memory_ratings}")

    # Rate locations and determine where agents will go next
    for agent in agents:
        place_ratings = agent.rate_locations(locations, global_time, prompt_meta)
        if log_ratings:
            log_output += f"=== UPDATED LOCATION RATINGS {global_time} FOR {agent.name}===\n"
            log_output += f"{agent.name} location ratings: {place_ratings}\n"
            if print_ratings:
                print(f"=== UPDATED LOCATION RATINGS {global_time} FOR {agent.name}===\n")
                print(f"{agent.name} location ratings: {place_ratings}\n")
        
        old_location = agent.location
        new_location = agent.move(locations.get_location(place_ratings[0][0]))
        if print_locations:
            log_output += f"=== UPDATED LOCATIONS AT TIME {global_time} FOR {agent.name}===\n"
            log_output += f"{agent.name} moved from {old_location} to {new_location}\n"
        if print_ratings:
            print(f"=== UPDATED LOCATIONS AT TIME {global_time} FOR {agent.name}===\n")
            print(f"{agent.name} moved from {old_location} to {new_location}\n")

    print(f"----------------------- SUMMARY FOR REPEAT {repeat} -----------------------")

    print(summarize_simulation(log_output=log_output))

    whole_simulation_output += log_output

    # Increment time
    global_time += 1

# Write log output to file
with open('simulation_log.txt', 'w') as f:
    f.write(whole_simulation_output)