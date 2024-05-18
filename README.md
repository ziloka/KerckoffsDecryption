## Notes
- [polyalphabetic substitution cipher](https://pi.math.cornell.edu/~mec/2003-2004/cryptography/polyalpha/polyalpha.html) variant
- [Kasiski examination](https://en.wikipedia.org/wiki/Kasiski_examination) is one way to crack type of ciphers
- [Kasiski examination implementation](https://github.com/ichantzaras/polysub-cryptanalysis/blob/master/kasiski.py#L39)
- https://crypto.stackexchange.com/a/1847
- this seems really similar to a modified version of [Vigenère cipher](https://en.wikipedia.org/wiki/Vigen%C3%A8re_cipher)
https://en.wikipedia.org/wiki/Vigen%C3%A8re_cipher#Cryptanalysis

useful tips for troubleshooting your code

use the following regular expression when searching through encrypted text
```
(?<=\D\B)\d+
```

https://www.geocaching.com/geocache/GC9NT53_kerckhoffs-part-1
get codewords
```bash
poetry run python -c "print(open('input/codewords.txt').read().strip().split('\n')[1::2])"
```

https://www.geocaching.com/geocache/GC9PAWZ_kerckhoffs-part-2
- https://github.com/ichantzaras/polysub-cryptanalysis
Run
```
python attack.py
```

<!-- - use a [word counter](https://wordcounter.net/character-count) to check if the frequencies from part1 are the same by using the part2 program to crack
- https://pypi.org/project/subbreaker/
- https://bionsgadgets.appspot.com/ww_forms/aristo_pat_web_worker3.html
- https://bionsgadgets.appspot.com/gadget_forms/solve_cipher_only.html
Calculate letter frequency, if letter frequency is not expected, eg A, E, and X are the most common letters by a small margin, shift  -->

https://www.geocaching.com/geocache/GC9PC6T_kerckhoffs-part-3

