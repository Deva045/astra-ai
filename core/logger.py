from loguru import logger
import sys

logger.remove()

logger.add(
    sys.stdout,
    colorize=True,
    format="<cyan>{time:HH:mm:ss}</cyan> | <level>{message}</level>",
)

logger.add(
    "logs/nexus.log",
    rotation="10 MB",
    retention="30 days",
    compression="zip",
)

app_logger = logger