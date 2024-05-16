import re
from collections import deque

string = open("input.txt", "r").read()
contents = open("part1.txt", "r").read().splitlines()
# https://stackoverflow.com/a/12739974
codemap = {v: k for k, v in dict(zip(*[iter(contents)]*2)).items()}

# https://stackoverflow.com/a/21139641
def dict_shift_keys(dct, n):
    shift_keys = deque(dct.keys())
    shift_keys.rotate(n)
    return dict(zip(shift_keys, dct.values()))

while any(char.isdigit() for char in string):
    result = re.search("\d+", string)
    start = result.start()
    code = string[start:start + int(string[start])]
    string = string.replace(code, codemap[code], 1)
    # print(f"{codemap}\n{code[-1]}\n")
    codemap = dict_shift_keys(codemap, int(code[-1]))

print(string)
