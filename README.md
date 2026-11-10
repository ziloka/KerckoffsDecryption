# General Notes
- [polyalphabetic substitution cipher](https://pi.math.cornell.edu/~mec/2003-2004/cryptography/polyalpha/polyalpha.html) variant, it is similar to the [Vigenère cipher](https://en.wikipedia.org/wiki/Vigen%C3%A8re_cipher)
- https://crypto.stackexchange.com/questions/40119/how-to-solve-columnar-transposition-cipher-without-a-key
- https://github.com/CrypToolProject/CrypTool-2
- https://www.cryptool.org/en/ct2/
- [Autokey C# implementation](https://github.com/CrypToolProject/CrypTool-2/blob/af0b6f3ced981b85bb7b911a9a3eccf50a909677/CrypPlugins/VigenereAnalyzer/VigenereAnalyzer.cs#L240-L390)
- https://inventwithpython.com/cracking/chapter20.html

### Data collection
- https://norvig.com/mayzner.html
- https://storage.googleapis.com/books/ngrams/books/datasetsv3.html
- https://github.com/zehadialam/Vigenere-Cipher-Breaker
- http://practicalcryptography.com/cryptanalysis/text-characterisation/quadgrams/#a-python-implementation
- http://practicalcryptography.com/cryptanalysis/stochastic-searching/cryptanalysis-autokey-cipher/
- https://iq.opengenus.org/auto-key-cipher/

## Things to think about the cipher
- study repetitions and near-repetitions in the ciphertext
- what will happen when a plaintext word is repeated, considering that the codewords shift each time that word is used?
- cipher might even show isomorphic sequences

https://www.geocaching.com/geocache/GC9NT53_kerckhoffs-part-1

## Cryptanalysis for [Kerckhoffs part 2](https://www.geocaching.com/geocache/GC9PAWZ_kerckhoffs-part-2)

> The first digit tells you how long the codeword is.
1. This part is huge and you can break up the text into codewords right from the start. 
2. the rest is solved more or less as an [autokey (aka autoclave) cipher key-autokey variant](https://en.wikipedia.org/wiki/Autokey_cipher), since the last digit of a codeword gives you the key for the next codeword

<!-- https://discord.com/channels/645341027053600768/645341027053600771/1241561354544877588 -->

key "apple"

plaintext "IT IS DURING OUR DARKEST MOMENTS THAT WE MUST FOCUS TO SEE THE LIGHT"

Use this to decrypt autokey cipher without key
- https://www.dcode.fr/autoclave-cipher

Autoclave decryption method without key (pseudocode)
find length of key by testing different keylengths of keyword
for each letter maximaze probability text is plain through frequency analysis

Might be helpful for determine bigrams, trigrams, quadgrams (for frequency analysis)
https://gitlab.com/guballa/SubstitutionBreaker/-/blob/93dcc269efbfe6c62c3a93a6ce66077d6ff335fb/subbreaker/breaker.py#L321-380
solver cracks substitution ciphers through dicitionary of quadgrams

https://github.com/gibsjose/statistical-attack/tree/master

### [Kercekoffs part 3](https://www.geocaching.com/geocache/GC9PC6T_kerckhoffs-part-3)

Part 3 changes two rules:
- the first digit of a codeword no longer gives its length,
- the last digit no longer gives the shift; every codeword has a secret shift value.

The codeword dictionary was recovered from the ciphertext alone (see
`input/codewords_part3.txt`): 26 prefix-free codewords that tile all 3,377
digits with no leftovers and no prefix collisions. The cipher is then

```
plaintext_i = (tau[c_i] + S_i) mod 26
S_{i+1}     = (S_i + omega[c_i]) mod 26
```

with `tau` a hidden permutation of the 26 codewords and `omega` 26 hidden
shifts. `src/part3.py` contains the solver: it recovers `tau` and `omega` from
a correct ~100 letter plaintext crib by solving the induced linear system over
Z/2 and Z/13, enumerating the small remaining solution space, keeping the key
whose `tau` is a permutation, and decrypting the whole message. `--selftest`
encrypts a known text with a random key and recovers it exactly, and `--break`
re-runs the phrase search described below.

**Solved.** Hint 4 gives two exact phrases that both appear verbatim in the
plaintext:

```text
NORTH THIRTY NINE DEGREES TEN POINT
WEST SEVENTY SIX DEGREES FIFTY ONE POINT
```

They are not adjacent. Searching all offset pairs for joint consistency
locates them at symbols 46 and 114, with the gap
`FIVE HUNDRED THIRTEEN IN THE OTHER DIRECTION`. That crib pins the key, and
the plaintext gives the final coordinates:

```text
N 39° 10.513  W 076° 51.682
```

Run it:

```text
python src/part3.py            # decrypt and print the answer
python src/part3.py --key      # recovered tau and omega
python src/part3.py --break    # re-run the two-block phrase search
```

The full key, crib, plaintext, and coordinates are in
`input/part3_solution.txt`; `POSTMORTEM.md` has the full narrative.

