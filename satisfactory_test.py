import math

import pytest
from planning import PlanTargetAmount
from producers import Producer
from recipes import Recipe
from resources import *
from factory import Factory

factory = Factory()

def test_fails_to_route_an_impossible_plan():
    plan = PlanTargetAmount(
        ResourceType.IronPlate,
        Resource(ResourceType.IronOre, 20)
    )

    with pytest.raises(Exception):
        factory.compute_route(plan)

def test_computes_utilisation():
    plan = PlanTargetAmount(
        ResourceType.IronIngot,
        Resource(ResourceType.IronPlate, 10)
    )

    route_node = factory.compute_route(plan)

    child_node = route_node.prior[0]

    assert child_node.utilisation == 0.5

def test_routing_iron_plates():
    plan = PlanTargetAmount(
        ResourceType.IronIngot,
        Resource(ResourceType.IronPlate, 20)
    )

    route_node = factory.compute_route(plan)

    assert len(route_node.prior) == 1
    child_node = route_node.prior[0]

    assert child_node.recipe.producer == Producer.Constructor
    assert child_node.recipe.inputs[0].type == ResourceType.IronIngot
    assert child_node.recipe.output.type == ResourceType.IronPlate
    assert len(child_node.prior) == 0

def test_routing_iron_rods():
    plan = PlanTargetAmount(
        ResourceType.IronIngot,
        Resource(ResourceType.IronRod, 15)
    )

    route_node = factory.compute_route(plan)

    assert len(route_node.prior) == 1
    child_node = route_node.prior[0]

    assert child_node.recipe.producer == Producer.Constructor
    assert child_node.recipe.inputs[0].type == ResourceType.IronIngot
    assert child_node.recipe.output.type == ResourceType.IronRod
    assert len(child_node.prior) == 0

def test_route_requiring_multiple_producers():
    plan = PlanTargetAmount(
        ResourceType.IronIngot,
        Resource(ResourceType.IronRod, 30)
    )

    route_node = factory.compute_route(plan)

    assert len(route_node.prior) == 2

    first_child = route_node.prior[0]

    assert first_child.recipe.producer == Producer.Constructor
    assert first_child.recipe.inputs[0].type == ResourceType.IronIngot
    assert first_child.recipe.output.type == ResourceType.IronRod

    second_child = route_node.prior[1]

    assert second_child.recipe.producer == Producer.Constructor
    assert second_child.recipe.inputs[0].type == ResourceType.IronIngot
    assert second_child.recipe.output.type == ResourceType.IronRod
    assert len(second_child.prior) == 0

def test_route_requiring_multiple_steps():
    plan = PlanTargetAmount(
        ResourceType.IronOre,
        Resource(ResourceType.IronRod, 15)
    )

    route_node = factory.compute_route(plan)

    assert len(route_node.prior) == 1

    first_child = route_node.prior[0]
    assert len(first_child.prior) == 1

    assert first_child.recipe.producer == Producer.Constructor
    assert first_child.recipe.inputs[0].type == ResourceType.IronIngot
    assert first_child.recipe.output.type == ResourceType.IronRod

    second_child = first_child.prior[0]

    assert second_child.recipe.producer == Producer.Smelter
    assert second_child.recipe.inputs[0].type == ResourceType.IronOre
    assert second_child.recipe.output.type == ResourceType.IronIngot
    assert len(second_child.prior) == 0

def test_route_requiring_multiple_steps():
    plan = PlanTargetAmount(
        ResourceType.IronOre,
        Resource(ResourceType.IronRod, 15)
    )

    route_node = factory.compute_route(plan)

    assert len(route_node.prior) == 1

    first_child = route_node.prior[0]
    assert len(first_child.prior) == 1

    assert first_child.recipe.producer == Producer.Constructor
    assert first_child.recipe.inputs[0].type == ResourceType.IronIngot
    assert first_child.recipe.output.type == ResourceType.IronRod
    assert first_child.utilisation == 1

    second_child = first_child.prior[0]

    assert second_child.recipe.producer == Producer.Smelter
    assert second_child.recipe.inputs[0].type == ResourceType.IronOre
    assert second_child.recipe.output.type == ResourceType.IronIngot
    assert second_child.utilisation == 0.5
    assert len(second_child.prior) == 0

def test_route_that_fans_out():
    plan = PlanTargetAmount(
        ResourceType.IronIngot,
        Resource(ResourceType.ReinforcedIronPlate, 5)
    )

    route_node = factory.compute_route(plan)

    assert len(route_node.prior) == 1

    assembler = route_node.prior[0]
    assert len(assembler.prior) == 4

    assert assembler.recipe.producer == Producer.Assembler
    assert assembler.recipe.inputs[0].type == ResourceType.IronPlate
    assert assembler.recipe.inputs[1].type == ResourceType.Screws
    assert assembler.recipe.output.type == ResourceType.ReinforcedIronPlate

    plate_constructor_1 = assembler.prior[0]

    assert plate_constructor_1.recipe.producer == Producer.Constructor
    assert plate_constructor_1.recipe.inputs[0].type == ResourceType.IronIngot
    assert plate_constructor_1.recipe.output.type == ResourceType.IronPlate
    assert plate_constructor_1.utilisation == 1
    assert len(plate_constructor_1.prior) == 0

    plate_constructor_2 = assembler.prior[1]

    assert plate_constructor_2.recipe.producer == Producer.Constructor
    assert plate_constructor_2.recipe.inputs[0].type == ResourceType.IronIngot
    assert plate_constructor_2.recipe.output.type == ResourceType.IronPlate
    assert plate_constructor_2.utilisation == 0.5
    assert len(plate_constructor_2.prior) == 0

    screw_constructor_1 = assembler.prior[2]

    assert screw_constructor_1.recipe.producer == Producer.Constructor
    assert screw_constructor_1.recipe.inputs[0].type == ResourceType.IronRod
    assert screw_constructor_1.recipe.output.type == ResourceType.Screws
    assert screw_constructor_1.utilisation == 1
    assert len(screw_constructor_1.prior) == 1

    screw_constructor_2 = assembler.prior[3]

    assert screw_constructor_2.recipe.producer == Producer.Constructor
    assert screw_constructor_2.recipe.inputs[0].type == ResourceType.IronRod
    assert screw_constructor_2.recipe.output.type == ResourceType.Screws
    assert screw_constructor_2.utilisation == 0.5
    assert len(screw_constructor_2.prior) == 1

    rod_constructor_1 = screw_constructor_1.prior[0]

    assert rod_constructor_1.recipe.producer == Producer.Constructor
    assert rod_constructor_1.recipe.inputs[0].type == ResourceType.IronIngot
    assert rod_constructor_1.recipe.output.type == ResourceType.IronRod
    assert math.isclose(rod_constructor_1.utilisation, 2/3)
    assert len(rod_constructor_1.prior) == 0

    rod_constructor_2 = screw_constructor_1.prior[0]

    assert rod_constructor_2.recipe.producer == Producer.Constructor
    assert rod_constructor_2.recipe.inputs[0].type == ResourceType.IronIngot
    assert rod_constructor_2.recipe.output.type == ResourceType.IronRod
    assert math.isclose(rod_constructor_2.utilisation, 2/3)
    assert len(rod_constructor_2.prior) == 0

def test_picks_most_efficient_when_there_are_multiple_options():
    plan = PlanTargetAmount(
        ResourceType.IronIngot,
        Resource(ResourceType.IronPlate, 1)
    )

    efficient_recipe = Recipe(Producer.Constructor, [Resource(ResourceType.IronIngot, 1)], Resource(ResourceType.IronPlate, 2), 1)
    inefficient_recipe = Recipe(Producer.Constructor, [Resource(ResourceType.IronIngot, 1)], Resource(ResourceType.IronPlate, 1), 1)

    factory_with_options = Factory([efficient_recipe, inefficient_recipe])

    route_node = factory_with_options.compute_route(plan)

    assert len(route_node.prior) == 1

    constructor = route_node.prior[0]

    assert len(constructor.prior) == 0
    assert constructor.recipe.output.amount == 1