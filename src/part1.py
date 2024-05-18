from timeit import default_timer as timer
from helper.crypto import decrypt
import helper.utils as utils

start = timer()
encrypted = open("input/part1.txt", "r").read()
codewords = open("input/codewords.txt", "r").read().splitlines()
print(f"Took {(timer()-start)*1000:.2f}ms to read the text files.")

codeworddict = utils.dict_swap_keys_and_values(utils.list_2_dict(codewords))
start = timer()
print(decrypt(encrypted, codeworddict))
print(f"It took {(timer()-start)*1000:.2f}ms to decrypt the text.")

# THE CACHE IS LOCATED AT NORTH THIRTY NINE DEGREES TEN POINT FOUR EIGHT TWO YOULL ALSO NEED WEST SEVENTY SIX DEGREES FIFTY ONE POINT FOUR HUNDRED TWENTY TWO CACHE IS AB IS ON ON A FENCE