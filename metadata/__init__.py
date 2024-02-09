from __future__ import annotations
import pickle
import pathlib
from git import Repo as GitRepo
from rich.progress import track
from modules.mod import Mod
from utils import logging, console
from typing import *

logger = logging.getLogger(__name__)


class Repo(object):
    def __init__(self, url: str, path: pathlib.Path) -> None:
        self.url = url
        self.path = path
        self.repo: Union[GitRepo, None] = None

        if not self.path.exists():
            logger.warning(
                f'The repo {self.url} is not exists, downloading...')
            self.path.mkdir(parents=True, exist_ok=True)

            with console.status(f'Downloading repo {self.url}...', spinner='dots8'):
                self.repo = GitRepo.clone_from(self.url, self.path)
        else:
            self.repo = GitRepo(self.path)

            with console.status(f'Updating repo {self.url}', spinner='dots8'):
                self.repo.remote().pull()

    @staticmethod
    def load_from_dict(data: dict) -> Repo:
        return Repo(data['url'], pathlib.Path(data['path']))


class Metadata(object):
    def __init__(self, repo: Repo) -> None:
        self.repo = repo
        self.mods: List[Mod] = []

        self.load_mods()

    def load_mods(self):
        logger.info(f'Loading metadata from repo {self.repo.url}')

        for file in track(self.repo.path.glob('*.mod'), description=f'Loading metadata from repo {self.repo.url}', total=len(list(self.repo.path.glob('*.mod')))):
            mod = pickle.loads(file.read_bytes())

            if not isinstance(mod, Mod):
                logger.warn(f'Invalid mod file: {file}')
                continue

            self.mods.append(mod)

    @staticmethod
    def load_from_dict(data: dict) -> Metadata:
        return Metadata(Repo.load_from_dict(data['repo']))
