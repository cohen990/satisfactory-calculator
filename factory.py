from recipes import *
from planning import Branch, BranchNode, Node, NodeType, PlanTargetAmount, RouteNode

class Factory:
    def __init__(self, recipes = default_recipes):
        self.recipes: list[Recipe] = recipes

    def compute_route(self, plan: PlanTargetAmount):
        entry_node = RouteNode(None, 1)
        unplanned_nodes: list[tuple[RouteNode, list[Resource]]] = [(entry_node, [plan.target])]

        # what we want is that when we find multiple recipes that provide the same resource, we should create a fork node that marks its children as divergent
        while(len(unplanned_nodes) > 0):
            current_node, targets = unplanned_nodes.pop()
            for target in targets:
                branches = []
                for recipe in self.recipes:
                    if(recipe.output.type == target.type):
                        branch = Branch()
                        branches.append(branch)
                        needed = target.amount
                        while(needed > 0):
                            node = RouteNode(recipe, min(needed / recipe.output_per_minute, 1))
                            branch.nodes.append(node)
                            needed -= recipe.output_per_minute
                            node_targets = get_targets(plan.entry_point, recipe, node.utilisation)
                            if len(targets) > 0:
                                unplanned_nodes.append([node, node_targets])
                if len(branches) == 1:
                    current_node.prior.extend(branch.nodes)
                if len(branches) > 1:
                    current_node.prior.append(BranchNode(branches))
                    


        unverified_nodes: list[Node] = entry_node.prior.copy()

        while(len(unverified_nodes) > 0):
            node = unverified_nodes.pop()
            if node.type == NodeType.BranchNode:
                shortest_branch = None
                for branch in node.branches:
                    if(shortest_branch == None or branch.nodes[0].recipe.output.amount > shortest_branch.nodes[0].recipe.output.amount):
                        shortest_branch = branch
                    unverified_nodes.extend(shortest_branch.nodes)
            else:
                if len(node.prior) == 0:
                    for input in node.recipe.inputs:
                        if input.type != plan.entry_point:
                            raise Exception("No valid route found") 
                else:
                    unverified_nodes.extend(node.prior)
        



        return entry_node

def get_targets(entry_point: ResourceType, recipe: Recipe, node_utilisation: float) -> list[Resource]:
    targets = []
    for input in recipe.inputs:
        required_per_minute = node_utilisation * (60/recipe.duration) * input.amount 
        if(entry_point != input.type):
            new_target = Resource(input.type, required_per_minute)
            targets.append(new_target)
    return targets
