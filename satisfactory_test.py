import satisfactory


def test_making_screws_with_1_impure_iron_deposit():
    result = satisfactory.calc("screw", 1, "iron ore", "impure")
    split = result.split("\n")
    assert split[0] == "mk2 miner, 1, iron ore, 60"
    assert split[1] == "smelter, 2, iron ingot, 60"
    assert split[2] == "constructor, 4, iron pipe, 60"
    assert split[3] == "constructor, 6, screw, 240"
