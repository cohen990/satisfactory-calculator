from base import Blueprint, Resource


def calc(resource):
    if resource.name == "screw":
        resource_in = Resource("pipe", 60)
        resource_out = Resource("screw", 240)
        return Blueprint("constructor", 6, resource_in, resource_out)
    resource_in = Resource("iron ingot", 60)
    resource_out = Resource("iron pipe", 60)
    return Blueprint("constructor", 4, resource_in, resource_out)
