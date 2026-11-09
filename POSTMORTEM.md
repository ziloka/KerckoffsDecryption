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

Part 3 removes both conveniences:

* the first digit no longer gives the codeword length,
* the last digit no longer gives the shift; every codeword has a secret shift.

Recovered codeword dictionary (`input/codewords_part3.txt`): 26 prefix-free
codewords that tile the entire ciphertext exactly.

The remaining key is a hidden permutation `tau` plus 26 hidden shifts `omega`:

```text
plaintext_i = (tau[c_i] + S_i) mod 26
S_{i+1}     = (S_i + omega[c_i]) mod 26
```

`src/part3.py` contains a solver that recovers `tau` and `omega` from a correct
plaintext crib of roughly 100 letters, then decrypts the whole message. It has
a `--selftest` that encrypts a known text with a random key and recovers it
exactly.

Status: the dictionary and solver are done; the plaintext is still blocked on
a correct crib. The obvious "swap and double" coordinate sentences have been
rejected by the key equations in every wording and offset tried, so the part 3
crib is still unknown.