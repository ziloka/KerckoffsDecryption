import re
from .utils import dict_shift_keys

def decrypt(text: str, codewordmap: dict[str, str]):
    while any(char.isdigit() for char in text):
        result = re.search("\d+", text)
        start = result.start()
        length = int(text[start])
        code = text[start:start + length]
        text = text.replace(code, codewordmap[code], 1)
        codewordmap = dict_shift_keys(codewordmap, int(code[-1]))
    return text