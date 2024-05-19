import copy
import helper.utils as utils

def encrypt(plaintext, codewordmap):
    codewordmap = copy.deepcopy(codewordmap)
    encrypted = ""
    for letter in plaintext:
        code = codewordmap[letter]
        encrypted += code
        codewordmap = utils.dict_shift_values(codewordmap, int(code[-1]))
    return encrypted

def decrypt(encrypted, codewordmap):
    codewordmap = copy.deepcopy(codewordmap)
    plaintext = ""
    start = 0
    while start < len(encrypted):
        length = int(encrypted[start])
        code = encrypted[start:start + length]
        plaintext += codewordmap[code]
        codewordmap = utils.dict_shift_keys(codewordmap, int(code[-1]))
        start += length
    return plaintext