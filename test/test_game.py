from .. import game


def test_snapshot_game():
    instance = game.SnapShotVersion.load("23w16a")

    assert instance is not None
    assert instance.year == "2023"
    assert instance.number == 16
    assert instance.__str__() == "23w16a"


def test_release_game():
    instance = game.ReleaseVersion.load("1.18.2")

    assert instance is not None
    assert instance.main_version == 1
    assert instance.sub_version == 18
    assert instance.subsub_version == 2
    assert instance.__str__() == "1.18.2"


def test_game_list():
    instance = game.GameList()

    assert (
        instance.version_list[0].__str__() == instance.raw["latest"]["snapshot"]
        or instance.version_list[0].__str__() == instance.raw["latest"]["release"]
    )
