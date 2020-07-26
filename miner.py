from base import Blueprint, Resource

ore_availability = 60

purity_multiplier = {
    "pure": 4,
    "normal": 2,
    "impure": 1
}


def calc(deposits):
    available_ore = deposits.number_of_deposits * \
        ore_availability * purity_multiplier[deposits.quality]
    resource_in = Resource("Mining", 0)
    resource_out = Resource("iron ore", available_ore)
    return Blueprint("mk2 miner", deposits.number_of_deposits, resource_in, resource_out)
