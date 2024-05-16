import string
import numpy as np

codewords = open("input/codewords.txt", "r").read().splitlines()

list1 = list(string.ascii_uppercase)
list2 = codewords[1::2]

print(np.column_stack((list1, list2)))