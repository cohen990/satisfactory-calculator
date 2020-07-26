from base import Recipe, Resource


def calc(resource):
    screw_recipe = Recipe(Resource("iron pipe", 10), Resource("screw", 40))
    iron_pipe_recipe = Recipe(
        Resource("iron ingot", 15), Resource("iron pipe", 15))
    iron_ingot_recipe = Recipe(
        Resource("iron ore", 30), Resource("iron ingot", 30))
    return [iron_ingot_recipe, iron_pipe_recipe, screw_recipe]
