import copy
import string
import logging
import random
from pathlib import Path
from timeit import default_timer as timer

import helper.utils as utils

logger = logging.getLogger(Path(__file__).stem)
logger.setLevel('DEBUG')
filehandler_dbg = logging.FileHandler(logger.name + "-debug.log", mode='w')
filehandler_dbg.setLevel('DEBUG')
logger.addHandler(filehandler_dbg)

alphabet = list(string.ascii_uppercase)
FILENAME = "input/part1.txt"
ciphertext = open(FILENAME, "r", encoding='utf-8').read().strip()

def get_codewords(encrypted):
    start = 0
    codewords = set()
    while start < len(encrypted):
        length = int(encrypted[start])
        code = encrypted[start:start + length]
        codewords.add(code)
        start += length
    return list(codewords)

perf_start = timer()
codeword2letter = utils.dict_swap_keys_and_values(dict(zip(alphabet, get_codewords(ciphertext))))
print(f"It took {(timer()-perf_start)*1000:.2f}ms to get codewords.")

def decrypt_wo_key(encrypted, codeword2letter):
    codeword2letter = copy.deepcopy(codeword2letter)
    plaintext = ""
    start = 0
    while start < len(encrypted):
        length = int(encrypted[start])
        code = encrypted[start:start + length]
        # TODO: step stating it is unrealistic that "x" is next to "z"
        # Use hill climbing algo to find the best key
        plaintext += codeword2letter[code]
        codeword2letter = utils.dict_shift_keys(codeword2letter, int(code[-1]))
        start += length
    return plaintext

# idea: use bruteforce and frequency analysis to find key quickly

def quadgram_score(text):
    """Calculate the score of a text based on quadgram frequencies."""
    score = 0
    n = len(text)
    for i in range(n - 3):
        quadgram = text[i:i + 4]
        if quadgram in QUADGRAMS:
            score += QUADGRAMS[quadgram]
        else:
            score += math.log10(0.01 / n)
    return score

def decrypt_autokey(ciphertext, key):
    """Decrypt the ciphertext using the given key."""
    ciphertext = ciphertext.upper()
    key = key.upper()
    decrypted_text = []

    key_extended = key
    for i, char in enumerate(ciphertext):
        if char in string.ascii_uppercase:
            shift = ord(key_extended[i]) - ord('A')
            decrypted_char = chr((ord(char) - shift - ord('A')) % 26 + ord('A'))
            decrypted_text.append(decrypted_char)
            key_extended += decrypted_char  # Autokey mechanism
        else:
            decrypted_text.append(char)

    return ''.join(decrypted_text)

def hill_climbing(ciphertext, max_key_length=20, iterations=1000):
    """Use hill climbing to find the best key."""
    best_key = ""
    best_score = float('-inf')

    # Try different initial key lengths
    for key_length in range(1, max_key_length + 1):
        key = ['A'] * key_length
        for _ in range(iterations):
            # Generate a candidate key by modifying the current key
            candidate_key = key[:]
            position = random.randint(0, key_length - 1)
            candidate_key[position] = chr((ord(candidate_key[position]) - ord('A') + random.randint(1, 25)) % 26 + ord('A'))
            candidate_key_text = ''.join(candidate_key)

            decrypted_text = decrypt_autokey(ciphertext, candidate_key_text)
            score = quadgram_score(decrypted_text)

            # If the candidate key is better, update the key and score
            if score > best_score:
                best_key = candidate_key_text
                best_score = score
                key = candidate_key

    return best_key