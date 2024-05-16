# The same letter could appear multiple times in the mapping with different codewords.
# The letters might not appear in alphabetical order in the mapping.
# Other symbols like punctuation or whitespace could also have entries in the mapping.
# Finally shorter codewords could "hide" inside longer codewords (such as having both codewords "321" and "53214") to confuse frequency analysis.
# None of these additional countermeasures will be employed for these puzzles (at least intentionally, all keys have been generated randomly).

import re
import string
import copy
import logging
from collections import deque
from itertools import chain

from tabulate import tabulate 

from src.crypto import decrypt
from src.utils import dict_shift_values, dict_swap_keys_and_values, list_shift_column, list_2_dict, find_in_list_of_list, list_duplicates

logger = logging.getLogger(__file__)
logger.setLevel('DEBUG')
filehandler_dbg = logging.FileHandler(logger.name + "-debug.log", mode='w')
filehandler_dbg.setLevel('DEBUG')
logger.addHandler(filehandler_dbg)

alphabet = list(string.ascii_uppercase)
text = open("input/part2.txt", "r").read()

def crack(encrypted):
    key = [[letter, ''] for letter in alphabet]
    hasempty = True
    while any(char.isdigit() for char in encrypted) and hasempty:
        result = re.search("\d+", encrypted)
        start = result.start()
        length = int(encrypted[start])
        code = encrypted[start:start + length]

        i = -1
        found = find_in_list_of_list(key, code)
        if type(found) == int:
            # find some index that is empty
            found = find_in_list_of_list(key, '')
            if type(found) == int:
                hasempty = False
                break

        i = found[0]

        key[i][1] = code
        letter = key[i][0]

        logger.debug(f"letter: {letter}")
        logger.debug(encrypted)
        logger.debug(f"[{code}] shift codewords by {code[-1]}")
        logger.debug(tabulate(key, headers=["Letter", "Codeword"]))

        encrypted = encrypted.replace(code, letter, 1)
        list_shift_column(key, 1, int(code[-1]))

    return key

# flatten the result and convert 2 dict
key = list(chain.from_iterable(crack(copy.deepcopy(text))))

# print(len(key))
# start = len(key)
keydict = list_2_dict(key)

print(f"Here are the duplicate codewords: {list_duplicates(list(keydict.values()))}")

key = dict_swap_keys_and_values(keydict)


# print(key)
print(len(key))

# # Try shifting the keys (letters) in the dict times
for i in range(0, len(alphabet)):
    dict_shift_values(key, 1)
    print(decrypt(text, key))