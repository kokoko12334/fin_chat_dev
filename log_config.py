from loguru import logger
import sys
import logging

from settings import settings

class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        # Get corresponding Loguru level if it exists.
        level: str | int
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message.
        frame, depth = logging.currentframe(), 0
        while frame and (depth == 0 or frame.f_code.co_filename == logging.__file__):
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())

# loguru log to gunicorn logger
# https://github.com/Delgan/loguru/issues/172
class PropagateHandler(logging.Handler):
    def emit(self, record):
        logging.getLogger("gunicorn").handle(record)
        


logger.trace("TRACE")
logger.debug("DEBUG")
logger.info("INFO")
logger.success("SUCCESS")
logger.warning("WARNING")
logger.error("ERROR")
logger.critical("CRITICAL")

# logger.remove() 

# test -sys stderr
if settings.ENVIRONMENT == "test":
    logger.add(PropagateHandler(), format="{time} {level} {message}", level="DEBUG")
    # logging.getLogger().handlers = [PropagateHandler()]
# dev - sys stderr
if settings.ENVIRONMENT == "dev":
    logger.add(sys.stderr, format="{time} {level} {message}", level="DEBUG")
# prod - file log
if settings.ENVIRONMENT == "prod":
    logger.add("logs/{time:YYYY-MM-DD}_log.log", format="{time} {level} {message}", level="INFO", rotation="500 MB")

logger.info(logging.getLogger().name)

logger.warning("This is a warning")
logger.warning("WARNING")