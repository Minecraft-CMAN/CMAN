import re

import requests

from .. import configs


class GameVersion:
    def __init__(self) -> None:
        pass

    @staticmethod
    def load(string: str):
        pass

    def __str__(self):
        pass


class SnapShotVersion:
    def __init__(self, year: str, number: int) -> None:
        self.year: str = year
        self.number: int = number

    @staticmethod
    def load(string: str):
        if re.match(r"[0-9][0-9]w[0-9][0-9]a", string) is not None:
            year = "20" + string[0:2]  # [23]w16a
            number = int(string[3:5])  # 23w[16]a

            return SnapShotVersion(year=year, number=number)
        else:
            return None

    def __str__(self) -> str:
        return f"{self.year[2:4]}w{self.number.__str__().zfill(2)}a"


class ReleaseVersion:
    def __init__(
        self, main_version: int, sub_version: int, subsub_version: int
    ) -> None:
        self.main_version = main_version
        self.sub_version = sub_version

        self.subsub_version = subsub_version

    @staticmethod
    def load(string: str):
        if (
            re.match(r"[0-2].[0-9][0-9].[0-9]", string) is not None
            or re.match(r"[0-2].[0-9].[0-9]", string) is not None
        ):
            main = string.split(".")[0]
            sub_version = string.split(".")[1]

            try:
                subsub_version = string.split(".")[2]
            except IndexError:
                subsub_version = 0

            return ReleaseVersion(
                main_version=int(main),
                sub_version=int(sub_version),
                subsub_version=int(subsub_version),
            )
        else:
            return None

    def __str__(self) -> str:
        return f"{self.main_version}.{self.sub_version}.{self.subsub_version}"


class GameList:
    def __init__(self) -> None:
        self.raw = requests.get(
            configs.LAUNCHER_META + "/mc/game/version_manifest_v2.json"
        ).json()
        self.version_list: list[ReleaseVersion | SnapShotVersion] = []

        for version in self.raw["versions"]:
            if version["type"] == "snapshot":
                instance = SnapShotVersion.load(version["id"])
            else:
                instance = ReleaseVersion.load(version["id"])

            if instance is not None:
                self.version_list.append(instance)


class Game:
    def __init__(self, version: GameVersion) -> None:
        self.version = version
