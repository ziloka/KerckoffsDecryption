from helper.crypto import encrypt, decrypt
import helper.utils as utils
import random

FILENAME = "input/part2.txt"
ciphertext = open(FILENAME, "r", encoding='utf-8').read().strip()
word = "NORTH"

def get_codewords(encrypted):
    start = 0
    codewords = list()
    while start < len(encrypted):
        length = int(encrypted[start])
        code = encrypted[start:start + length]
        codewords.append(code)
        start += length
    return codewords

codes = get_codewords(ciphertext)

uniquecodes = []
for code in codes:
    if not code in uniquecodes:
        uniquecodes.append(code)

mapping = {chr(i) : "-" for i in range(65, 65+26)}

# for start in range(0, len(codes)-len(word)):
shift = 0
for i in range(len(word)):
    mapping[chr((ord(word[i])-shift-65)%26 + 65)] = codes[i]
    shift += int(codes[i][-1])
    uniquecodes.remove(codes[i])

for letter in mapping.keys():
    if mapping[letter] != "-":
        continue
    if len(uniquecodes) == 0:
        break
    randomcode = random.choice(uniquecodes)
    mapping[letter] = randomcode
    uniquecodes.remove(randomcode)
print(mapping)

inv_map = {v: k for k, v in mapping.items()}
print(inv_map)
print(decrypt(ciphertext, inv_map))