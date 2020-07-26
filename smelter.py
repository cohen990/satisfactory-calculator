from base import Blueprint, Resource


def calc(resource):
    resource_in = Resource("iron ore", 60)
    resource_out = Resource("iron ingot", 60)
    return Blueprint("smelter", 2, resource_in, resource_out)
