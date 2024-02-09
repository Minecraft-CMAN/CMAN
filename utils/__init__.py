import logging
import configs
import datetime
from rich.logging import RichHandler
from rich.console import Console

filehandler = logging.FileHandler(f'runtime/logs/{datetime.datetime.now().strftime("%Y-%m-%d")}.log')
console = Console()

filehandler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

logging.basicConfig(
    level=configs.LOG_LEVEL,
    format="%(message)s",
    handlers=[RichHandler(), filehandler]
)