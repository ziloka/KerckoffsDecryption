from helper.crypto import encrypt, decrypt, caesar_cipher
import helper.utils as utils
import random

#set ciphertext file and word to find
FILENAME = "input/part2.txt"
ciphertext = open(FILENAME, "r", encoding='utf-8').read().strip()
word = "NORTHTHIRTAT"

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
uniquecodes = []
for code in codes:
    if not code in uniquecodes:
        uniquecodes.append(code)
mapping = {chr(i) : "-" for i in range(65, 65+26)}

#loops until cant anymore, keeps moving start up and finding which mappings work
start = 0
while start < len(codes)-len(word):
    codes = get_codewords(ciphertext)
    uniquecodes = []
    for code in codes:
        if not code in uniquecodes:
            uniquecodes.append(code)
    mapping = {chr(i) : "-" for i in range(65, 65+26)}

    shift = 0
    for i in range(len(word)):
        letter = chr((ord(word[i])-shift-65)%26 + 65)
        if start == 0 or 190 < start < 200 or 205 < start < 215 or 245 < start < 255 or 280 < start < 290:
            print(start, i, letter, codes[start + i])
        # if codes[start+i] in mapping.values():
        #     print(mapping[letter])
        #     print(mapping[letter] != "-", letter != list(mapping.keys())[list(mapping.values()).index(codes[start+i])] and codes[start+i] in mapping.values())
        # if (mapping[letter] != "-" and codes[start+i] in mapping.values()) and letter != list(mapping.keys())[list(mapping.values()).index(codes[start+i])]:
        #     print("HUHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH")
        #     print(letter, mapping)
        #     break
        if codes[start+i] in mapping.values():
            if letter != list(mapping.keys())[list(mapping.values()).index(codes[start+i])]:
                break
        if mapping[letter] != "-":
            if mapping[letter] != codes[start+i]:
                break
        mapping[letter] = codes[start+i]
        shift += int(codes[start+i][-1])
        if codes[start+i] in uniquecodes:
            uniquecodes.remove(codes[start+i])
    else:
        print('we found one')
        goodmappings.append((start, mapping))
    start += 1
print("first half done")

#decrypts using mapping, assigns random code to alphabet we dont know
for gstart, gmapping in goodmappings:
    print(gstart, gmapping)
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
    print(inv_map)
    msg = decrypt(ciphertext, inv_map)
    print(gstart, ord(word[0])-ord(msg[gstart]))
    #it was getting caesar cipher shifted by some amount idk why
    msg = caesar_cipher(msg, ord(word[0])-ord(msg[gstart])) 
    print(msg)

#if goodmappings is empty there is no key possible to make the word appear in the ciphertext
print(len(goodmappings))
if len(goodmappings)==0:
    print("didnt work (word not found in msg)")



#194 210 250 285