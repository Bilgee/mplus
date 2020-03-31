import os
import logging
from logging.handlers import TimedRotatingFileHandler
from config import LOG, ENV

# ----------------------------------------------------------------------


def _getLogger(path, back_up_interval=1, back_up_count=7):
    """Rotated log creator
    """
    logging.basicConfig(
        format='%(asctime)s - %(message)s', datefmt='%m/%d/%Y %H:%M:%S',
        level=LOG['LEVEL'])
    logger = logging.getLogger(__name__)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %H:%M:%S')
    handler = TimedRotatingFileHandler(path,
                                       when="d",
                                       interval=back_up_interval,
                                       backupCount=back_up_count)
    handler.setLevel(LOG['LEVEL'])
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


logger = _getLogger(os.path.join(LOG['PATH'], LOG['NAME']))