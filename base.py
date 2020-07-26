class Blueprint:
    def __init__(self, building, number, resource_in, resource_out):
        self.building = building
        self.number = number
        self.resource_in = resource_in
        self.resource_out = resource_out

    def __str__(self):
        return f'{self.building}, {self.number:g}, {self.resource_out}'


class Resource:
    def __init__(self, name, amount_per_minute):
        self.name = name
        self.amount_per_minute = amount_per_minute

    def __str__(self):
        return f'{self.name}, {self.amount_per_minute:g}'


class Recipe:
    def __init__(self, resource_in, resource_out):
        self.resource_in = resource_in
        self.resource_out = resource_out

    def __str__(self):
        return f'{self.resource_in}, {self.resource_out}'


class Deposits:
    def __init__(self, resource, quality, number_of_deposits):
        self.resource = resource
        self.quality = quality
        self.number_of_deposits = number_of_deposits
