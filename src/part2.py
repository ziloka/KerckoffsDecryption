import string
import sys
import logging
import random
from pathlib import Path
from collections import Counter
from timeit import default_timer as timer
from helper import utils, crypto
import math

# seed = random.randrange(sys.maxsize)
seed = 9126045727986561402
random.seed(seed)
print("seed: ", seed)

logger = logging.getLogger(Path(__file__).stem)
logger.setLevel('DEBUG')
filehandler_dbg = logging.FileHandler(logger.name + "-debug.log", mode='w')
filehandler_dbg.setLevel('DEBUG')
logger.addHandler(filehandler_dbg)

alphabet = list(string.ascii_uppercase)
FILENAME = "input/part1.txt"
ciphertext = open(FILENAME, "r", encoding='utf-8').read().strip()

necessary_words = {
    "THE": 3,
    "CACHE": 1,
    "NORTHTHIRTYNINEDEGREES": 1,
    "WESTSEVENTYSIXDEGREES": 1,
    "POINT": 2
}

def get_codewords(encrypted):
    start = 0
    codewords = set()
    while start < len(encrypted):
        length = int(encrypted[start])
        code = encrypted[start:start + length]
        codewords.add(code)
        start += length
    return list(codewords)

perf_start = timer()
codeword2letter = utils.dict_swap_keys_and_values(dict(zip(alphabet, get_codewords(ciphertext))))
print(f"It took {(timer()-perf_start)*1000:.2f}ms to get codewords.")

# https://stackoverflow.com/a/58869428/15332154
def derangement(keys):
    if len(keys) == 1:
        raise ValueError('No derangement is possible')

    new_keys = list(keys)

    while any(x == y for x, y in zip(keys, new_keys)):
        random.shuffle(new_keys)

    return new_keys

def shuffle_dict(d):
    return { x: d[y] for x, y in zip(d, derangement(d)) }

ENGLISH_FREQ = {
    'E': 12.02, 'T': 9.10, 'A': 8.12, 'O': 7.68, 'I': 7.31, 'N': 6.95, 'S': 6.28,
    'R': 6.02, 'H': 5.92, 'D': 4.32, 'L': 3.98, 'U': 2.88, 'C': 2.71, 'M': 2.61,
    'F': 2.30, 'Y': 2.11, 'W': 2.09, 'G': 2.03, 'P': 1.82, 'B': 1.49, 'V': 1.11,
    'K': 0.69, 'X': 0.17, 'Q': 0.11, 'J': 0.10, 'Z': 0.07
}

def chi_squared_statistic(text_freq: dict[str, str], text_length: int, text: str):
    chi_squared = 0.0
    for letter in ENGLISH_FREQ:
        observed = text_freq.get(letter, 0)
        expected = ENGLISH_FREQ[letter] * text_length / 100
        if expected > 0:  # Avoid division by zero
            chi_squared += (observed - expected) ** 2 / expected
    
    if not "TH" in text:
        return math.inf
    
    return chi_squared

def mutate_key(key: dict[str, str], mutation_rate: int, shuffle_elements=3):
    if not key or len(key) <= 1:
        return key  # No mutation if empty or single key dictionary

    # Create a new dictionary to avoid modifying the original
    mutated_dict = dict(key)

    # Choose a random key to swap
    key_to_mutate = random.choice(list(mutated_dict.keys()))

    # Mutate key with probability
    if random.random() < mutation_rate:
        # Choose another random key (excluding the chosen one)
        other_key = random.choice(list(mutated_dict.keys()))
        while other_key == key_to_mutate:
            other_key = random.choice(list(mutated_dict.keys()))

        # Swap key-value pairs
        mutated_dict[key_to_mutate], mutated_dict[other_key] = mutated_dict[other_key], mutated_dict[key_to_mutate]

    return mutated_dict

def crossover_keys(key1: dict[str, str], key2: dict[str, str]):
    common_keys = list(key1.keys())
    offspring = {}
    for key in common_keys:
        if random.random() < 0.5:
            offspring[key] = key1[key]
        else:
            offspring[key] = key2[key]
    return offspring

def generate_initial_population(codeword2letter: dict[str, str], population_size: int):
    population = []
    for _ in range(population_size):
        key = shuffle_dict(codeword2letter)
        decrypted = crypto.decrypt(ciphertext, key)
        text_freq = Counter(decrypted)
        chi_squared = chi_squared_statistic(text_freq, len(decrypted), decrypted)
        population.append((key, chi_squared))
    return population

def genetic_algorithm(ciphertext: str, codeword2letter: dict[str, str], population_size: int, generations: int, mutation_rate: int):
    population = generate_initial_population(codeword2letter, population_size)
    best_key, best_chi_squared = min(population, key=lambda x: x[1])

    for generation in range(generations):
        new_population = []
        elite = sorted(population, key=lambda x: x[1])[:population_size // 10]
        new_population.extend(elite)
        
        for _ in range(population_size - len(elite)):
            parent1, parent2 = random.sample(population, 2)
            child_key = crossover_keys(parent1[0], parent2[0])

            # old_keys = child_key.keys()

            # print(f"old key & child key remain the same {list(set(old_keys).difference(child_key))}\n")

            # mutate key actually mutates the key itself
            # child_key = mutate_key(child_key, mutation_rate)

            new_keys = child_key.keys()

            # differences = list(set(old_keys).difference(new_keys))
            # if len(differences) > 0:
            #     print(child_key)
            #     print(f"{differences}")
                

            decrypted = crypto.decrypt(ciphertext, child_key)
            text_freq = Counter(decrypted)
            chi_squared = chi_squared_statistic(text_freq, len(decrypted), decrypted)
            new_population.append((child_key, chi_squared))

        population = new_population
        current_best_key, current_best_chi_squared = min(population, key=lambda x: x[1])
        if current_best_chi_squared < best_chi_squared:
            print(f"best_chi_squared: {best_chi_squared}")
            best_key, best_chi_squared = current_best_key, current_best_chi_squared
        
        # Adaptive mutation rate
        if generation % 50 == 0:
            mutation_rate *= 0.95

    return best_key

def crack_autokey(ciphertext: str, codeword2letter: dict[str, str], population_size: int=100, generations: int=500):
    best_key = genetic_algorithm(ciphertext, codeword2letter, population_size, generations, 0.05)
    best_decrypted = crypto.decrypt(ciphertext, best_key)
    return best_decrypted, best_key

if __name__ == "__main__":
    start = timer()
    best_decrypted, best_key = crack_autokey(ciphertext, codeword2letter)
    print(f"Time taken: {(timer()-start)*1000:.2f}ms")

    print("Best Decrypted Text:", best_decrypted)
    print("Best Key:", best_key)
    print("Chi Squared:", chi_squared_statistic(Counter(best_decrypted), len(best_decrypted), best_decrypted))
