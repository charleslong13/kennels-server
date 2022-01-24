class Location():
    ''' creating a Location class'''
    def __init__(self, id, name, address):
        self.id = id
        self.name = name
        self.address = address
new_location = Location(3, "Nashville East", "123 legit address")