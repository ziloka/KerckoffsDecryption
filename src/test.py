from helper import crypto, utils

letter2codeword = {
    "A": "26",
    "B": "29",
    "C": "27",
    "D": "20",
    "E": "28",
    "F": "21"
}

codeword2letter = utils.dict_swap_keys_and_values(letter2codeword)

text = "ABCDEF"
ciphertext = crypto.encrypt(text, letter2codeword)
print(ciphertext)
plaintext = crypto.decrypt(ciphertext, codeword2letter)
print(plaintext)