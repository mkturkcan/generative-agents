class Location:
    """
    A class to represent a location in the simulated environment.

    Attributes:
    ----------
    name : str
        The name of the location.
    description : str
        A brief description of the location.

    Methods:
    -------
    describe():
        Prints the description of the location.
    """

    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.people = []
    
    def __str__(self):
        return self.name
    
    def add_people(self, people):
        if isinstance(people, list):
            self.people = self.people + people
        else:
            self.people = self.people + [people]

    def get_people(self):
        return self.people
        
    
    def describe(self):
        print(self.description)

class Locations:
    """
    A class to represent a collection of locations in the simulated environment.

    Attributes:
    ----------
    locations : dict
        A dictionary of locations, with keys as the location names and values as Location objects.

    Methods:
    -------
    add_location(name, description):
        Adds a new location to the collection.
    
    get_location(name):
        Returns the Location object with the given name.
    
    __str__():
        Returns a string representation of the collection of locations.
    """
    
    def __init__(self):
        self.locations = {}

    def add_location(self, name, description):
        self.locations[name] = Location(name, description)

    def get_locations(self):
        return self.locations

    def get_location(self, name):
        return self.locations.get(name)

    def __str__(self):
        return '\n'.join([str(location) for location in self.locations.values()])

    

