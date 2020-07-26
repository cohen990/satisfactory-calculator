import miner
import constructor
import smelter
import resource_chain
from base import Resource, Deposits


def calc(resource, number_of_deposits, deposit_type, deposit_quality):
    deposits = Deposits(deposit_type, deposit_quality, number_of_deposits)

    chain = resource_chain.calc(resource)
    last_link = miner.calc(deposits)
    blueprints = [last_link]

    for recipe in chain:
        print(recipe)
        blueprints.append(get_blueprint_for(recipe, last_link))
        last_link = recipe

    out_string = ""

    for blueprint in blueprints:
        out_string += str(blueprint) + "\n"

    return out_string


def get_blueprint_for(recipe, last_link):
    print(recipe)
    if recipe.resource_out.name == "iron ingot":
        print("doing smelter")
        return smelter.calc(recipe.resource_out)
    print("doing constructor")
    return constructor.calc(recipe.resource_out)
