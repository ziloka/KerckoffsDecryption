import numpy as np
from helper.utils import chisquare

# Known frequency of letters in English text (percentage)
# https://pi.math.cornell.edu/~mec/2003-2004/cryptography/subs/frequencies.html
english_letter_freq = {
    'A': 8.2, 'B': 1.5, 'C': 2.8, 'D': 4.3, 'E': 13.0, 'F': 2.2, 'G': 2.0,
    'H': 6.1, 'I': 7.0, 'J': 0.15, 'K': 0.77, 'L': 4.0, 'M': 2.4, 'N': 6.7,
    'O': 7.5, 'P': 1.9, 'Q': 0.095, 'R': 6.0, 'S': 6.3, 'T': 9.1, 'U': 2.8,
    'V': 0.98, 'W': 2.4, 'X': 0.15, 'Y': 2.0, 'Z': 0.074
}

def calculate_letter_frequencies(text):
    text = text.upper()
    letter_counts = {letter: 0 for letter in english_letter_freq.keys()}
    total_letters = 0

    for char in text:
        if char in letter_counts:
            letter_counts[char] += 1
            total_letters += 1

    if total_letters == 0:
        return letter_counts

    letter_freqs = {letter: (count / total_letters) * 100 for letter, count in letter_counts.items()}
    return letter_freqs

def chi_square_test(observed, expected):
    observed_values = np.array(list(observed.values()))
    expected_values = np.array(list(expected.values()))
    chi2, p = chisquare(observed_values, f_exp=expected_values)
    return chi2, p

def detect_gibberish(text, alpha=0.05, min_length=50):
    if len(text) < min_length:
        return "Text too short for reliable analysis", None, None

    observed_freqs = calculate_letter_frequencies(text)
    chi2, p = chi_square_test(observed_freqs, english_letter_freq)
    return p < alpha, chi2, p

# Example usage
text = "This is a sample text to check if it is gibberish or understandable English."

result, chi2_value, p_value = detect_gibberish(text)

print(f"Chi2 Value: {chi2_value}")
print(f"P-Value: {p_value}")
if result:
    print("The text is comprehensible English")
else:
    print("The text is gibberish")
