import sys
import logging
from colorlog import StreamHandler, ColoredFormatter


fmtout = ColoredFormatter(
    "%(white)s%(asctime)s | %(name)s | %(log_color)s%(levelname)s | %(log_color)s%(message)s %(blue)s(%(filename)s:%(lineno)d)"
)

fmttxt = logging.Formatter(
    "%(asctime)s | %(name)s | %(levelname)s | %(message)s (%(filename)s:%(lineno)d)"
)

# Screen log
stdout = StreamHandler(stream=sys.stdout)
stdout.setFormatter(fmtout)

# Log file
fileHandler = logging.FileHandler("logs.txt")
fileHandler.setFormatter(fmttxt)


def get_logger(file: str):
    logger = logging.getLogger(file)
    logger.addHandler(stdout)
    logger.addHandler(fileHandler)
    logger.setLevel(logging.DEBUG)
    return logger
