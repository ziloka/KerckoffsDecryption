import copy
import helper.utils as utils

def encrypt(plaintext, letter2codeword):
    letter2codeword = copy.deepcopy(letter2codeword)
    encrypted = ""
    for letter in plaintext:
        code = letter2codeword[letter]
        encrypted += code
        letter2codeword = utils.dict_shift_values(letter2codeword, int(code[-1]))
    return encrypted

def decrypt(encrypted, codeword2letter):
    codeword2letter = copy.deepcopy(codeword2letter)
    plaintext = ""
    start = 0
    while start < len(encrypted):
        length = int(encrypted[start])
        code = encrypted[start:start + length]
        plaintext += codeword2letter[code]
        codeword2letter = utils.dict_shift_keys(codeword2letter, int(code[-1]))
        start += length
    return plaintext