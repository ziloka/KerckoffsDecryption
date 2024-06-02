# this is an autokey where the key is given by the last digit of the codeword
# this means it is a ciphertext-autokey, the less common kind
# it says that after each codeword is produced, the alphabet table is shifted by an amount equal to the last digit
# so when you go to encipher the third codeword, the alphabet table has previously been shifted by the last digit of the first codeword plus the last digit of the second codeword. so for each codeword you know the total shift that was applied to the alphabet at that point
# for example here are the first several codewords together with the shift that was used for each codeword. you can assume the shift for the first codeword is zero because the rest of the solution will be the same no matter the initial shift.

import string
from timeit import default_timer as timer

start = timer()
alphabet = list(string.ascii_uppercase)
FILENAME = "input/part2.txt"
ciphertext = open(FILENAME, "r", encoding='utf-8').read().strip()

ASCII_CODE_a = 97
ASCII_CODE_A = 65

def get_codewords(encrypted: str) -> set[str]:
    start = 0
    codewords = list()
    while start < len(encrypted):
        length = int(encrypted[start])
        code = encrypted[start:start + length]
        codewords.append(code)
        start += length
    return codewords

codewords = get_codewords(ciphertext)

# the key is the shift number (the position the letter is in the english alphabet)
# the value is all codewords with the same exact shift, this list of [start, end] positions can be replaced with a single letter

# key is in x_y format, x is the start pos, y is the end pos
# value maps to a number that represents the position in the alphabet

shift = 0
start = 0
updated_ciphertext = ""
shifts = []
for codeword in codewords:
    last = int(codeword[-1])
    end = start + len(codeword)
    updated_ciphertext += chr(shift + ASCII_CODE_A)
    shifts.append(shift)
    start += len(codeword)
    shift += last
    shift %= 26

# keep track of both the 26 different frequency charts, and the positions of those 26 groups within the ciphertexts. 
charts = {i: {letter: [] for letter in alphabet} for i in range(len(alphabet))}

# one of the things you can do with the frequency charts is to divide the code words into "high", "medium", and "low frequency" classes within each chart.
# in the ciphertext you can identify each code word (each letter) as one of those H/M/L classes by looking at which group the letter (codeword) is in.

frequency_classes = {
    "H": "ETAOINSR",
    "M": "HDLCUMFPGWYBV",
    "L": "JKQXZ"
}

start = 0
for i, letter in enumerate(updated_ciphertext):
    shift = shifts[i]

    freq_class = ""
    for k, v in frequency_classes.items():
        if letter in v:
            freq_class = k
            break
    if len(freq_class) == 0:
        raise Exception(f"Did not expect character {letter}. This character is not in the english alphabet")
    
    # print(f"{letter} charts[{shift}]['{freq_class}']")
    charts[shift][freq_class].append(letter)

    start += len(codeword)

print(charts)

# # you can also use this to place the crib you mentioned earlier. the three classes are roughly  ETAOINSR, HDLCUMFPGWYBV, and JKQXZ
# you can also find positions where it is impossible to place that crib, because doing so would assign the same letter to two different codewords within the same group, or two different letters to the same codeword+group

# the assigned frequency classes for the crib

# NORTHTHIRTYNINEDEGREES
# HHHHMHMHHHMHHHHMHMHHHH

# print(f"took {timer()-start:.0f}ms")