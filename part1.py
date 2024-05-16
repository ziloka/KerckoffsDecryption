from src.crypto import decrypt
from src.utils import list_2_dict, dict_swap_keys_and_values

encrypted = open("input/part1.txt", "r").read()
codewords = open("input/codewords.txt", "r").read().splitlines()

print(decrypt(encrypted, dict_swap_keys_and_values(list_2_dict(codewords))))
