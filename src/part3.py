"""Tools for breaking Kerckhoffs (part 3).

Part 3 removes the two "hand decryption" conveniences of parts 1 and 2:

* the first digit of a codeword no longer gives its length,
* the digit after a codeword no longer gives the table shift.

What remains is a prefix-free codeword dictionary, a hidden table permutation
``tau`` and 26 secret shifts ``omega``.  Decryption is::

    plaintext_i = (tau[c_i] + S_i) mod 26
    S_{i+1}     = (S_i + omega[c_i]) mod 26

The dictionary below was recovered directly from ``input/part3.txt``: it is a
prefix-free set of 26 codewords that tiles the entire ciphertext with no
leftovers, and is the only set of maximal repeated substrings that does so.

The remaining unknown is the key (tau, omega).  With a correct plaintext crib
of roughly 80-100 letters the linear system that relates plaintext differences
to the key becomes full rank, so a single correct crib is enough to recover the
whole key and decrypt the rest of the message.

Usage::

    python src/part3.py --selftest
    python src/part3.py "THE CACHE IS LOCATED AT NORTH ..."

No crib is supplied by default; this module is the finished tool that turns a
correct coordinate sentence (or any other correct ~100 letter crib) into the
full plaintext.
"""

import itertools
import math
import random
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from part2 import LETTERS, QUADGRAM_FILE, load_quadgram_scores  # noqa: E402

CODEWORD_FILE = REPO_ROOT / "input" / "codewords_part3.txt"
CIPHERTEXT_FILE = REPO_ROOT / "input" / "part3.txt"

ALPHABET_SIZE = 26
_SCORES: list[float] | None = None


def load_codewords(path: Path = CODEWORD_FILE) -> list[str]:
    return [
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def segment(ciphertext: str, codewords: list[str]) -> list[int]:
    """Split the ciphertext into codeword indices (prefix-free => unique)."""
    by_length = sorted(codewords, key=len, reverse=True)
    index = {codeword: i for i, codeword in enumerate(codewords)}
    symbols: list[int] = []
    position = 0
    while position < len(ciphertext):
        for codeword in by_length:
            if ciphertext.startswith(codeword, position):
                symbols.append(index[codeword])
                position += len(codeword)
                break
        else:
            raise ValueError(f"no codeword matches at offset {position}")
    return symbols


def check_prefix_free(codewords: list[str]) -> None:
    for a in codewords:
        for b in codewords:
            if a != b and b.startswith(a):
                raise ValueError(f"{a!r} is a prefix of {b!r}")


def get_scores() -> list[float]:
    global _SCORES
    if _SCORES is None:
        _SCORES = load_quadgram_scores(QUADGRAM_FILE)
    return _SCORES


def quadgram_index(letters: list[int], start: int) -> int:
    a, b, c, d = letters[start : start + 4]
    return a * 17576 + b * 676 + c * 26 + d


def score_text(text: str) -> float:
    scores = get_scores()
    letters = [ord(ch) - 65 for ch in text]
    return sum(
        scores[quadgram_index(letters, start)]
        for start in range(len(letters) - 3)
    )


def decrypt(symbols: list[int], tau: list[int], omega: list[int]) -> str:
    shift = 0
    out: list[str] = []
    for symbol in symbols:
        out.append(LETTERS[(tau[symbol] + shift) % ALPHABET_SIZE])
        shift = (shift + omega[symbol]) % ALPHABET_SIZE
    return "".join(out)


def _solve_mod(
    equations: list[tuple[dict[int, int], int]], n: int, p: int
) -> tuple[list[int], list[list[int]], int] | None:
    matrix: list[list[int]] = []
    for coeffs, rhs in equations:
        row = [0] * (n + 1)
        for var, value in coeffs.items():
            row[var] = (row[var] + value) % p
        row[n] = rhs % p
        matrix.append(row)

    row = 0
    pivots: list[int] = []
    for col in range(n):
        pivot = None
        for r in range(row, len(matrix)):
            if matrix[r][col] % p:
                pivot = r
                break
        if pivot is None:
            continue
        matrix[row], matrix[pivot] = matrix[pivot], matrix[row]
        inverse = pow(matrix[row][col], -1, p)
        matrix[row] = [(x * inverse) % p for x in matrix[row]]
        for r in range(len(matrix)):
            if r != row and matrix[r][col] % p:
                factor = matrix[r][col]
                matrix[r] = [
                    (matrix[r][c] - factor * matrix[row][c]) % p
                    for c in range(n + 1)
                ]
        pivots.append(col)
        row += 1

    for r in range(row, len(matrix)):
        if all(matrix[r][c] % p == 0 for c in range(n)) and matrix[r][n] % p:
            return None

    free = [c for c in range(n) if c not in pivots]
    particular = [0] * n
    for r, col in enumerate(pivots):
        particular[col] = matrix[r][n] % p
    basis: list[list[int]] = []
    for f in free:
        vector = [0] * n
        vector[f] = 1
        for r, col in enumerate(pivots):
            vector[col] = (-matrix[r][f]) % p
        basis.append(vector)
    return particular, basis, len(free)


def _enumerate(particular, basis, p):
    for combo in itertools.product(range(p), repeat=len(basis)):
        vector = particular[:]
        for coeff, base in zip(combo, basis):
            if coeff:
                for j in range(len(vector)):
                    vector[j] = (vector[j] + coeff * base[j]) % p
        yield vector


def solve_from_crib(
    ciphertext: str,
    codewords: list[str],
    plain_prefix: str,
    offset: int = 0,
    max_candidates: int = 500_000,
) -> tuple[list[tuple[float, str, list[int], list[int]]] | None, str]:
    """Recover the key from a correct plaintext crib and decrypt everything.

    Returns ``(results, info)`` where ``results`` is a list of
    ``(quadgram_score, plaintext, tau, omega)`` sorted best-first, or ``None``
    with a human-readable reason in ``info``.
    """
    symbols = segment(ciphertext, codewords)
    n = len(symbols)
    prefix = "".join(ch for ch in plain_prefix.upper() if ch.isalpha())
    m = len(prefix)
    if not prefix:
        return None, "empty crib"
    if offset < 0 or offset + m > n:
        return None, "crib does not fit in the ciphertext"
    values = [ord(ch) - 65 for ch in prefix]

    equations: list[tuple[dict[int, int], int]] = []
    for i in range(m - 1):
        a = symbols[offset + i]
        b = symbols[offset + i + 1]
        coeffs = {a + 26: 1}
        coeffs[a] = coeffs.get(a, 0) - 1
        coeffs[b] = coeffs.get(b, 0) + 1
        equations.append((coeffs, (values[i + 1] - values[i]) % 26))

    # Absolute equation: sum of the shifts before the crib plus tau(c_offset) = p0.
    coeffs = {}
    for j in range(offset):
        coeffs[symbols[j] + 26] = coeffs.get(symbols[j] + 26, 0) + 1
    coeffs[symbols[offset]] = coeffs.get(symbols[offset], 0) + 1
    equations.append((coeffs, values[0] % 26))

    solutions: dict[int, tuple[list[int], list[list[int]]]] = {}
    for p in (2, 13):
        result = _solve_mod(equations, 52, p)
        if result is None:
            return None, f"crib is inconsistent modulo {p}"
        particular, basis, free = result
        if p ** free > max_candidates:
            return None, f"solution space too large mod {p} (free={free})"
        solutions[p] = (particular, basis)

    results: list[tuple[float, str, list[int], list[int]]] = []
    for a in _enumerate(*solutions[2], 2):
        for b in _enumerate(*solutions[13], 13):
            key = [(13 * a[i] + 14 * b[i]) % 26 for i in range(52)]
            tau = key[:26]
            omega = key[26:]
            if len(set(tau)) != ALPHABET_SIZE:
                continue
            plaintext = decrypt(symbols, tau, omega)
            results.append((score_text(plaintext), plaintext, tau, omega))

    results.sort(key=lambda item: item[0], reverse=True)
    info = (
        f"free mod2={len(solutions[2][1])} free mod13={len(solutions[13][1])} "
        f"valid keys={len(results)}"
    )
    return results, info


def verify_roundtrip(
    plaintext: str, symbols: list[int], tau: list[int], omega: list[int]
) -> bool:
    inverse = [0] * ALPHABET_SIZE
    for symbol, position in enumerate(tau):
        inverse[position] = symbol
    shift = 0
    rebuilt: list[int] = []
    for ch in plaintext:
        letter = ord(ch) - 65
        symbol = inverse[(letter - shift) % ALPHABET_SIZE]
        rebuilt.append(symbol)
        shift = (shift + omega[symbol]) % ALPHABET_SIZE
    return rebuilt == symbols


def selftest() -> None:
    """Encrypt a known text with a random key and recover it from a crib."""
    rng = random.Random(20240612)
    tau = list(range(ALPHABET_SIZE))
    rng.shuffle(tau)
    omega = [rng.randrange(ALPHABET_SIZE) for _ in range(ALPHABET_SIZE)]
    plaintext = (
        "CONGRATULATIONSYOUAREACRYPTOGRAPHEREXTRAORDINAIRE"
        "TOSOLVESWAPANDDOUBLETHELASTPARTSOFTHECOORDS"
        "THISISATESTPLAINTEXTFORTHESELFTEST"
    )
    inverse = [0] * ALPHABET_SIZE
    for symbol, position in enumerate(tau):
        inverse[position] = symbol
    shift = 0
    symbols: list[int] = []
    for ch in plaintext:
        letter = ord(ch) - 65
        symbol = inverse[(letter - shift) % ALPHABET_SIZE]
        symbols.append(symbol)
        shift = (shift + omega[symbol]) % ALPHABET_SIZE

    codewords = load_codewords()
    check_prefix_free(codewords)
    ciphertext = "".join(codewords[symbol] for symbol in symbols)

    results, info = solve_from_crib(ciphertext, codewords, plaintext[:100])
    print(f"selftest: {info}")
    if results is None:
        raise SystemExit("selftest failed: could not solve")
    best_score, best_text, best_tau, best_omega = results[0]
    print(f"selftest: recovered {best_text[:60]}...")
    print(f"selftest: exact match = {best_text == plaintext}")
    print(
        "selftest: roundtrip = "
        f"{verify_roundtrip(best_text, symbols, best_tau, best_omega)}"
    )


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if "--selftest" in sys.argv:
        selftest()
        return

    codewords = load_codewords()
    check_prefix_free(codewords)
    ciphertext = CIPHERTEXT_FILE.read_text(encoding="utf-8").strip()
    symbols = segment(ciphertext, codewords)
    print(f"part 3: {len(codewords)} codewords, {len(symbols)} symbols")
    if not args:
        print(
            "No crib supplied.  Pass a correct ~100 letter plaintext crib:\n"
            '  python src/part3.py "THE CACHE IS LOCATED AT NORTH ..."'
        )
        return

    crib = " ".join(args)
    results, info = solve_from_crib(ciphertext, codewords, crib)
    print(info)
    if results is None:
        return
    for score, plaintext, _tau, _omega in results[:3]:
        print(f"score {score:.1f}: {plaintext}")


if __name__ == "__main__":
    main()
