#!/usr/bin/python3

from helper.crypto import encrypt, decrypt
import helper.utils as utils

encrypted = open("input/part1.txt", 'r', encoding='utf-8').read()
codewords = open("input/codewords.txt", "r", encoding='utf-8').read().splitlines()

letter2codeword = utils.list_2_dict(codewords)
codeword2letter = utils.dict_swap_keys_and_values(letter2codeword)

plaintext = decrypt(encrypted, codeword2letter)
print(plaintext)
print(encrypt(plaintext, letter2codeword))

print(len(encrypt(plaintext, letter2codeword)))

# THE CACHE IS LOCATED AT NORTH THIRTY NINE DEGREES TEN POINT FOUR EIGHT TWO YOULL ALSO NEED WEST SEVENTY SIX DEGREES FIFTY ONE POINT FOUR HUNDRED TWENTY TWO CACHE IS AB IS ON ON A FENCE