import copy
import helper.utils as utils

def decrypt(encrypted, codewordmap):
    codewordmap = copy.deepcopy(codewordmap)
    decrypted = ""
    start = 0
    while any(char.isdigit() for char in encrypted) and start < len(encrypted):
        length = int(encrypted[start])
        code = encrypted[start:start + length]
        letter = codewordmap[code]
        decrypted += letter
        utils.dict_shift_keys(codewordmap, int(code[-1]))
        start += length
    return decrypted