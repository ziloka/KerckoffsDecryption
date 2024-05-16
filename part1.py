# from src.crypto import decrypt
import re
import logging
import string
from tabulate import tabulate
import numpy as np
from src.utils import list_2_dict, dict_swap_keys_and_values, dict_shift_keys

logger = logging.getLogger(__file__)
logger.setLevel('DEBUG')
filehandler_dbg  = logging.FileHandler(logger.name + "-debug.log", mode='w')
filehandler_dbg.setLevel('DEBUG')
logger.addHandler(filehandler_dbg)

encrypted = open("input/part1.txt", "r").read()
codewords = open("input/codewords.txt", "r").read().splitlines()

def decrypt(text: str, codewordmap: dict[str, str]):
    while any(char.isdigit() for char in text):
        result = re.search("\d+", text)
        start = result.start()
        length = int(text[start])
        code = text[start:start + length]
        letter = codewordmap[code]

        logger.debug(encrypted)
        logger.debug(f"[{letter} {code}] shift codewords by {code[-1]}")
        logger.debug(tabulate(list(zip(list(string.ascii_uppercase), codewordmap.keys())), headers=["Letter", "Codeword"]))

        text = text.replace(code, codewordmap[code], 1)
        codewordmap = dict_shift_keys(codewordmap, int(code[-1]))
    return text

print(decrypt(encrypted, dict_swap_keys_and_values(list_2_dict(codewords))))
