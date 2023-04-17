class Location:
    def __init__(self, name, description):
        self.name = name
        self.description = description
    
    def __str__(self):
        return self.name
    
    def describe(self):
        print(self.description)

class Locations:
    def __init__(self):
        self.locations = {}

    def add_location(self, name, description):
        self.locations[name] = Location(name, description)

    def get_location(self, name):
        return self.locations.get(name)

    def __str__(self):
        return '\n'.join(str(loc) for loc in self.locations.values())
    

