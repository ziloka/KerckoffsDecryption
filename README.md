# General Notes
- [polyalphabetic substitution cipher](https://pi.math.cornell.edu/~mec/2003-2004/cryptography/polyalpha/polyalpha.html) variant, it is similar to the [Vigenère cipher](https://en.wikipedia.org/wiki/Vigen%C3%A8re_cipher)

## Things to think about the cipher
- study repetitions and near-repetitions in the ciphertext
- what will happen when a plaintext word is repeated, considering that the codewords shift each time that word is used?
- cipher might even show isomorphic sequences

https://www.geocaching.com/geocache/GC9NT53_kerckhoffs-part-1

https://www.geocaching.com/geocache/GC9PAWZ_kerckhoffs-part-2

## Cryptanalysis for part 2

> The first digit tells you how long the codeword is.
1. This part is huge and you can break up the text into codewords right from the start. 
2. the rest is solved more or less as an [autokey cipher key-autokey variant](https://en.wikipedia.org/wiki/Autokey_cipher), since the last digit of a codeword gives you the key for the next codeword

key "apple"
plaintext "ITISDURINGOURDARKESTMOMENTSTHATWEMUSTFOCUSTOSEETHELIGHT"
Use this website to encrypt autokey cipher
- https://crypto.interactive-maths.com/autokey-cipher.html

Use this to decrypt autokey cipher without key
- https://www.dcode.fr/autoclave-cipher

https://www.geocaching.com/geocache/GC9PC6T_kerckhoffs-part-3

