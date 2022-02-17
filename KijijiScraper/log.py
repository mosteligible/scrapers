import logging
import logging.handlers


LOG_FILE_NAME = "adextract_logs"
LOGGER_NAME = "EXTRACT_LOG"


def create_logger(logger_name=LOGGER_NAME, file_name=LOG_FILE_NAME):
    log = logging.getLogger(logger_name)
    log.setLevel(logging.INFO)
    rotating_fhandler = logging.handlers.RotatingFileHandler(
        filename=file_name, maxBytes=1024*1024, backupCount=5
    )
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s : %(message)s")
    rotating_fhandler.setFormatter(formatter)
    log.addHandler(rotating_fhandler)
    return log


LOGGER = create_logger()
