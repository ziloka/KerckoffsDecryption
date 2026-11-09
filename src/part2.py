"""Break Kerckhoffs part 2.

Cipher recap
------------
* The key is a 26-letter substitution: each plaintext letter maps to one unique
  codeword.  The first digit of a codeword is its length, so the ciphertext can
  be split into codewords without knowing the key.
* After every codeword is used, the whole codeword table is rotated down by the
  last digit of that codeword.  The shift is cumulative.

Why the old approach failed
---------------------------
The old code tried to *mutate a guessed letter -> codeword table while reading*
the ciphertext.  That is the wrong model: the shift applied to the table is
already known from the ciphertext (the last digit of every codeword), so it
should be applied to the plaintext side, not to a guessed mapping.

The correct model
-----------------
Let c_i be the codeword used at position i, let pos(c_i) be its position in the
original table (a permutation of 0..25), and let S_i be the cumulative shift
before position i.  Then:

        plaintext_i = (pos(c_i) + S_i) mod 26

S_i is known from the ciphertext.  The only unknown is the permutation pos, so
this is a 26! search that can be solved very reliably with simulated annealing
on a quadgram language model.

Run from the repository root:
    python src/part2.py
"""

import math
import random
import string
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CIPHERTEXT_FILE = REPO_ROOT / "input" / "part2.txt"
QUADGRAM_FILE = REPO_ROOT / "assets" / "quadgrams.txt"

LETTERS = string.ascii_uppercase
ALPHABET_SIZE = len(LETTERS)
QUADGRAM_BASE = ALPHABET_SIZE ** 3


def load_codewords(ciphertext: str) -> list[str]:
    """Split the ciphertext using the first digit of each codeword."""
    codewords: list[str] = []
    start = 0
    while start < len(ciphertext):
        length = int(ciphertext[start])
        if length <= 0:
            raise ValueError(f"invalid codeword length at offset {start}")
        codewords.append(ciphertext[start : start + length])
        start += length
    return codewords


def cumulative_shifts(codewords: list[str]) -> list[int]:
    """Cumulative table shift before each codeword."""
    shifts: list[int] = []
    shift = 0
    for codeword in codewords:
        shifts.append(shift)
        shift = (shift + int(codeword[-1])) % ALPHABET_SIZE
    return shifts


def load_quadgram_scores(path: Path) -> list[float]:
    """Return a log10 score indexed by a*26^3 + b*26^2 + c*26 + d."""
    scores: list[float | None] = [None] * (ALPHABET_SIZE ** 4)
    smallest = float("inf")
    with open(path, "r", encoding="utf-8") as handle:
        for line in handle:
            quadgram, count = line.split()
            if len(quadgram) != 4:
                continue
            count = int(count)
            smallest = min(smallest, count)
            index = (
                (ord(quadgram[0]) - 65) * QUADGRAM_BASE
                + (ord(quadgram[1]) - 65) * 26 * 26
                + (ord(quadgram[2]) - 65) * 26
                + (ord(quadgram[3]) - 65)
            )
            scores[index] = math.log10(count)
    # A quadgram that never occurs in the corpus should still be penalised,
    # but not so heavily that a single bad quadgram can never be repaired.
    floor = math.log10(smallest * 0.01)
    return [floor if value is None else value for value in scores]


def quadgram_index(letters: list[int], start: int) -> int:
    a, b, c, d = letters[start : start + 4]
    return a * QUADGRAM_BASE + b * 26 * 26 + c * 26 + d


def quadgram_indices(letters: list[int]) -> list[int]:
    return [
        quadgram_index(letters, start)
        for start in range(len(letters) - 3)
    ]


def decode(
    symbols: list[int], shifts: list[int], permutation: list[int]
) -> str:
    return "".join(
        LETTERS[(permutation[symbol] + shift) % ALPHABET_SIZE]
        for symbol, shift in zip(symbols, shifts)
    )


def score_text(plaintext: str, scores: list[float]) -> float:
    letters = [ord(letter) - 65 for letter in plaintext]
    return sum(scores[index] for index in quadgram_indices(letters))


def anneal(
    symbols: list[int],
    shifts: list[int],
    scores: list[float],
    *,
    seed: int = 0,
    iterations: int = 15_000,
    start_temperature: float = 5.0,
    end_temperature: float = 0.05,
) -> tuple[list[int], float]:
    """Simulated annealing over the 26! table permutation."""
    rng = random.Random(seed)
    permutation = list(range(ALPHABET_SIZE))
    rng.shuffle(permutation)

    plaintext = [
        (permutation[symbol] + shift) % ALPHABET_SIZE
        for symbol, shift in zip(symbols, shifts)
    ]
    indices = quadgram_indices(plaintext)
    current = sum(scores[index] for index in indices)
    best_permutation = permutation[:]
    best_score = current

    if len(indices) < 4:
        return best_permutation, best_score

    for step in range(iterations):
        temperature = start_temperature * (
            end_temperature / start_temperature
        ) ** (step / iterations)

        a, b = rng.sample(range(ALPHABET_SIZE), 2)
        permutation[a], permutation[b] = permutation[b], permutation[a]

        # Every position whose plaintext letter changed, and every quadgram
        # that overlaps one of those positions.
        affected_positions = {
            i for i, symbol in enumerate(symbols) if symbol in (a, b)
        }
        affected_starts: set[int] = set()
        for i in affected_positions:
            first = max(0, i - 3)
            last = min(len(indices) - 1, i)
            affected_starts.update(range(first, last + 1))

        for i in affected_positions:
            plaintext[i] = (
                permutation[symbols[i]] + shifts[i]
            ) % ALPHABET_SIZE

        new_score = current
        for i in affected_starts:
            new_score += (
                scores[quadgram_index(plaintext, i)] - scores[indices[i]]
            )

        delta = new_score - current
        if delta >= 0 or rng.random() < math.exp(delta / temperature):
            current = new_score
            for i in affected_starts:
                indices[i] = quadgram_index(plaintext, i)
            if current > best_score:
                best_score = current
                best_permutation = permutation[:]
        else:
            permutation[a], permutation[b] = permutation[b], permutation[a]
            for i in affected_positions:
                plaintext[i] = (
                    permutation[symbols[i]] + shifts[i]
                ) % ALPHABET_SIZE

    return best_permutation, best_score


def main() -> None:
    ciphertext = CIPHERTEXT_FILE.read_text(encoding="utf-8").strip()
    codewords = load_codewords(ciphertext)
    shifts = cumulative_shifts(codewords)

    unique_codewords = sorted(set(codewords))
    codeword_index = {
        codeword: index for index, codeword in enumerate(unique_codewords)
    }
    symbols = [codeword_index[codeword] for codeword in codewords]

    scores = load_quadgram_scores(QUADGRAM_FILE)

    best_permutation: list[int] | None = None
    best_score = float("-inf")
    for seed in range(4):
        permutation, score = anneal(
            symbols, shifts, scores, seed=seed, iterations=15_000
        )
        print(f"seed {seed}: quadgram score {score:.1f}")
        if score > best_score:
            best_score = score
            best_permutation = permutation

    assert best_permutation is not None
    plaintext = decode(symbols, shifts, best_permutation)

    # Round-trip check: re-encrypting must reproduce the original ciphertext.
    inverse = [0] * ALPHABET_SIZE
    for symbol, position in enumerate(best_permutation):
        inverse[position] = symbol
    rebuilt = "".join(
        unique_codewords[inverse[(ord(letter) - 65 - shift) % ALPHABET_SIZE]]
        for letter, shift in zip(plaintext, shifts)
    )
    assert rebuilt == ciphertext, "recovered table does not re-encrypt correctly"

    print(f"best quadgram score: {best_score:.1f}")
    print(plaintext)


if __name__ == "__main__":
    main()
