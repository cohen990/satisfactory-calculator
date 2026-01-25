from factory import get_targets
from producers import Producer
from recipes import Recipe
from resources import Resource, ResourceType


def test_pulls_out_targets_from_recipe():
    recipe = Recipe(Producer.Assembler, [Resource(ResourceType.IronIngot, 1)], Resource(ResourceType.IronPlate, 1), 60)
    targets = get_targets(ResourceType.IronOre, recipe, 1) 

    assert len(targets) == 1
    assert targets[0].amount == 1
    assert targets[0].type == ResourceType.IronIngot


def test_computes_target_amount_per_minute():
    recipe = Recipe(Producer.Assembler, [Resource(ResourceType.IronIngot, 1)], Resource(ResourceType.IronPlate, 1), 6)
    targets = get_targets(ResourceType.IronOre, recipe, 1) 

    assert len(targets) == 1
    assert targets[0].amount == 10
    assert targets[0].type == ResourceType.IronIngot

def test_attenuates_amount_by_utilisation():
    recipe = Recipe(Producer.Assembler, [Resource(ResourceType.IronIngot, 1)], Resource(ResourceType.IronPlate, 1), 6)
    targets = get_targets(ResourceType.IronOre, recipe, 0.5) 

    assert len(targets) == 1
    assert targets[0].amount == 5
    assert targets[0].type == ResourceType.IronIngot