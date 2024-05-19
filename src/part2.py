# The same letter could appear multiple times in the mapping with different codewords.
# The letters might not appear in alphabetical order in the mapping.
# Other symbols like punctuation or whitespace could also have entries in the mapping.
# Finally shorter codewords could "hide" inside longer codewords (such as having both codewords "321" and "53214") to confuse frequency analysis.
# None of these additional countermeasures will be employed for these puzzles (at least intentionally, all keys have been generated randomly).

import string
from pathlib import Path
import logging
from timeit import default_timer as timer

import helper.utils as utils

logger = logging.getLogger(Path(__file__).stem)
logger.setLevel('DEBUG')
filehandler_dbg = logging.FileHandler(logger.name + "-debug.log", mode='w')
filehandler_dbg.setLevel('DEBUG')
logger.addHandler(filehandler_dbg)

alphabet = list(string.ascii_uppercase)
filename = "input/part1.txt"
ciphertext = open(filename, "r").read().strip()

def getCodewords(encrypted):
    start = 0
    codewords = set()
    while start < len(encrypted):
        length = int(encrypted[start])
        code = encrypted[start:start + length]
        codewords.add(code)
        start += length
    return list(codewords)

start = timer()
key_mapping = utils.dict_swap_keys_and_values(dict(zip(alphabet, getCodewords(ciphertext))))
print(f"It took {(timer()-start)*1000:.2f}ms to get codewords.")
print(key_mapping)