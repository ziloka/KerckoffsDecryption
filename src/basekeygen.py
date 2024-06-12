import random
import string
from helper.crypto import decrypt, caesar_cipher_decrypt
# import helper.utils as utils

#set ciphertext file and word to find
FILENAME = "input/part1.txt"
ciphertext = open(FILENAME, "r", encoding='utf-8').read().strip()
CRIB = "NORTHTHIRTYNINEDEGREES".upper()

#gets all codes in ciphertext
def get_codewords(encrypted):
    start = 0
    codewords = list()
    while start < len(encrypted):
        length = int(encrypted[start])
        code = encrypted[start:start + length]
        codewords.append(code)
        start += length
    return codewords

#goodmappings are mappings which satisfy the word and ciphertext
goodmappings = []
codes = get_codewords(ciphertext)

#loops until cant anymore, keeps moving start up and finding which mappings work
for start in range(len(codes)-len(CRIB)):
    codes = get_codewords(ciphertext)
    uniquecodes = [*set(codes)]
    mapping = {letter: "-" for letter in string.ascii_uppercase}

    shift = 0
    for i, letter in enumerate(CRIB):
        letters = [*mapping.keys()]
        letter = chr((ord(letter)-shift-65)%26 + 65)
        codewords = [*mapping.values()]
        codeword = codes[start+i]

        isWrongLetter = mapping[letter] != "-" and mapping[letter] != codeword
        isMisaligned = codeword in codewords and letter != letters[codewords.index(codeword)]

        if isWrongLetter or isMisaligned:
            break
        mapping[letter] = codeword
        shift += int(codeword[-1])
        if codeword in uniquecodes:
            uniquecodes.remove(codeword)
    else:
        # print('we found one')
        goodmappings.append((start, mapping))
# print("first half done")

#decrypts using mapping, assigns random code to alphabet we dont know
for gstart, gmapping in goodmappings:
    # print(gstart, gmapping)
    uniquecodes = []
    for code in codes:
        if not code in uniquecodes and not code in gmapping.values():
            uniquecodes.append(code)
    for letter in gmapping.keys():
        if gmapping[letter] != "-":
            continue
        if len(uniquecodes) == 0:
            break
        randomcode = random.choice(uniquecodes)
        gmapping[letter] = randomcode
        uniquecodes.remove(randomcode)

    inv_map = {v: k for k, v in gmapping.items()}
    msg = decrypt(ciphertext, inv_map)
    #it was getting caesar cipher shifted by some amount idk why
    msg = caesar_cipher_decrypt(msg, ord(CRIB[0])-ord(msg[gstart]))
    print(msg)

#if goodmappings is empty there is no key possible to make the word appear in the ciphertext
print((goodmappings))

if len(goodmappings)==0:
    print("didnt work (word not found in msg)")



#194 210 250 285