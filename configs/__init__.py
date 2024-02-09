import logging
import orjson
import pathlib
import os
import dotenv
from typing import Any
dotenv.load_dotenv()

LOG_LEVEL = logging.DEBUG


class Config(dict):
    def __init__(self) -> None:
        self.file = pathlib.Path('./runtime/configs/config.json')

        if not self.file.parent.exists():
            self.file.parent.mkdir(parents=True, exist_ok=True)

        if not self.file.exists():
            self.file.touch()
            self.file.write_text('{}')

    def __getitem__(self, key: str, default: Any) -> Any:
        data: dict = orjson.loads(self.file.read_bytes())

        if key not in data.keys():
            self.__setitem__(key, default)
            return default

        return data[key]

    def __setitem__(self, __key: str, __value: Any) -> None:
        data = orjson.loads(self.file.read_bytes())
        data[__key] = __value
        self.file.write_bytes(orjson.dumps(
            data, option=orjson.OPT_SORT_KEYS | orjson.OPT_INDENT_2))


config = Config()
