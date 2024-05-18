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

from helper.crypto import decrypt
import helper.utils as utils
from helper.polysub import kasiski

logger = logging.getLogger(Path(__file__).stem)
logger.setLevel('DEBUG')
filehandler_dbg = logging.FileHandler(logger.name + "-debug.log", mode='w')
filehandler_dbg.setLevel('DEBUG')
logger.addHandler(filehandler_dbg)

alphabet = list(string.ascii_uppercase)
filename = "input/part1.txt"
ciphertext = open(filename, "r").read().strip()

def codewords(encrypted):
    start = 0
    codewordmap = [[letter, ''] for letter in alphabet]
    # freq = {letter: 0 for letter in alphabet}
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
        # freq[letter]+=1

        # print(code)
        # logger.debug('------ encrypted ------')
        # logger.debug(encrypted)
        # logger.debug(f"[{letter} {code} freq: {freq[letter]}] shift codewords by {code[-1]}")
        # logger.debug(tabulate(codewordmap, headers=["Letter", "Codeword"]))

        start += length
        utils.list_shift_column(codewordmap, 1, int(code[-1]))

    # logger.debug('------ frequencies ------')
    # logger.debug(freq)
    # logger.debug('-------------------------')

    return codewordmap

# flatten the result and convert 2 dict
key = list(chain.from_iterable(codewords(ciphertext)))

keydict = utils.list_2_dict(key)

# print(f"Here are the duplicate codewords: {utils.list_duplicates(list(keydict.values()))}")

# codewordmap = utils.dict_swap_keys_and_values(keydict)

# print(ciphertext)
# logger.debug(ciphertext)
# logger.debug('Warning! codewordmap values are incorrect position and order')
# logger.debug(codewordmap)
# logger.debug('Codewords might be wrong double check to make sure')
# logger.debug(list(codewordmap.keys()))

# if "part1" in filename:
#     logger.debug("-- part 1 crack specific info --")
#     same = Counter(list(codewordmap.keys())) == Counter(['4502', '53177', '946320122', '85053600', '7171031', '87445918', '4504', '692473', '20', '638440', '57643', '7004062', '52381', '930424404', '84524991', '89411894', '4254', '376', '88527391', '23', '29', '361', '923921735', '4468', '636187', '971559793'])
#     if same:
#         logger.debug("codewordmaps are the same")
#     else:
#         logger.debug("codewordmaps are different")

# monoalphabetic_cipher = decrypt(text, codewordmap)

# # should give you subsitution cipher
# # logger.debug(cyphertext)
# print(monoalphabetic_cipher)

# freq.restore_key(cyphertext, 26)




from collections import Counter

# Initial key mapping as given
key_mapping = keydict
# key_mapping = {
#     'A': "89411894",
#     'B': "52381",
#     'C': "88527391",
#     'D': "946320122",
#     'E': "923921735",
#     'F': "4254",
#     'G': "4504",
#     'H': "7171031",
#     'I': "692473",
#     'J': "971559793",
#     'K': "638440",
#     'L': "930424404",
#     'M': "84524991",
#     'N': "87445918",
#     'O': "57643",
#     'P': "7004062",
#     'Q': "376",
#     'R': "29",
#     'S': "4468",
#     'T': "85053600",
#     'U': "361",
#     'V': "636187",
#     'W': "20",
#     'X': "23",
#     'Y': "53177",
#     'Z': "4502"
# }

# Frequency of letters in the English language
english_frequency = {
    'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97,
    'N': 6.75, 'S': 6.33, 'H': 6.09, 'R': 5.99, 'D': 4.25,
    'L': 4.03, 'C': 2.78, 'U': 2.76, 'M': 2.41, 'W': 2.36,
    'F': 2.23, 'G': 2.02, 'Y': 1.97, 'P': 1.93, 'B': 1.29,
    'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15, 'Q': 0.10,
    'Z': 0.07
}

def extract_segments(ciphertext, key_mapping):
    """Extract segments from ciphertext based on the initial key mapping."""
    segments = []
    index = 0
    
    while index < len(ciphertext):
        for codeword in key_mapping.values():
            length = int(codeword[0])
            if ciphertext[index:index+length] == codeword:
                segments.append(codeword)
                index += length
                break
        else:
            raise ValueError("No matching codeword found in the initial key mapping.")
    
    return segments

def frequency_analysis(segments):
    """Analyze the frequency of segments in the ciphertext."""
    frequency = Counter(segments)
    total_segments = sum(frequency.values())
    for segment in frequency:
        frequency[segment] = (frequency[segment] / total_segments) * 100
    
    return frequency

def map_frequencies(ciphertext_frequency, english_frequency):
    """Map ciphertext frequencies to the closest English letter frequencies."""
    sorted_ciphertext = sorted(ciphertext_frequency.items(), key=lambda item: item[1], reverse=True)
    sorted_english = sorted(english_frequency.items(), key=lambda item: item[1], reverse=True)
    
    mapping = {}
    for (ciphertext_segment, _), (english_letter, _) in zip(sorted_ciphertext, sorted_english):
        mapping[ciphertext_segment] = english_letter
    
    return mapping

def apply_mapping(segments, mapping):
    """Apply the frequency mapping to the segments to generate the plaintext."""
    plaintext = ''.join(mapping.get(segment, segment) for segment in segments)
    return plaintext

# Example usage
# ciphertext = ""
try:
    segments = extract_segments(ciphertext, key_mapping)
    ciphertext_frequency = frequency_analysis(segments)
    mapping = map_frequencies(ciphertext_frequency, english_frequency)
    refined_text = apply_mapping(segments, mapping)
    
    print("Refined text:", refined_text)
except ValueError as e:
    print("Error:", e)