from rich import print
from utils import logging, console
from configs import config
from metadata import Metadata

logger = logging.getLogger(__name__)

if '__main__' == __name__:
    logger.info("===== CMAN started =====")

    metadatas = config.__getitem__('metadatas', [
        {
            'repo': {
                'url': 'https://github.com/Minecraft-CMAN/CMAN-official-mirror.git',
                'path': './runtime/official-mirror'
            }
        }
    ])
    metadatas = [
        Metadata.load_from_dict(metadata)
        for metadata in metadatas
    ]
