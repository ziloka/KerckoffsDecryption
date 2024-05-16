# The same letter could appear multiple times in the mapping with different codewords.
# The letters might not appear in alphabetical order in the mapping.
# Other symbols like punctuation or whitespace could also have entries in the mapping.
# Finally shorter codewords could "hide" inside longer codewords (such as having both codewords "321" and "53214") to confuse frequency analysis.
# None of these additional countermeasures will be employed for these puzzles (at least intentionally, all keys have been generated randomly).

import re
import string
import copy
from collections import deque
from src.crypto import decrypt, dict_shift_values

text = open("part2.txt", "r").read()

i = 0
alphabet = list(string.ascii_uppercase)
codewordmap = [''] * len(alphabet)
print(codewordmap)
encrypted = copy.deepcopy(text)
while any(char.isdigit() for char in encrypted) and i < len(alphabet):
    results = re.finditer("\d+", encrypted)
    for result in results:
        start = result.start()
        length = int(encrypted[start])
        code = encrypted[start:start + length]
        if code not in codewordmap:
            codewordmap[i] = [code, alphabet[i]]
        else:
            # print(f"{codewordmap}")
            print(f"[{start}] code: {code} already exists in alphabet: {alphabet[i]}")
            continue
        i+=1
        encrypted = encrypted.replace(code, codewordmap[code], 1)
    # print(f"{i} {codewordmap}")

# Try checking if shorter codewords are in larger codewords

# Try shifting the keys (letters) in the dict 24 times
# print(text)
# print(len(codewordmap))
# print(codewordmap)

# for i in range(0, 24):
#     dict_shift_values(codewordmap, i)
#     # print(codewordmap)
#     print(decrypt(text, codewordmap))

