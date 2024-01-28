import logging

fmttxt = logging.Formatter(
    "[%(asctime)s %(name)s]: %(message)s", "%d %b %Y %H:%M:%S"
)


fileHandler = logging.FileHandler("data/logs.txt", mode='a')
fileHandler.setFormatter(fmttxt)


def get_logger(file: str):
    logger = logging.getLogger(file)
    logger.addHandler(fileHandler)
    logger.setLevel(logging.INFO)
    return logger
