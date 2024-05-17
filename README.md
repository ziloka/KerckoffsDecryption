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
- use a [word counter](https://wordcounter.net/character-count) to check if the frequencies from part1 are the same by using the part2 program to crack
- 

https://www.geocaching.com/geocache/GC9PC6T_kerckhoffs-part-3

