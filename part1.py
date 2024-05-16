from src.crypto import decrypt

encrypted = open("input/part1.txt", "r").read()
codewords = open("input/codewords.txt", "r").read().splitlines()
# https://stackoverflow.com/a/12739974
codewordmap = {v: k for k, v in dict(zip(*[iter(codewords)]*2)).items()}

print(decrypt(encrypted, codewordmap))
