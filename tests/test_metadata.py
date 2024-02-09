import tests
import metadata
import shutil
import pathlib


def test_download_metadata():
    shutil.rmtree(pathlib.Path(
        './runtime/official-mirror').absolute().as_posix(), ignore_errors=True)

    md = metadata.Metadata.load_from_dict({
        'repo': {
            'url': 'https://github.com/Minecraft-CMAN/CMAN-official-mirror.git',
            'path': 'runtime/official-mirror'
        }
    })

    assert len(md.mods) > 0

    metadata.Metadata.load_from_dict({
        'repo': {
            'url': 'https://github.com/Minecraft-CMAN/CMAN-official-mirror.git',
            'path': 'runtime/official-mirror'
        }
    })
