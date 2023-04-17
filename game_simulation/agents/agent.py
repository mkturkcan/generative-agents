import random
from utils.text_generation import generate, get_rating

class Agent:
     
    """
    A class to represent an individual agent in a simulation similar to The Sims.

    Attributes:
    -----------
    name : str
        The name of the agent.
    description : str
        A brief description of the agent.
    location : str
        The current location of the agent in the simulated environment.
    memories : list
        A list of memories the agent has about their interactions.
    compressed_memories : list
        A list of compressed memories that summarize the agent's experiences.
    plans : str
        The agent's daily plans, generated at the beginning of each day.

    Methods:
    --------
    plan(global_time, town_people, prompt_meta):
        Generates the agent's daily plan.
    
    execute_action(other_agents, location, global_time, town_areas, prompt_meta):
        Executes the agent's action based on their current situation and interactions with other agents.
    
    update_memories(other_agents, global_time, action_results):
        Updates the agent's memories based on their interactions with other agents.
    
    compress_memories(memory_ratings, global_time, MEMORY_LIMIT=10):
        Compresses the agent's memories to a more manageable and relevant set.
    
    rate_locations(locations, town_areas, global_time, prompt_meta):
        Rates different locations in the simulated environment based on the agent's preferences and experiences.
    """
     
    def __init__(self, name, description, location=None):
        self.name = name
        self.description = description
        self.location = location
        self.memory_ratings = []
        self.memories = []
        self.compressed_memories = []
        self.plans = ""
        
    def __repr__(self):
        return f"Agent({self.name}, {self.description}, {self.location})"
    
    def plan(self, global_time, prompt_meta):
        prompt = "You are {}. The following is your description: {} You just woke up. What is your goal for today? Write it down in an hourly basis, starting at {}:00. Write only one or two very short sentences. Be very brief. Use at most 50 words.".format(self.name, self.description, str(global_time))
        self.plans = generate(prompt_meta.format(prompt))
    
    def execute_action(self, other_agents, location, global_time, town_areas, prompt_meta):
        people = [agent.name for agent in other_agents if agent.location == location]
        
        prompt = "You are {}. Your plans are: {}. You are currently in {} with the following description: {}. It is currently {}:00. The following people are in this area: {}. You can interact with them.".format(self.name, self.plans, location.name, town_areas[location.name], str(global_time), ', '.join(people))
        
        people_description = [f"{agent.name}: {agent.description}" for agent in other_agents if agent.location == location.name]
        prompt += ' You know the following about people: ' + '. '.join(people_description)
        
        prompt += "What do you do in the next hour? Use at most 10 words to explain."
        action = generate(prompt_meta.format(prompt))
        return action
    
    def update_memories(self, other_agents, global_time, action_results):
        for agent in other_agents:
            if agent.location == self.location:
                self.memories.append('[Time: {}. Person: {}. Memory: {}]\n'.format(str(global_time), agent.name, action_results[agent.name]))

    def compress_memories(self, global_time, MEMORY_LIMIT=10):
        memories_sorted = sorted(self.memory_ratings, key=lambda x: x[1], reverse=True)
        relevant_memories = memories_sorted[:MEMORY_LIMIT]
        memory_string_to_compress = '.'.join([a[0] for a in relevant_memories])
        return '[Recollection at Time {}:00: {}]'.format(str(global_time), memory_string_to_compress)
    
    def rate_memories(self, locations, global_time, prompt_meta):
        memory_ratings = []
        for memory in self.memories:
            prompt = "You are {}. Your plans are: {}. You are currently in {}. It is currently {}:00. You observe the following: {}. Give a rating, between 1 and 5, to how much you care about this.".format(self.name, self.plans, locations.get_location(self.location), str(global_time), memory)
            res = generate(prompt_meta.format(prompt))
            rating = get_rating(res)
            max_attempts = 2
            current_attempt = 0
            while rating is None and current_attempt < max_attempts:
                rating = get_rating(res)
                current_attempt += 1
            if rating is None:
                rating = 0
            memory_ratings.append((memory, rating, res))
        self.memory_ratings = memory_ratings
        return memory_ratings


    def rate_locations(self, locations, global_time, prompt_meta):
        place_ratings = []
        for location in locations.locations.values():
            prompt = "You are {}. Your plans are: {}. It is currently {}:00. You are currently at {}. How likely are you to go to {} next?".format(self.name, self.plans, str(global_time), locations.get_location(self.location), location.name)
            res = generate(prompt_meta.format(prompt))
            rating = get_rating(res)
            max_attempts = 2
            current_attempt = 0
            while rating is None and current_attempt < max_attempts:
                rating = get_rating(res)
                current_attempt += 1
            if rating is None:
                rating = 0
            place_ratings.append((location.name, rating, res))
        self.place_ratings = place_ratings
        return sorted(place_ratings, key=lambda x: x[1], reverse=True)
    
    def move(self, new_location):
        self.location = new_location.name
        return new_location

