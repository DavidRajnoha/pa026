from source.resources import Race


def test_race(race_basic):
    race: Race = Race(name="basic", id="1", categories={},
                      interval=2, concurrent_slots_limit=2)
    assert len(race.slots) == 4
