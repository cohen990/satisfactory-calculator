from __future__ import annotations
from enum import Enum

class Resource:
    def __init__(self, type: ResourceType, amount: int):
        self.type = type
        self.amount = amount

    def __repr__(self):
        return "%s<amount:%d>" % (self.type, self.amount)

class ResourceType(Enum):
    Mined = 1
    IronOre = 2
    IronIngot = 3
    IronPlate = 4
    IronRod = 5
    ReinforcedIronPlate = 6
    Screws = 7