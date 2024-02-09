import datetime
import aiohttp
import asyncio
from typing import List, Literal, Optional
from utils import logging

logger = logging.getLogger(__name__)


class VersionFileHashes(object):
    def __init__(
        self,
        sha512: str,
        sha1: str,
        *args,
        **kwargs
    ) -> None:
        self.sha512 = sha512
        self.sha1 = sha1
        self.args = args
        self.kwargs = kwargs


class VersionFile(object):
    def __init__(
        self,
        hashes: VersionFileHashes,
        url: str,
        filename: str,
        primary: bool,
        size: int,
        file_type: Optional[Literal["required-resource-pack",
                                    "optional-resource-pack"]],
        *args,
        **kwargs
    ) -> None:
        self.hashes = hashes
        self.url = url
        self.filename = filename
        self.primary = primary
        self.size = size
        self.file_type = file_type
        self.args = args
        self.kwargs = kwargs


class VersionDependency(object):
    def __init__(
        self,
        dependency_type: Literal["required", "optional", "incompatible", "embedded"],
        version_id: Optional[str] = None,
        project_id: Optional[str] = None,
        file_name: Optional[str] = None,
        *args,
        **kwargs
    ) -> None:
        self.dependency_type = dependency_type
        self.version_id = version_id
        self.project_id = project_id
        self.file_name = file_name
        self.args = args
        self.kwargs = kwargs


class Version(object):
    def __init__(
        self,
        name: str,
        version_number: str,
        game_versions: List[str],
        version_type: Literal['release', 'beta', 'alpha'],
        loaders: List[Literal['fabric', 'forge']],
        featured: bool,
        id: str,
        project_id: str,
        author_id: str,
        date_published: str,
        downloads: int,
        files: List[VersionFile],
        changelog: Optional[str] = None,
        dependencies: Optional[List[VersionDependency]] = None,
        status: Optional[Literal["listed", "archived",
                                 "draft", "unlisted", "scheduled", "unknown"]] = None,
        requested_status: Optional[Literal['listed',
                                           'archived', 'draft', 'unlisted']] = None,
        *args,
        **kwargs
    ) -> None:
        self.name = name
        self.version_number = version_number
        self.game_versions = game_versions
        self.version_type = version_type
        self.loaders = loaders
        self.featured = featured
        self.id = id
        self.project_id = project_id
        self.author_id = author_id
        self.date_published = date_published
        self.downloads = downloads
        self.files = files
        self.changelog = changelog
        self.dependencies = dependencies
        self.status = status
        self.requested_status = requested_status
        self.args = args
        self.kwargs = kwargs


class Mod(object):
    def __init__(
        self,
        slug: str,
        title: str,
        description: str,
        categories: List[str],
        client_side: Literal['required', 'optional', 'unsupported'],
        server_side: Literal['required', 'optional', 'unsupported'],
        project_type: Literal['mod', 'modpack', 'resourcepack', 'shader'],
        downloads: int,
        project_id: str,
        author: str,
        versions: List[str],
        follows: int,
        date_created: str,
        date_modified: str,
        license: str,
        gallery: Optional[List[str]] = None,
        featured_gallery: Optional[List[str]] = None,
        latest_version: Optional[str] = None,
        display_categories: Optional[str] = None,
        thread_id: Optional[str] = None,
        monetization_status: Optional[Literal['monetized',
                                              'demonetized', 'force-demonetized']] = None,
        icon_url: Optional[str] = None,
        color: Optional[str] = None,
        *args,
        **kwargs
    ) -> None:
        self.slug: str = slug
        self.title: str = title
        self.description: str = description
        self.categories: List[str] = categories
        self.client_side: Literal['required',
                                  'optional', 'unsupported'] = client_side
        self.server_side: Literal['required',
                                  'optional', 'unsupported'] = server_side
        self.project_type: Literal['mod', 'modpack',
                                   'resourcepack', 'shader'] = project_type
        self.downloads: int = downloads
        self.project_id: str = project_id
        self.author: str = author
        self.versions: List[str] = versions
        self.follows: int = follows
        self.date_created: str = datetime.datetime.fromisoformat(
            date_created.replace('Z', ''))
        self.date_modified: str = datetime.datetime.fromisoformat(
            date_modified.replace('Z', ''))
        self.license: str = license
        self.gallery: Optional[List[str]] = gallery
        self.featured_gallery: Optional[List[str]] = featured_gallery
        self.latest_version: Optional[str] = latest_version
        self.display_categories: Optional[List[str]] = display_categories
        self.thread_id: Optional[str] = thread_id
        self.monetization_status: Optional[Literal['monetized',
                                                   'demonetized', 'force-demonetized']] = monetization_status
        self.icon_url: Optional[str] = icon_url
        self.color: Optional[str] = color

        self.args = args
        self.kwargs = kwargs

        self._project_versions: List[Version] = []

    async def fetch_project_versions(self):
        session = aiohttp.ClientSession(base_url='https://api.modrinth.com/')
        project_version_resp = await session.get(f'/v2/project/{self.project_id}/version')

        if project_version_resp.status != 200:
            logger.error(
                f'Failed to fetch project versions for {self.project_id}')
            return -1

        # Parse
        data = (await project_version_resp.json())

        for idx, item in enumerate(data):
            data[idx]['dependencies'] = [VersionDependency(
                **dependency) for dependency in data[idx]['dependencies']]

            for index, file in enumerate(data[idx]['files']):
                data[idx]['files'][index]['hashes'] = VersionFileHashes(
                    **file['hashes'])
                data[idx]['files'][index] = VersionFile(**file)

        self._project_versions = [Version(**version) for version in data]

    def project_versions(self) -> List[Version]:
        if self._project_versions == []:
            logging.warning(
                'PLEASE Execute Mod.fetch_project_versions() before access project_versions')

        return self._project_versions
