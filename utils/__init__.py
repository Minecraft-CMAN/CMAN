import logging
import configs
import datetime
import pathlib
from rich.logging import RichHandler
from rich.console import Console

pathlib.Path('runtime/').mkdir(parents=True, exist_ok=True)
pathlib.Path('runtime/logs').mkdir(parents=True, exist_ok=True)
pathlib.Path('runtime/configs').mkdir(parents=True, exist_ok=True)

filehandler = logging.FileHandler(
    f'runtime/logs/{datetime.datetime.now().strftime("%Y-%m-%d")}.log')
console = Console()

filehandler.setFormatter(logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s'))

logging.basicConfig(
    level=configs.LOG_LEVEL,
    format="%(message)s",
    handlers=[RichHandler(), filehandler]
)
