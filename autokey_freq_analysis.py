# prompt: write a python script that can decrypt autokey ciphers without the key using frequency analysis
# make sure you try your hardest to make the most accurate, effective script

# chatgpt (gpt-4o) generated the following code

import string
from collections import Counter

# Frequency of English letters
ENGLISH_FREQ = {
    'E': 12.02, 'T': 9.10, 'A': 8.12, 'O': 7.68, 'I': 7.31, 'N': 6.95, 'S': 6.28,
    'R': 6.02, 'H': 5.92, 'D': 4.32, 'L': 3.98, 'U': 2.88, 'C': 2.71, 'M': 2.61,
    'F': 2.30, 'Y': 2.11, 'W': 2.09, 'G': 2.03, 'P': 1.82, 'B': 1.49, 'V': 1.11,
    'K': 0.69, 'X': 0.17, 'Q': 0.11, 'J': 0.10, 'Z': 0.07
}

# Function to get the chi-squared statistic
def chi_squared_statistic(text_freq, english_freq, text_length):
    chi_squared = 0.0
    for letter in english_freq:
        observed = text_freq.get(letter, 0)
        expected = english_freq[letter] * text_length / 100
        chi_squared += (observed - expected) ** 2 / expected
    return chi_squared

# Function to perform a single letter shift
def shift(text, amount):
    shifted = ""
    for char in text:
        if char in string.ascii_uppercase:
            shifted += chr((ord(char) - ord('A') - amount) % 26 + ord('A'))
        else:
            shifted += char
    return shifted

# Function to decrypt using a given key
def decrypt_autokey(ciphertext, key):
    decrypted = ""
    extended_key = key.upper() + decrypted
    for i, char in enumerate(ciphertext):
        if char in string.ascii_uppercase:
            shift_amount = ord(extended_key[i]) - ord('A')
            decrypted += chr((ord(char) - ord('A') - shift_amount) % 26 + ord('A'))
            extended_key += decrypted[-1]
        else:
            decrypted += char
            extended_key += char
    return decrypted

# Main function to crack the Autokey cipher
def crack_autokey(ciphertext):
    ciphertext = ciphertext.upper()
    best_guess = ""
    best_chi_squared = float('inf')

    for _ in range(1, 10):  # Trying different key lengths
        for key in (chr(i) for i in range(ord('A'), ord('Z')+1)):
            decrypted = decrypt_autokey(ciphertext, key)
            text_freq = Counter(decrypted)
            chi_squared = chi_squared_statistic(text_freq, ENGLISH_FREQ, len(decrypted))
            if chi_squared < best_chi_squared:
                best_chi_squared = chi_squared
                best_guess = decrypted
                best_key = key

    return best_guess, best_key

# Example usage
# plaintext: dCodeAutoclave
# initial keyword: X
ciphertext = "aFqrhEunhqnlvz"
plaintext, key = crack_autokey(ciphertext)
print(f"Decrypted Text: {plaintext}")
print(f"Guessed Key: {key}")