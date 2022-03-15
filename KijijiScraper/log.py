import logging
import logging.handlers
from KijijiScraper.config import Config


LOG_FILE_NAME = Config.LOG_DIR / "adextract_logs"
LOGGER_NAME = "EXTRACT_LOG"

DB_ADDENTRY_LOG_FILENAME = Config.LOG_DIR / "db_addentry_log"
DB_ADDENTRY_LOGGER = "ADDENTRY_LOG"


def create_logger(logger_name=LOGGER_NAME, file_name=LOG_FILE_NAME):
    log = logging.getLogger(logger_name)
    log.setLevel(logging.DEBUG)
    rotating_fhandler = logging.handlers.RotatingFileHandler(
        filename=file_name, maxBytes=1024 * 1024, backupCount=5
    )
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s : %(message)s")
    rotating_fhandler.setFormatter(formatter)
    log.addHandler(rotating_fhandler)
    return log


LOGGER = create_logger()
LOG_DB_ADD_ENTRY = create_logger(
    logger_name=DB_ADDENTRY_LOGGER, file_name=DB_ADDENTRY_LOG_FILENAME
)
