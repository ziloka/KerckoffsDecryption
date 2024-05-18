import re
from collections import Counter
import string

def find_repeated_sequences(ciphertext, min_length=3):
    sequences = {}
    for length in range(min_length, len(ciphertext)//2):
        for i in range(len(ciphertext) - length):
            sequence = ciphertext[i:i+length]
            matches = [m.start() for m in re.finditer(f'(?={re.escape(sequence)})', ciphertext)]
            if len(matches) > 1:
                sequences[sequence] = matches
    return sequences

def find_factors(n):
    factors = []
    for i in range(2, n + 1):
        if n % i == 0:
            factors.append(i)
    return factors

def find_most_common_factor(distances):
    factor_counts = Counter()
    for dist in distances:
        factors = find_factors(dist)
        factor_counts.update(factors)
    common_factors = factor_counts.most_common()
    if common_factors:
        return common_factors[0][0]
    else:
        return None

def compute_distances(sequences):
    distances = []
    for seq, indexes in sequences.items():
        for i in range(len(indexes) - 1):
            distance = indexes[i + 1] - indexes[i]
            distances.append(distance)
    return distances

def kasiski_examination(ciphertext, min_length=3):
    sequences = find_repeated_sequences(ciphertext, min_length)
    distances = compute_distances(sequences)
    keyword_length = find_most_common_factor(distances)
    return keyword_length

def frequency_analysis(ciphertext, keyword_length):
    frequencies = []
    for i in range(keyword_length):
        nth_letters = ciphertext[i::keyword_length]
        frequency = Counter(nth_letters)
        frequencies.append(frequency)
    return frequencies

def get_shift_for_char(char, most_common):
    shift = (ord(char) - ord(most_common)) % 26
    return shift

def find_keyword(ciphertext, keyword_length):
    english_letter_frequency = 'ETAOINSHRDLCUMWFGYPBVKJXQZ'
    most_common_letter = 'E'  # Most common letter in English
    keyword = []

    frequencies = frequency_analysis(ciphertext, keyword_length)
    for frequency in frequencies:
        # Find the most frequent letter in the ciphertext position
        most_frequent_cipher_letter = frequency.most_common(1)[0][0].upper()
        # Calculate the shift assuming the most frequent letter maps to 'E'
        shift = get_shift_for_char(most_frequent_cipher_letter, most_common_letter)
        # Derive the corresponding keyword letter
        keyword_letter = chr((shift + ord('A')) % 26 + ord('A'))
        keyword.append(keyword_letter)

    return ''.join(keyword)

def decrypt_with_key(ciphertext, key):
    decrypted_text = []
    key_length = len(key)
    for i, char in enumerate(ciphertext):
        if char.isalpha():
            shift = ord(key[i % key_length].upper()) - ord('A')
            if char.isupper():
                decrypted_char = chr((ord(char) - shift - ord('A')) % 26 + ord('A'))
            else:
                decrypted_char = chr((ord(char) - shift - ord('a')) % 26 + ord('a'))
            decrypted_text.append(decrypted_char)
        else:
            decrypted_text.append(char)
    return ''.join(decrypted_text)

def main():
    ciphertext = "IIPQIFYSTQWWBTNUIUREUF"
    
    # Step 1: Find keyword length
    keyword_length = kasiski_examination(ciphertext)
    print(f"Probable Keyword Length: {keyword_length}")

    if keyword_length:
        # Step 2: Find the keyword
        keyword = find_keyword(ciphertext, keyword_length)
        print(f"Derived Keyword: {keyword}")

        # Step 3: Decrypt the ciphertext with the found key
        decrypted_text = decrypt_with_key(ciphertext, keyword)
        print(f"Decrypted Text: {decrypted_text}")

if __name__ == "__main__":
    main()