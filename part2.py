# The same letter could appear multiple times in the mapping with different codewords.
# The letters might not appear in alphabetical order in the mapping.
# Other symbols like punctuation or whitespace could also have entries in the mapping.
# Finally shorter codewords could "hide" inside longer codewords (such as having both codewords "321" and "53214") to confuse frequency analysis.
# None of these additional countermeasures will be employed for these puzzles (at least intentionally, all keys have been generated randomly).

import string
import copy
import logging
from collections import deque
from itertools import chain

from tabulate import tabulate 

from src.crypto import decrypt
from src.utils import dict_shift_values, printTable, dict_shift_keys, dict_swap_keys_and_values, list_shift_column, list_2_dict, find_in_list_of_list, list_duplicates

logger = logging.getLogger(__file__)
logger.setLevel('DEBUG')
filehandler_dbg = logging.FileHandler(logger.name + "-debug.log", mode='w')
filehandler_dbg.setLevel('DEBUG')
logger.addHandler(filehandler_dbg)

alphabet = list(string.ascii_uppercase)
text = open("input/part2.txt", "r").read().strip()

def codewords(encrypted):
    start = 0
    key = [[letter, ''] for letter in alphabet]
    while any(char.isdigit() for char in encrypted) and start <= len(encrypted):
        length = int(encrypted[start])
        code = encrypted[start:start + length]

        print(start, start+length)

        found = find_in_list_of_list(key, code)
        if type(found) == int:
            found = find_in_list_of_list(key, '')

        i = found[0]

        if key[i][1] != '' and key[i][1] != code:
            print(f"tried to place {key[i][1]} but {code} was there")
        key[i][1] = code
        letter = key[i][0]

        print(code)
        logger.debug(encrypted)
        logger.debug(f"[{letter} {code}] shift codewords by {code[-1]}")
        logger.debug(tabulate(key, headers=["Letter", "Codeword"]))

        start += length
        # encrypted = encrypted.replace(code, letter, 1)
        list_shift_column(key, 1, int(code[-1]))

    return key

# flatten the result and convert 2 dict
key = list(chain.from_iterable(codewords(copy.deepcopy(text))))

keydict = list_2_dict(key)

# print(f"Here are the duplicate codewords: {list_duplicates(list(keydict.values()))}")

codewordmap = dict_swap_keys_and_values(keydict)

logger.debug(text)
logger.debug(codewordmap)
# print(substitutioncipher)

# # # # Try shifting the keys (letters) in the dict times
for i in range(0, len(alphabet)):
    codewordmap = dict_shift_values(codewordmap, 1)
    print(decrypt(text, codewordmap))

# freq = {letter: 0 for letter in alphabet}

# start = 0
# data = []
# textcopy = copy.deepcopy(text)
# while any(char.isdigit() for char in textcopy) and start < len(textcopy):  
#     length = int(textcopy[start])
#     code = textcopy[start:start + length]
#     letter = codewordmap[code]

#     data.append({
#         "letter": letter,
#         "start": start,
#         "end": start + length
#     })

#     start += length
#     codewordmap = dict_shift_keys(codewordmap, int(code[-1]))

# # logger.debug(tabulate(list(zip(freq.keys(), freq.values())), headers=["Letter", "Frequency"]))
# logger.debug(data)
# # print(codewordmap)
# # logger.debug(text)

# # print(data)

# print("".join([item["letter"] for item in data]))

# for letter, positions in data.items():
#     for pos in positions:
#         start = pos["start"]
#         end = pos["end"]
#         # print(pos["start"])
#         # print(pos["end"])
#         # print(text[start:end])
#         text = text.replace(text[start:end], letter, 1)
#         # text = text[:start] + letter + text[end:]
#         # text[start:end] = letter

# print(text)