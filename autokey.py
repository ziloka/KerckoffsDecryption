# https://chatgpt.com/share/3b4b4233-bc13-4b20-ac84-de5f680be82e

import string
from collections import Counter
import math

# Frequency of letters in English language
ENGLISH_FREQ = {
    'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97, 'N': 6.75,
    'S': 6.33, 'H': 6.09, 'R': 5.99, 'D': 4.25, 'L': 4.03, 'C': 2.78,
    'U': 2.76, 'M': 2.41, 'W': 2.36, 'F': 2.23, 'G': 2.02, 'Y': 1.97,
    'P': 1.93, 'B': 1.29, 'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15,
    'Q': 0.10, 'Z': 0.07
}

# Load English n-gram probabilities for more accurate frequency analysis
with open('quadgrams.txt', 'r') as f:
    QUADGRAMS = {line.split()[0]: math.log10(float(line.split()[1])) for line in f}

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

def main():
    # plaintext: dCodeAutoclave
    # initial keyword: X
    ciphertext = "aFqrhEunhqnlvz"
    
    print("Ciphertext:", ciphertext)
    
    best_key = hill_climbing(ciphertext)
    print("Guessed Key:", best_key)
    
    decrypted_text = decrypt_autokey(ciphertext, best_key)
    print("Decrypted Text:", decrypted_text)

if __name__ == "__main__":
    import random
    main()