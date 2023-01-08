from enum import Enum
import logging
import verboselogs
import sys
import random
import time

random.seed(1)

class Axis(Enum):
    LENGTH = 0
    WIDTH = 1
    HEIGHT = 2

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name

class SearchMethod(Enum):
    NONE = 0
    BRUTE = 1
    GREEDY = 2
    CANDIDATE_POINTS = 3
    SUB_SPACE = 4

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name

PRECISION = 0 # =10^x

LOG_FILE_PATH = r"D:\OneDrive\Projects\Coding\Python\Fun\3D_Bin_Packing\Logs\run_log_" + \
                time.asctime().replace(" ","_").replace(":","_") + r".log"

def get_logger():
    logger = verboselogs.VerboseLogger("3DBP")
    logger.setLevel(logging.DEBUG)

    streamFormatter = logging.Formatter(fmt="({filename}:{lineno}) {levelname}: {message}",style="{")
    fileFormatter = logging.Formatter(fmt='[{asctime}] File "{filename}", line {lineno}, in {funcName}\n{levelname}: {message}',style="{")

    streamHandler = logging.StreamHandler(sys.stdout)
    streamHandler.setLevel(logging.INFO)
    streamHandler.setFormatter(streamFormatter)

    fileHandler = logging.FileHandler(LOG_FILE_PATH, "w")
    fileHandler.setLevel(logging.VERBOSE)
    fileHandler.setFormatter(fileFormatter)

    logger.addHandler(streamHandler)
    logger.addHandler(fileHandler)

    return logger

logger = get_logger()
