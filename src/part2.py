# The same letter could appear multiple times in the mapping with different codewords.
# The letters might not appear in alphabetical order in the mapping.
# Other symbols like punctuation or whitespace could also have entries in the mapping.
# Finally shorter codewords could "hide" inside longer codewords (such as having both codewords "321" and "53214") to confuse frequency analysis.
# None of these additional countermeasures will be employed for these puzzles (at least intentionally, all keys have been generated randomly).

import string
import copy
from pathlib import Path
import logging
from collections import Counter
from itertools import chain

from tabulate import tabulate
# from scipy.stats import chisquare

import helper.utils as utils
__name__
logger = logging.getLogger(Path(__file__).stem)
logger.setLevel('DEBUG')
filehandler_dbg = logging.FileHandler(logger.name + "-debug.log", mode='w')
filehandler_dbg.setLevel('DEBUG')
logger.addHandler(filehandler_dbg)

alphabet = list(string.ascii_uppercase)
filename = "input/part1.txt"
text = open(filename, "r").read().strip()

def getFrequency(codewordmap):
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
        codewordmap = utils.dict_shift_keys(codewordmap, int(code[-1]))

    logger.debug('------ getFrequency ----------')
    logger.debug(tabulate(list(zip(freq.keys(), freq.values())), headers=["Letter", "Frequency"]))
    logger.debug(f"There are {sum(freq.values())} characters")
    logger.debug(data)
    logger.debug('-------------------------')
    # # print(codewordmap)
    # logger.debug(text)
    return freq

def codewords(encrypted):
    start = 0
    codewordmap = [[letter, ''] for letter in alphabet]
    freq = {letter: 0 for letter in alphabet}
    while any(char.isdigit() for char in encrypted) and start < len(encrypted):
        length = int(encrypted[start])
        code = encrypted[start:start + length]

        # print(start, start+length)

        found = utils.find_in_list_of_list(codewordmap, code)
        if type(found) == int and found == -1:
            found = utils.find_in_list_of_list(codewordmap, '')
        i = found[0]

        codewordmap[i][1] = code
        letter = codewordmap[i][0]
        freq[letter]+=1

        # print(code)
        # logger.debug('------ encrypted ------')
        logger.debug(encrypted)
        logger.debug(f"[{letter} {code} freq: {freq[letter]}] shift codewords by {code[-1]}")
        logger.debug(tabulate(codewordmap, headers=["Letter", "Codeword"]))

        start += length
        utils.list_shift_column(codewordmap, 1, int(code[-1]))

    logger.debug('------ frequencies ------')
    logger.debug(freq)
    logger.debug('-------------------------')

    return codewordmap

def decrypt(encrypted, codewordmap):
    codewordmap = copy.deepcopy(codewordmap)
    decrypted = ""
    start = 0
    while any(char.isdigit() for char in encrypted) and start < len(encrypted):
        length = int(encrypted[start])
        code = encrypted[start:start + length]
        letter = codewordmap[code]
        decrypted += letter
        utils.dict_shift_keys(codewordmap, int(code[-1]))
        start += length
    return decrypted

# flatten the result and convert 2 dict
key = list(chain.from_iterable(codewords(text)))

keydict = utils.list_2_dict(key)

print(f"Here are the duplicate codewords: {utils.list_duplicates(list(keydict.values()))}")

codewordmap = utils.dict_swap_keys_and_values(keydict)

logger.debug(text)
logger.debug('Warning! codewordmap values are incorrect position and order')
logger.debug(codewordmap)
logger.debug('Codewords might be wrong double check to make sure')
logger.debug(list(codewordmap.keys()))

if "part1" in filename:
    logger.debug("-- part 1 crack specific info --")
    same = Counter(list(codewordmap.keys())) == Counter(['4502', '53177', '946320122', '85053600', '7171031', '87445918', '4504', '692473', '20', '638440', '57643', '7004062', '52381', '930424404', '84524991', '89411894', '4254', '376', '88527391', '23', '29', '361', '923921735', '4468', '636187', '971559793'])
    if same:
        logger.debug("codewordmaps are the same")
    else:
        logger.debug("codewordmaps are different")

# should give you subsitution cipher
logger.debug(decrypt(text, codewordmap))

def modified_kasiski_examination():
    pass