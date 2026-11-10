# Kerckhoffs Post-Mortem

## Part 1

The key is a fixed letter -> codeword table (`input/codewords.txt`). Each
codeword starts with its own length, and after every codeword the table is
shifted down by the last digit of that codeword (the shifts are cumulative).

Plaintext:

> THE CACHE IS LOCATED AT NORTH THIRTY NINE DEGREES TEN POINT FOUR EIGHT TWO
> YOULL ALSO NEED WEST SEVENTY SIX DEGREES FIFTY ONE POINT FOUR HUNDRED TWENTY
> TWO CACHE IS AB IS ON ON A FENCE

Final coordinates:

```text
N 39° 10.482  W 076° 51.422
```

Solver: `src/part1.py`.

## Part 2

### Cipher

Same mechanism as part 1, but the key is not published. The first digit still
gives the codeword length, so the ciphertext can be split into codewords
directly. The shift after each codeword is still the codeword's last digit, so
the cumulative shift before every codeword is known from the ciphertext alone.

If `pos(c)` is the codeword's position in the hidden table and `S_i` is the
cumulative shift before position `i`, then:

```text
plaintext_i = (pos(c_i) + S_i) mod 26
```

The only unknown is the 26-symbol table permutation. `src/part2.py` recovers it
with quadgram-scored simulated annealing over the 26! permutation space.

Decrypted message:

> CONGRATULATIONS YOU ARE A CRYPTOGRAPHER EXTRAORDINAIRE TO SOLVE SWAP AND
> DOUBLE THE LAST PARTS OF THE COORDS SORRY IF THIS IS CONFUSING I DIDNT WANT
> ANY NUMBERS OR CARDINAL DIRECTIONS TO BE PRESENT IN THE PLAINTEXT FOR USE AS
> CRIBS AT LEAST FOR THIS ONE THE CHECKER CAN HELP YOU VERIFY YOUR ANSWER THE
> CACHE IS AT THE WEIRD STUMP THIS IS OBVIOUSLY NOT REQUIRED BUT ID LOVE TO HEAR
> ABOUT YOUR SOLUTION METHOD

### The coordinate step

The instruction is applied to the **posted coordinates on the part 2 page**,
not to part 1's solved coordinates.

Posted coordinates:

```text
N 39° 10.227  W 076° 51.187
```

Take the last parts (the decimal minutes), swap them, then double them:

```text
N 39° 10.227  W 076° 51.187
            227 / 187
   swap  ->  187 / 227
  double ->  374 / 454

N 39° 10.374  W 076° 51.454
```

**Confirmed by the solution checker:**

```text
N 39° 10.374  W 076° 51.454
```

### The red herring

Applying the same swap/double to part 1's solved decimals (`482 / 422`) gives:

```text
N 39° 10.844  W 076° 51.964
```

That coordinate is rejected by the part 2 checker. This is the trap the finder
logs describe as "the beginning had a red herring start" and "the first solve
was heartbreakingly wrong". The operation only works on the part 2 **posted**
coordinates.

## Part 3

### Cipher

Part 3 removes both conveniences:

* the first digit no longer gives the codeword length,
* the last digit no longer gives the shift; every codeword has a secret shift.

The codeword dictionary (`input/codewords_part3.txt`) was recovered from the
ciphertext alone: 26 prefix-free codewords that tile all 3,377 digits with no
leftovers. The key is a hidden permutation `tau` plus 26 hidden shifts `omega`:

```text
plaintext_i = (tau[c_i] + S_i) mod 26
S_{i+1}     = (S_i + omega[c_i]) mod 26
```

`src/part3.py` recovers `tau` and `omega` from a correct plaintext crib of
roughly 100 letters and decrypts the whole message. Running it with no
arguments decrypts the solved ciphertext; `--key` prints the key, `--break`
re-runs the phrase search below, and `--selftest` verifies the solver on a
synthetic key.

### The crib

The part 3 hint block contains a fourth hint that made the break:

> [Puzzle 4] The two phrases `North Thirty Nine Degrees Ten Point` and
> `West Seventy Six Degrees Fifty One Point` both appear somewhere in the
> plaintext. No other assumptions about the plaintext need be made.

The part 2 hint ("only the seconds differ") only guarantees that the final
coordinate shares its degrees/minutes with the posted one. The fourth hint is
what gives exact plaintext: two verbatim phrases, with no assumption about
their order, adjacency, or connectors.

Together the phrases are 64 known letters, enough to overdetermine the
52-unknown key. They are **not** adjacent. A two-block search over all offset
pairs (flat-array Gaussian elimination over GF(2), ~300k pairs in about one
second) finds the unique pair that also survives modulo 13:

```text
NORTHTHIRTYNINEDEGREESTENPOINT      at symbol 46
WESTSEVENTYSIXDEGREESFIFTYONEPOINT  at symbol 114
```

That pair leaves a 6+6-dimensional solution space. Decrypting with the
particular solution (free variables set to zero) exposes the 38-letter gap:

```text
FIVEHUNDREDTHIRTEENINTHEOTHERDIRECTION
```

It is the latitude seconds (`FIVEHUNDREDTHIRTEEN` = 513) followed by the
connector `INTHEOTHERDIRECTION` - the part 3 wording, not part 1's
`YOULL ALSO NEED`. Adding the gap as a final crib pins the key:

```text
tau   = [9, 16, 15, 11, 2, 12, 23, 19, 10, 18, 5, 1, 0, 17, 25, 3, 24, 7, 13, 4, 22, 20, 8, 6, 21, 14]
omega = [17, 13, 5, 21, 21, 17, 2, 5, 17, 10, 4, 14, 0, 1, 11, 18, 14, 24, 1, 5, 1, 24, 11, 5, 18, 19]
```

The key is indexed by the line order of `input/codewords_part3.txt`.

### Plaintext

> WOW IM IMPRESSED. I THINK THIS PUZZLE IS PRETTY HARD. GO TO NORTH THIRTY
> NINE DEGREES TEN POINT FIVE HUNDRED THIRTEEN IN THE OTHER DIRECTION WEST
> SEVENTY SIX DEGREES FIFTY ONE POINT SIX EIGHT TWO. IM REALLY CURIOUS IF YOU
> CAN FIND A SOLUTION TO THIS GENERALIZATION THAT DOESNT RELY ON CRIBS. THE
> ONLY SOLUTION I FOUND USED THE WORD THE AS THE MOST COMMON TRIGRAM STARTING
> WITH EACH CODEWORD. EVEN THEN IT TOOK MILLIONS OF LETTERS, WASNT CONSISTENT,
> AND STILL NEEDED A LARGE EXHAUST. I REALLY THOUGHT I COULD USE THE FACT THAT
> THERE IS A STATISTICAL DIFFERENCE IN HOW FAR AWAY THE SECOND LETTER IS
> CIRCULARLY FROM THE FIRST IN ALL BIGRAMS REGARDLESS OF FIRST LETTER, BUT IT
> DIDNT WORK. CACHE IS MAYBE KNEE HIGH IN TREE.

Final coordinates:

```text
N 39° 10.513  W 076° 51.682
```

Verification: 579 letters, quadgram score 3119.0, `tau` is a 26-permutation,
and re-encrypting with the key reproduces the 3,377-digit ciphertext exactly.

### Coordinate step

Part 1 spells out its own final coordinate in the plaintext, and part 2's
"swap and double" applies only to part 2's posted coordinates. Part 3 follows
part 1: the plaintext gives the final coordinate directly. The part 2 hint
"only the seconds differ" is consistent - posted and final share the degrees
and minutes:

```text
posted  N 39° 10.177  W 076° 51.187
final   N 39° 10.513  W 076° 51.682
```

### What did not work

The author's own note in the plaintext describes the same dead ends this
repository went through: a crib-free attack using "THE" as the most common
trigram starting with a codeword took millions of letters, was inconsistent,
and still needed a large exhaustive search; the bigram letter-distance
statistic did not work either. The intended break is the crib route from the
hints.

`input/part3_solution.txt` records the key, crib, plaintext, and coordinates.