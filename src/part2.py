import copy
import string
import logging
from pathlib import Path
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
codeword2letter = utils.dict_swap_keys_and_values(dict(zip(alphabet, getCodewords(ciphertext))))
print(f"It took {(timer()-start)*1000:.2f}ms to get codewords.")

def decrypt_wo_key(encrypted, codeword2letter):
    codeword2letter = copy.deepcopy(codeword2letter)
    plaintext = ""
    start = 0
    while start < len(encrypted):
        length = int(encrypted[start])
        code = encrypted[start:start + length]
        # TODO: step stating it is unrealistic that "x" is next to "z"
        # Use hill climbing to find the best key
        plaintext += codeword2letter[code]
        codeword2letter = utils.dict_shift_keys(codeword2letter, int(code[-1]))
        start += length
    return plaintext

# idea: use bruteforce and frequency analysis to find key quickly
