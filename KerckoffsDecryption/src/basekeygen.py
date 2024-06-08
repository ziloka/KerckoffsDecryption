from helper.crypto import encrypt, decrypt, caesar_cipher
import helper.utils as utils
import random

FILENAME = "input/part1.txt"
ciphertext = open(FILENAME, "r", encoding='utf-8').read().strip()
word = "THIRTYNINEDEGREE"


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
        if start == 91:
            print(start, i, letter, codes[start + i])
        # if codes[start+i] in mapping.values():
        #     print(mapping[letter])
        #     print(mapping[letter] != "-", letter != list(mapping.keys())[list(mapping.values()).index(codes[start+i])] and codes[start+i] in mapping.values())
        # if (mapping[letter] != "-" and codes[start+i] in mapping.values()) and letter != list(mapping.keys())[list(mapping.values()).index(codes[start+i])]:
        #     print("HUHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH")
        #     print(letter, mapping)
        #     break
        if mapping[letter] != "-":
            #print("the - wasnt there!!! oh no!!!")
            if mapping[letter] != codes[start+i]:
                #print("OK THE - WASNT THERE AND ALSO THE CODE WAS DIFFERENT SO KILL IT !!!")
                break
        if codes[start+i] in mapping.values():
            #print("the codes already in mapping!! oh no!!!")
            if letter != list(mapping.keys())[list(mapping.values()).index(codes[start+i])]:
                #print("ok we can break now! no 26 mod")
                break
        mapping[letter] = codes[start+i]
        shift += int(codes[start+i][-1])
        if codes[start+i] in uniquecodes:
            uniquecodes.remove(codes[start+i])
    else:
        print("we doneeeee")
        break
    start += 1
print("first done")

print(mapping)
if start != len(codes)-len(word):
    for letter in mapping.keys():
        if mapping[letter] != "-":
            continue
        if len(uniquecodes) == 0:
            break
        randomcode = random.choice(uniquecodes)
        mapping[letter] = randomcode
        uniquecodes.remove(randomcode)

    inv_map = {v: k for k, v in mapping.items()}
    print(inv_map)
    msg = decrypt(ciphertext, inv_map)
    print(start, ord(word[0])-ord(msg[start]))
    #it was getting caesar cipher shifted by some amount idk why
    msg = caesar_cipher(msg, ord(word[0])-ord(msg[start])) 
    print(msg)

else:
    print("DOESNT WORKKAOPSKDOPASKDPAK (word not in message)")