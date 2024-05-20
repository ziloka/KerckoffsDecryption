import string
import random
from collections import Counter
from timeit import default_timer as timer
import math

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

# Function to decrypt using a given key
def decrypt_autokey(ciphertext, key):
    decrypted = ""
    extended_key = key.upper()
    for i, char in enumerate(ciphertext):
        if char in string.ascii_uppercase:
            shift_amount = ord(extended_key[i]) - ord('A')
            decrypted += chr((ord(char) - ord('A') - shift_amount) % 26 + ord('A'))
            extended_key += decrypted[-1]
        else:
            decrypted += char
            extended_key += char
    return decrypted

# Simulated Annealing function to find the best key
def simulated_annealing(ciphertext, max_key_length, initial_temp, cooling_rate, iterations):
    ciphertext = ciphertext.upper()
    best_key = "A" * max_key_length
    best_decrypted = decrypt_autokey(ciphertext, best_key)
    best_freq = Counter(best_decrypted)
    best_chi_squared = chi_squared_statistic(best_freq, ENGLISH_FREQ, len(best_decrypted))

    current_key = best_key
    current_chi_squared = best_chi_squared

    temp = initial_temp

    for _ in range(iterations):
        # Create a new candidate key by modifying one character
        position = random.randint(0, max_key_length - 1)
        new_char = chr((ord(current_key[position]) - ord('A') + random.randint(1, 25)) % 26 + ord('A'))
        candidate_key = current_key[:position] + new_char + current_key[position + 1:]

        decrypted = decrypt_autokey(ciphertext, candidate_key)
        text_freq = Counter(decrypted)
        candidate_chi_squared = chi_squared_statistic(text_freq, ENGLISH_FREQ, len(decrypted))

        # Acceptance probability
        delta_chi_squared = candidate_chi_squared - current_chi_squared
        acceptance_prob = math.exp(-delta_chi_squared / temp) if delta_chi_squared > 0 else 1

        # Decide whether to accept the new candidate
        if random.random() < acceptance_prob:
            current_key = candidate_key
            current_chi_squared = candidate_chi_squared
            if current_chi_squared < best_chi_squared:
                best_key = current_key
                best_chi_squared = current_chi_squared
                best_decrypted = decrypted
                print(f"best key: {best_key}, best chi-squared: {best_chi_squared}, decrypted: {decrypted}")

        # Cool down the temperature
        temp *= cooling_rate

    return best_decrypted, best_key

# Main function to crack the Autokey cipher
def crack_autokey(ciphertext, max_key_length=20, initial_temp=100.0, cooling_rate=0.99, iterations=10000):
    return simulated_annealing(ciphertext, max_key_length, initial_temp, cooling_rate, iterations)

# Example usage
ciphertext = "IHWKYVFREZJSEHRSHSXBWIOXBRGNUAPTTWIZENINPWCPONWBNVIFEKLMDSSHWGEMICLLGFDOGOELSTZRTTSIAQYKEKSMZSJUEKHMRRLIIFSIVRMOMOGEEHNUMXONULHGMIKNABUXXNYSTZLSUTAEE"
best_decrypted, best_key = crack_autokey(ciphertext)
print("Best Decrypted Text:", best_decrypted)
print("Best Key:", best_key)
