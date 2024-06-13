# this is an autokey where the key is given by the last digit of the codeword
# this means it is a ciphertext-autokey, the less common kind
# it says that after each codeword is produced, the alphabet table is shifted by an amount equal to the last digit
# so when you go to encipher the third codeword, the alphabet table has previously been shifted by the last digit of the first codeword plus the last digit of the second codeword. so for each codeword you know the total shift that was applied to the alphabet at that point
# for example here are the first several codewords together with the shift that was used for each codeword. you can assume the shift for the first codeword is zero because the rest of the solution will be the same no matter the initial shift.

import math
import string
from helper import crypto, utils

alphabet = list(string.ascii_uppercase)
FILENAME = "input/part1.txt"
ciphertext = open(FILENAME, "r", encoding='utf-8').read().strip()

ASCII_CODE_a = 97
ASCII_CODE_A = 65

def get_codewords(encrypted: str) -> set[str]:
    start = 0
    codewords = list()
    while start < len(encrypted):
        length = int(encrypted[start])
        code = encrypted[start:start + length]
        codewords.append(code)
        start += length
    return codewords

def main():
    codewords = get_codewords(ciphertext)
    unique_codewords = sorted(set(codewords))
    bigrams = {}
    for s in open("assets/english-bigrams.txt", encoding='utf-8').read().strip().split("\n"):
        bigram, score = s.split(" ")
        bigrams[bigram] = math.log(int(score))

    def get_text_score(text: str):
        text = text.upper().translate(str.maketrans('', '', string.punctuation))
        score = 0
        for word in text.split(" "):
            for idx in range(len(word) - 1):
                bigram = word[idx : idx + 2]
                score += 0 if bigram not in bigrams else bigrams[bigram]
        return score

    ALPHABET = [*string.ascii_uppercase]
    WINDOW_SIZE = 2
    i = 0
    shift = 0
    mapping = {letter: None for letter in ALPHABET}
    while i < len(codewords) - WINDOW_SIZE + 1:
        codeword1, codeword2 = codewords[i: i + WINDOW_SIZE]
        for bigram in bigrams:
            letter1, letter2 = [*bigram]

            if mapping[letter1] is None:
                mapping[letter1] = codeword1
                print(f"[{letter1} {codeword1[-1]}]")
                mapping = utils.dict_shift_values(mapping, int(codeword1[-1]))
                break

            if mapping[codeword2] is None:
                mapping[codeword2] = letter2
                print(f"{codeword2} {codeword2[-1]} old mapping: {mapping}")
                mapping = utils.dict_shift_values(mapping, int(codeword2[-1]))
                print(f"new mapping: {mapping}\n")
                break
        assert [*set(mapping.values())] == len(mapping)
        shift %= len(string.ascii_uppercase)
        i += 1
    plaintext = crypto.decrypt(ciphertext, mapping)
    print(mapping)
    print(plaintext)
    print(get_text_score(plaintext))

if __name__ == "__main__":
    main()