from __future__ import annotations

from recipes import Recipe
from resources import *

class PlanTargetAmount:
    def __init__(self, entry_point: ResourceType, target_per_minute: Resource):
        self.entry_point = entry_point
        self.target = target_per_minute

class NodeType(Enum):
    RouteNode = 1
    BranchNode = 2

class Node:
    def __init__(self, type: NodeType):
        self.type = type

class RouteNode(Node):
    def __init__(self, recipe: Recipe, utilisation: float):
        super().__init__(NodeType.RouteNode)
        self.recipe = recipe
        self.utilisation = utilisation
        self.prior: list[Node] = []

    def __repr__(self):
        return "RouteNode<%s, utilisation:%f>" % (self.recipe, self.utilisation)

class BranchNode(Node):
    def __init__(self, branches: list[Branch]):
        super().__init__(NodeType.BranchNode)
        self.branches: list[Branch] = branches

class Branch:
    def __init__(self):
        self.nodes = []