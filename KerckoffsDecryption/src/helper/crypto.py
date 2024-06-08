import helper.utils as utils

def encrypt(plaintext: str, letter2codeword: dict[str, str]):
    letter2codeword = letter2codeword.copy()
    encrypted = ""
    for letter in plaintext:
        code = letter2codeword[letter]
        encrypted += code
        letter2codeword = utils.dict_shift_values(letter2codeword, int(code[-1]))
    return encrypted

def decrypt(encrypted: str, codeword2letter: dict[str, str]):
    codeword2letter = codeword2letter.copy()
    plaintext = ""
    start = 0
    while start < len(encrypted):
        length = int(encrypted[start])
        code = encrypted[start:start + length]
        plaintext += codeword2letter[code]
        codeword2letter = utils.dict_shift_keys(codeword2letter, int(code[-1]))
        start += length
    return plaintext

def caesar_cipher(text, shift):
    result = []

    for char in text:
        if char.isalpha():
            # Determine if the character is uppercase or lowercase
            offset = 65 if char.isupper() else 97
            # Shift character and wrap around the alphabet
            new_char = chr((ord(char) + shift - offset) % 26 + offset)
            result.append(new_char)
        else:
            # Non-alphabetical characters are added without change
            result.append(char)

    return ''.join(result)