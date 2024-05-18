# https://github.com/ichantzaras/polysub-cryptanalysis/blob/290a8bf48f6998333aed260855760a427c3f6145/freq_analysis.py

import helper.polysub.processing as processing
import string
# from const import EN_REL_FREQ

SEQ_LEN = 7
MAX_KEY_LEN = 8
EN_IC = 0.67
EN_REL_FREQ = {'A': 0.08167, 'B': 0.01492, 'C': 0.02782, 'D': 0.04253, 'E': 0.12702, 'F': 0.02228, 'G': 0.02015,
               'H': 0.06094, 'I': 0.06966, 'J': 0.00153, 'K': 0.00772, 'L': 0.04025, 'M': 0.02406, 'N': 0.06749,
               'O': 0.07507, 'P': 0.01929, 'Q': 0.00095, 'R': 0.05987, 'S': 0.06327, 'T': 0.09056, 'U': 0.02758,
               'V': 0.00978, 'W': 0.02360, 'X': 0.00150, 'Y': 0.01974, 'Z': 0.00074}

def get_letter_counts(text):
    text_upper = text.upper()
    letter_counts = {}
    for index, letter in enumerate(string.ascii_uppercase):
        letter_counts[letter] = text_upper.count(letter)
    return letter_counts

def _get_letter_frequencies(text):
    letter_counts = get_letter_counts(text)
    frequencies = {letter: count/len(text) for letter, count in letter_counts.items()}
    return frequencies

def shift(text, amount):
    shifted = ''
    letters = string.ascii_uppercase
    for letter in text:
        shifted += letters[(letters.index(letter)-amount) % len(letters)]
    return shifted

def _corr(text, lf):
    return sum([(lf[letter]*EN_REL_FREQ[letter]) for letter in text])

def _find_key_letter(text, lf):
    key_letter = ''
    max_corr = 0
    for count, letter in enumerate(string.ascii_uppercase):
        shifted = shift(text=text, amount=count)
        corr = _corr(text=shifted, lf=lf)
        if corr > max_corr:
            max_corr = corr
            key_letter = letter
    return key_letter


def restore_key(cyphertext, key_len):
    key = ''
    blocks = processing.get_blocks(text=cyphertext, size=key_len)
    columns = processing.get_columns(blocks)
    frequencies = _get_letter_frequencies(text=cyphertext)
    for column in columns:
        key += _find_key_letter(text=column, lf=frequencies)
    return key