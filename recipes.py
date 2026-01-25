from producers import Producer
from resources import *

class Recipe:
    def __init__(self, producer: Producer, inputs: list[Resource], output: Resource, duration: float):
        self.producer = producer
        self.inputs = inputs
        self.output = output
        self.duration = duration

        runs_per_minute = duration / 60
        self.output_per_minute = output.amount / runs_per_minute

    def __repr__(self):
        return "Recipe<%s,inputs:%s, output:%s, duration:%d>"% (self.producer, self.inputs, self.output, self.duration)

default_recipes = [
    Recipe(Producer.MinerLvl1, [Resource(ResourceType.Mined, 1)], Resource(ResourceType.IronOre, 1), 0.5),
    Recipe(Producer.Smelter, [Resource(ResourceType.IronOre, 1)], Resource(ResourceType.IronIngot, 1), 2),
    Recipe(Producer.Constructor, [Resource(ResourceType.IronIngot, 3)], Resource(ResourceType.IronPlate,2), 6),
    Recipe(Producer.Constructor, [Resource(ResourceType.IronIngot, 1)], Resource(ResourceType.IronRod,1), 4),
    Recipe(Producer.Constructor, [Resource(ResourceType.IronRod, 1)], Resource(ResourceType.Screws,4), 6),
    Recipe(Producer.Assembler, [Resource(ResourceType.IronPlate, 6), Resource(ResourceType.Screws, 12)], Resource(ResourceType.ReinforcedIronPlate,1), 12)
]