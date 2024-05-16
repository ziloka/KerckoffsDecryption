# The same letter could appear multiple times in the mapping with different codewords.
# The letters might not appear in alphabetical order in the mapping.
# Other symbols like punctuation or whitespace could also have entries in the mapping.
# Finally shorter codewords could "hide" inside longer codewords (such as having both codewords "321" and "53214") to confuse frequency analysis.
# None of these additional countermeasures will be employed for these puzzles (at least intentionally, all keys have been generated randomly).

import re
import string
import copy
from collections import deque
from itertools import chain
from src.crypto import decrypt
from src.utils import dict_shift_values, dict_swap_keys_and_values, list_shift_column, list_2_dict

alphabet = list(string.ascii_uppercase)
text = open("input/part2.txt", "r").read()

def crack(encrypted):
    i = 0
    key = [[letter, ''] for letter in alphabet]
    while any(char.isdigit() for char in encrypted) and i < len(alphabet):
        result = re.search("\d+", encrypted)
        start = result.start()
        length = int(encrypted[start])
        code = encrypted[start:start + length]
        key[i][1] = code
        letter = key[i][0]
        encrypted = encrypted.replace(code, letter, 1)
        list_shift_column(key, 1, int(code[-1]))
    return key

# flatten the result and convert 2 dict
key = list(chain.from_iterable(crack(copy.deepcopy(text))))

# if len(set(key)) != len(key):
#     print("Warning! There are duplicates!")
print(len(key))

key = dict_swap_keys_and_values(list_2_dict(key))

# print(key)
print(len(key))

# Try shifting the keys (letters) in the dict times
for i in range(0, len(alphabet)):
    dict_shift_values(key, 1)
    print(decrypt(text, key))