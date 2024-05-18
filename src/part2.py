# The same letter could appear multiple times in the mapping with different codewords.
# The letters might not appear in alphabetical order in the mapping.
# Other symbols like punctuation or whitespace could also have entries in the mapping.
# Finally shorter codewords could "hide" inside longer codewords (such as having both codewords "321" and "53214") to confuse frequency analysis.
# None of these additional countermeasures will be employed for these puzzles (at least intentionally, all keys have been generated randomly).

import string
from pathlib import Path
import logging
from collections import Counter

from helper.crypto import decrypt
import helper.utils as utils
# from helper.polysub import kasiski

logger = logging.getLogger(Path(__file__).stem)
logger.setLevel('DEBUG')
filehandler_dbg = logging.FileHandler(logger.name + "-debug.log", mode='w')
filehandler_dbg.setLevel('DEBUG')
logger.addHandler(filehandler_dbg)

alphabet = list(string.ascii_uppercase)
filename = "input/part1.txt"
ciphertext = open(filename, "r").read().strip()

def getCodewords(encrypted):
    start = 0
    codewords = set()
    while any(char.isdigit() for char in encrypted) and start < len(encrypted):
        length = int(encrypted[start])
        code = encrypted[start:start + length]
        codewords.add(code)
        start += length
    return list(codewords)

key_mapping = dict(zip(alphabet, getCodewords(ciphertext)))
print(key_mapping)

# Frequency of letters in the English language
english_frequency = {
    'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97,
    'N': 6.75, 'S': 6.33, 'H': 6.09, 'R': 5.99, 'D': 4.25,
    'L': 4.03, 'C': 2.78, 'U': 2.76, 'M': 2.41, 'W': 2.36,
    'F': 2.23, 'G': 2.02, 'Y': 1.97, 'P': 1.93, 'B': 1.29,
    'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15, 'Q': 0.10,
    'Z': 0.07
}

def extract_segments(ciphertext, key_mapping):
    """Extract segments from ciphertext based on the initial key mapping."""
    segments = []
    index = 0
    
    while index < len(ciphertext):
        found = False
        for codeword in key_mapping.values():
            length = int(codeword[0])
            if ciphertext[index:index+length] == codeword:
                segments.append(codeword)
                index += length
                found = True
                break
        if not found:
            print(f"start: {index}, end: {index+length}, {ciphertext[index:index+length]}")
            raise ValueError("No matching codeword found in the initial key mapping.")
    
    return segments

def frequency_analysis(segments):
    """Analyze the frequency of segments in the ciphertext."""
    frequency = Counter(segments)
    total_segments = sum(frequency.values())
    for segment in frequency:
        frequency[segment] = (frequency[segment] / total_segments) * 100
    
    return frequency

def map_frequencies(ciphertext_frequency, english_frequency):
    """Map ciphertext frequencies to the closest English letter frequencies."""
    sorted_ciphertext = sorted(ciphertext_frequency.items(), key=lambda item: item[1], reverse=True)
    sorted_english = sorted(english_frequency.items(), key=lambda item: item[1], reverse=True)
    
    mapping = {}
    for (ciphertext_segment, _), (english_letter, _) in zip(sorted_ciphertext, sorted_english):
        mapping[ciphertext_segment] = english_letter
    
    return mapping

def apply_mapping(segments, mapping):
    """Apply the frequency mapping to the segments to generate the plaintext."""
    plaintext = ''.join(mapping.get(segment, segment) for segment in segments)
    return plaintext

# Example usage
try:
    segments = extract_segments(ciphertext, key_mapping)
    print("extracted segments")
    ciphertext_frequency = frequency_analysis(segments)
    mapping = map_frequencies(ciphertext_frequency, english_frequency)
    refined_text = apply_mapping(segments, mapping)
    
    print("Refined text:", refined_text)
except ValueError as e:
    print("Error:", e)