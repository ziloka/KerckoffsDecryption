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
QUADGRAM_BASE2 = ALPHABET_SIZE ** 2
QUADGRAM_BASE3 = ALPHABET_SIZE


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
    # Direct indexing avoids allocating a four-element slice in the hot loop.
    return (
        letters[start] * QUADGRAM_BASE
        + letters[start + 1] * QUADGRAM_BASE2
        + letters[start + 2] * QUADGRAM_BASE3
        + letters[start + 3]
    )


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


def build_move_tables(
    symbols: list[int], n_quadgrams: int
) -> tuple[list[list[list[int]]], list[list[list[int]]]]:
    """Precompute what a swap of two symbols affects.

    Swapping the permutation entries for symbols ``a`` and ``b`` only changes
    positions whose codeword is ``a`` or ``b``, and only quadgrams that
    overlap one of those positions.  Building an inverted index once turns
    every annealing step from an O(len(symbols)) scan into an O(affected)
    lookup.
    """
    positions_per_symbol: list[list[int]] = [[] for _ in range(ALPHABET_SIZE)]
    for i, symbol in enumerate(symbols):
        positions_per_symbol[symbol].append(i)

    starts_per_symbol: list[list[int]] = []
    for symbol in range(ALPHABET_SIZE):
        starts: set[int] = set()
        for i in positions_per_symbol[symbol]:
            for start in range(max(0, i - 3), min(n_quadgrams, i + 1)):
                starts.add(start)
        starts_per_symbol.append(sorted(starts))

    def merge(first: list[int], second: list[int]) -> list[int]:
        merged: list[int] = []
        i = j = 0
        while i < len(first) and j < len(second):
            if first[i] < second[j]:
                merged.append(first[i])
                i += 1
            elif first[i] > second[j]:
                merged.append(second[j])
                j += 1
            else:
                merged.append(first[i])
                i += 1
                j += 1
        merged.extend(first[i:])
        merged.extend(second[j:])
        return merged

    positions_table = [
        [[] for _ in range(ALPHABET_SIZE)] for _ in range(ALPHABET_SIZE)
    ]
    starts_table = [
        [[] for _ in range(ALPHABET_SIZE)] for _ in range(ALPHABET_SIZE)
    ]
    for a in range(ALPHABET_SIZE):
        for b in range(a + 1, ALPHABET_SIZE):
            merged_positions = merge(
                positions_per_symbol[a], positions_per_symbol[b]
            )
            merged_starts = merge(starts_per_symbol[a], starts_per_symbol[b])
            positions_table[a][b] = positions_table[b][a] = merged_positions
            starts_table[a][b] = starts_table[b][a] = merged_starts
    return positions_table, starts_table


def anneal(
    symbols: list[int],
    shifts: list[int],
    scores: list[float],
    *,
    seed: int = 0,
    iterations: int = 15_000,
    start_temperature: float = 5.0,
    end_temperature: float = 0.05,
    patience: int = 1000,
    move_tables: tuple[list[list[list[int]]], list[list[list[int]]]] | None = None,
) -> tuple[list[int], float]:
    """Simulated annealing over the 26! table permutation.

    ``iterations`` is an upper bound.  If the best score has not improved for
    ``patience`` consecutive steps the run stops early, which cuts the default
    work by roughly an order of magnitude on the actual ciphertext.  Pass
    ``patience=0`` to disable early stopping.
    """
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
    best_step = 0

    if len(indices) < 4:
        return best_permutation, best_score

    if move_tables is None:
        move_tables = build_move_tables(symbols, len(indices))
    positions_table, starts_table = move_tables
    qindex = quadgram_index
    exp = math.exp

    for step in range(iterations):
        temperature = start_temperature * (
            end_temperature / start_temperature
        ) ** (step / iterations)

        a, b = rng.sample(range(ALPHABET_SIZE), 2)
        affected_positions = positions_table[a][b]
        affected_starts = starts_table[a][b]

        permutation[a], permutation[b] = permutation[b], permutation[a]
        for i in affected_positions:
            plaintext[i] = (
                permutation[symbols[i]] + shifts[i]
            ) % ALPHABET_SIZE

        new_score = current
        for i in affected_starts:
            new_score += scores[qindex(plaintext, i)] - scores[indices[i]]

        delta = new_score - current
        if delta >= 0 or rng.random() < exp(delta / temperature):
            current = new_score
            for i in affected_starts:
                indices[i] = qindex(plaintext, i)
            if current > best_score:
                best_score = current
                best_permutation = permutation[:]
                best_step = step
        else:
            permutation[a], permutation[b] = permutation[b], permutation[a]
            for i in affected_positions:
                plaintext[i] = (
                    permutation[symbols[i]] + shifts[i]
                ) % ALPHABET_SIZE

        if patience and step - best_step >= patience:
            break

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
    move_tables = build_move_tables(symbols, len(symbols) - 3)

    best_permutation: list[int] | None = None
    best_score = float("-inf")
    for seed in range(4):
        permutation, score = anneal(
            symbols,
            shifts,
            scores,
            seed=seed,
            iterations=15_000,
            move_tables=move_tables,
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
