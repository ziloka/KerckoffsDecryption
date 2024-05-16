import regex
from collections import deque

contents = open("part1.txt", "r").read().splitlines()
# https://stackoverflow.com/a/12739974
codemap = dict(zip(*[iter(contents)]*2))

# swap the keys and the values
codemap = {v: k for k, v in codemap.items()}
string = open("input.txt", "r").read()
plaintext = ""

# https://stackoverflow.com/a/21139641
def dict_roll(dct, n):
    shift_values = deque(dct.values())
    shift_values.rotate(n)
    return dict(zip(dct.keys(), shift_values))

i = 0
while i < len(string):
    length = string[i]
    code = string[i:i+int(length)]
    plaintext += codemap[code]
    dict_roll(codemap, int(code[-1]))

    # print(code)
    # for key in codemap:
        # string = string.replace(key, codemap[key])

print(plaintext)