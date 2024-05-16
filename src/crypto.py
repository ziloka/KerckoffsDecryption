import re
from collections import deque

# https://stackoverflow.com/a/21139641
# shift dct (dict) values by n to right if n is positive
# and to left if n is negative; returns new dictionary
def dict_shift_values(dct, n):
    shift_values = deque(dct.values())
    shift_values.rotate(n)
    return dict(zip(dct.keys(), shift_values))

def dict_shift_keys(dct, n):
    shift_keys = deque(dct.keys())
    shift_keys.rotate(n)
    return dict(zip(shift_keys, dct.values()))

def decrypt(text: str, codewordmap: dict[str, str]):
    while any(char.isdigit() for char in text):
        result = re.search("\d+", text)
        start = result.start()
        length = int(text[start])
        code = text[start:start + length]
        text = text.replace(code, codewordmap[code], 1)
        codewordmap = dict_shift_keys(codewordmap, int(code[-1]))
    return text