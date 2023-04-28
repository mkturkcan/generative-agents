class Space:
    """
    A class to represent a space in the simulated environment.

    Attributes:
    ----------
    name : str
        The name of the space.
    description : str
        A brief description of the space.

    Methods:
    -------
    describe():
        Prints the description of the space.
    """

    def __init__(self, name, description, shape="cube", scale=[1,1,1], position=[0,0,0]):
        self.name = name
        self.description = description
        self.shape = shape
        self.scale = scale
        
    
    def __str__(self):
        return self.name
    
    def describe(self):
        print(self.description)

class Spaces:
    """
    A class to represent a collection of spaces in the simulated environment.

    Attributes:
    ----------
    spaces : dict
        A dictionary of spaces, with keys as the space names and values as space objects.

    Methods:
    -------
    add_space(name, description):
        Adds a new space to the collection.
    
    get_space(name):
        Returns the space object with the given name.
    
    __str__():
        Returns a string representation of the collection of spaces.
    """
    
    def __init__(self):
        self.spaces = {}

    def add_space(self, name, description):
        self.spaces[name] = Space(name, description)

    def get_space(self, name):
        return self.spaces.get(name)

    def __str__(self):
        return '\n'.join([str(space) for space in self.spaces.values()])

    

