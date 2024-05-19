# General Notes
- [polyalphabetic substitution cipher](https://pi.math.cornell.edu/~mec/2003-2004/cryptography/polyalpha/polyalpha.html) variant
- [autokey cipher](https://en.wikipedia.org/wiki/Autokey_cipher)

https://www.geocaching.com/geocache/GC9NT53_kerckhoffs-part-1

https://www.geocaching.com/geocache/GC9PAWZ_kerckhoffs-part-2

## Cryptanalysis for part 2

> The first digit tells you how long the codeword is.
1. This part is huge and you can break up the text into codewords right from the start. 
2. the rest is solved more or less as an [autokey cipher](https://en.wikipedia.org/wiki/Autokey_cipher), since the last digit of a codeword gives you the key for the next codeword

### Things to think about the cipher
- study repetitions and near-repetitions in the ciphertext
- what will happen when a plaintext word is repeated, considering that the codewords shift each time that word is used?
- cipher might even show isomorphic sequences

https://www.geocaching.com/geocache/GC9PC6T_kerckhoffs-part-3

