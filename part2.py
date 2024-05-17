# The same letter could appear multiple times in the mapping with different codewords.
# The letters might not appear in alphabetical order in the mapping.
# Other symbols like punctuation or whitespace could also have entries in the mapping.
# Finally shorter codewords could "hide" inside longer codewords (such as having both codewords "321" and "53214") to confuse frequency analysis.
# None of these additional countermeasures will be employed for these puzzles (at least intentionally, all keys have been generated randomly).

import string
import copy
import logging
from collections import deque, Counter
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
filename = "input/part1.txt"
text = open(filename, "r").read().strip()

def logFrequencyData(codewordmap):
    freq = {letter: 0 for letter in alphabet}
    start = 0
    data = []
    while any(char.isdigit() for char in text) and start < len(text):  
        length = int(text[start])
        code = text[start:start + length]
        letter = codewordmap[code]
        freq[letter]+=1

        data.append({
            "letter": letter,
            "start": start,
            "end": start + length
        })

        start += length
        codewordmap = dict_shift_keys(codewordmap, int(code[-1]))

    logger.debug(tabulate(list(zip(freq.keys(), freq.values())), headers=["Letter", "Frequency"]))
    logger.debug(f"There are {sum(freq.values())} characters")
    logger.debug(data)
    # print(codewordmap)
    logger.debug(text)

def codewords(encrypted):
    start = 0
    key = [[letter, ''] for letter in alphabet]
    while any(char.isdigit() for char in encrypted) and start < len(encrypted):
        length = int(encrypted[start])
        code = encrypted[start:start + length]

        # print(start, start+length)

        found = find_in_list_of_list(key, code)
        if type(found) == int and found == -1:
            found = find_in_list_of_list(key, '')
        i = found[0]

        key[i][1] = code
        letter = key[i][0]

        # print(code)
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

print(f"Here are the duplicate codewords: {list_duplicates(list(keydict.values()))}")

codewordmap = dict_swap_keys_and_values(keydict)

logger.debug(text)
logger.debug('Warning! codewordmap values are incorrect position and order')
logger.debug(codewordmap)
logger.debug('Codewords might be wrong double check to make sure')
logger.debug(list(codewordmap.keys()))
# print(codewordmap)
# print(substitutioncipher)

# # # # Try shifting the keys (letters) in the dict times
# logger.debug('--------- Rotating code"wordmap ------------')

# for i in range(0, len(alphabet)):
#     codewordmap = dict_shift_keys(codewordmap, 1)
#     logger.debug(codewordmap)
#     print(decrypt(text, codewordmap))

logFrequencyData(codewordmap)

if "part1" in filename:
    logger.debug("-- part 1 crack specific info --")
    same =Counter(list(codewordmap.keys())) == Counter(['4502', '53177', '946320122', '85053600', '7171031', '87445918', '4504', '692473', '20', '638440', '57643', '7004062', '52381', '930424404', '84524991', '89411894', '4254', '376', '88527391', '23', '29', '361', '923921735', '4468', '636187', '971559793'])
    if same:
        logger.debug("codewordmaps are the same")
    else:
        logger.debug("codewordmaps are different")
