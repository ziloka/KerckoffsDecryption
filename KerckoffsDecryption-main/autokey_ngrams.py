# https://chatgpt.com/share/3b4b4233-bc13-4b20-ac84-de5f680be82e

import sys
import string
import math
import random
from timeit import default_timer as timer
from helper.crypto import decrypt

seed = random.randrange(sys.maxsize)
random.seed(seed)

ENGLISH_FREQ = {
    'E': 12.02, 'T': 9.10, 'A': 8.12, 'O': 7.68, 'I': 7.31, 'N': 6.95, 'S': 6.28,
    'R': 6.02, 'H': 5.92, 'D': 4.32, 'L': 3.98, 'U': 2.88, 'C': 2.71, 'M': 2.61,
    'F': 2.30, 'Y': 2.11, 'W': 2.09, 'G': 2.03, 'P': 1.82, 'B': 1.49, 'V': 1.11,
    'K': 0.69, 'X': 0.17, 'Q': 0.11, 'J': 0.10, 'Z': 0.07
}

def chi_squared_statistic(text_freq, english_freq, text_length):
    chi_squared = 0.0
    for letter in english_freq:
        observed = text_freq.get(letter, 0)
        expected = english_freq[letter] * text_length / 100
        if expected > 0:  # Avoid division by zero
            chi_squared += (observed - expected) ** 2 / expected
    return chi_squared

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

            decrypted_text = decrypt(ciphertext, candidate_key_text)
            score = quadgram_score(decrypted_text)

            # If the candidate key is better, update the key and score
            if score > best_score:
                best_key = candidate_key_text
                best_score = score
                key = candidate_key

    return best_key

def main():
    # plaintext: dCodeAutoclave
    # initial keyword: X
    ciphertext = "aFqrhEunhqnlvz"
    start = timer()

    # print("Ciphertext:", ciphertext)

    best_key = hill_climbing(ciphertext)
    # print("Guessed Key:", best_key)

    decrypted_text = decrypt_autokey(ciphertext, best_key)
    print(f"took {(timer()-start)*1000:.2f}ms")
    print("Decrypted Text:", decrypted_text)
    

if __name__ == "__main__":
    main()
