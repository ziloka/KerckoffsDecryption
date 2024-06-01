# use a dictionary of quadgrams to try and map some letters
# use frequency analysis to check if the ciphertext gets closer to something that looks like english

import string
import sys
import random
# from timeit import default_timer as timer

seed = random.randrange(sys.maxsize)
random.seed(seed)
print("seed:", seed)

alphabet = list(string.ascii_uppercase)
FILENAME = "input/part1.txt"
ciphertext = open(FILENAME, "r", encoding='utf-8').read().strip()

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

# words = ["NORTHTHIRTYNINEDEGREES", "WESTSEVENTYSIXDEGREES"]

# plaintext = "NORTHTHIRTYNINEDEGREES"

# the key is the shift number
# the value is all codewords with the same exact shift, this list of [start, end] positions can be replaced with a single letter
# the resulting text can be decrypted as a monoalphabetic cipher
frequency_charts = {i: [] for i in range(len(alphabet))}
shifts_dict = {i: [] for i in range(len(alphabet))}

# Index of concidence
shift = 0
start = 0
# monoalphabetic_cipher = ""
for codeword in codewords:
    last = int(codeword[-1])
    # monoalphabetic_cipher += alphabet[shift]
    shifts_dict[shift].append([start, start + len(codeword)])
    start += len(codeword)
    shift += last
    shift %= 26

# print(monoalphabetic_cipher)

# monoalphabetic cipher stuff
# keep track of both the 26 different frequency charts, and the positions of those 26 groups within the ciphertexts. 
# one of the things you can do with the frequency charts is to divide the code words into "high", "medium", and "low frequency" classes within each chart.
# then in the ciphertext you can identify each code word (each letter) as one of those H/M/L classes by looking at which group the code word is in.
# you can also use this to place the crib you mentioned earlier. the three classes are roughly  ETAOINSR, HDLCUMFPGWYBV, and JKQXZ

# the assigned frequency classes for the crib

# NORTHTHIRTYNINEDEGREES
# HHHHMHMHHHMHHHHMHMHHHH

