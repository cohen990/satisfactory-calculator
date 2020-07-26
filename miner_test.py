import miner
from base import Deposits


def test_iron_ore_on_normal_gives_120():
    blueprint = miner.calc(Deposits("iron ore", "normal", 1))
    assert blueprint.building == "mk2 miner"
    assert blueprint.number == 1
    assert blueprint.resource_out.name == "iron ore"
    assert blueprint.resource_out.amount_per_minute == 120


def test_2_iron_ore_on_normal_gives_240():
    blueprint = miner.calc(Deposits("iron ore", "normal", 2))
    assert blueprint.building == "mk2 miner"
    assert blueprint.number == 2
    assert blueprint.resource_out.name == "iron ore"
    assert blueprint.resource_out.amount_per_minute == 240


def test_1_iron_ore_on_impure_gives_60():
    blueprint = miner.calc(Deposits("iron ore", "impure", 1))
    assert blueprint.building == "mk2 miner"
    assert blueprint.number == 1
    assert blueprint.resource_out.name == "iron ore"
    assert blueprint.resource_out.amount_per_minute == 60


def test_1_iron_ore_on_pure_gives_240():
    blueprint = miner.calc(Deposits("iron ore", "pure", 1))
    assert blueprint.building == "mk2 miner"
    assert blueprint.number == 1
    assert blueprint.resource_out.name == "iron ore"
    assert blueprint.resource_out.amount_per_minute == 240
