import re
from collections import deque

contents = open("part1.txt", "r").read().splitlines()
# https://stackoverflow.com/a/12739974
codemap = dict(zip(*[iter(contents)]*2))

# swap the keys and the values
codemap = {v: k for k, v in codemap.items()}
string = open("input.txt", "r").read()

# https://stackoverflow.com/a/21139641
def dict_roll(dct, n):
    shift_values = deque(dct.values())
    shift_values.rotate(n)
    return dict(zip(dct.keys(), shift_values))

while any(char.isdigit() for char in string):
    result = re.search("\d+", string)
    length = string[result.start()]
    code = string[result.start():result.start() + int(length)]
    # print(f": {result.start()} {result.end()} {length} {code}\n")
    string = string.replace(code, codemap[code], 1)
    dict_roll(codemap, int(code[-1]))

print(string)
