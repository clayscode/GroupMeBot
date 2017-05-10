import logging


def setupLogger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        'Line %(lineno)d,%(filename)s- %(asctime)s- %(levelname)s- %(message)s'
    )
    ch.setFormatter(formatter)
    logger.addHandler(ch)
