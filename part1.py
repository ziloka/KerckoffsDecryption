from src.crypto import decrypt

encrypted = open("part1.txt", "r").read()
codewords = open("codewords.txt", "r").read().splitlines()
# https://stackoverflow.com/a/12739974
codewordmap = {v: k for k, v in dict(zip(*[iter(codewords)]*2)).items()}

print(decrypt(encrypted, codewordmap))
