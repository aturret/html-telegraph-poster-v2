from loguru import logger

logger.add("logs/info.log", level="INFO", rotation="10 MB")
