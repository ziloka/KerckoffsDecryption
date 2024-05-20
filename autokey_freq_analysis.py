import string
import random
from collections import Counter
from timeit import default_timer as timer
import math
from multiprocessing import Pool, cpu_count, freeze_support

# Frequency of English letters
ENGLISH_FREQ = {
    'E': 12.02, 'T': 9.10, 'A': 8.12, 'O': 7.68, 'I': 7.31, 'N': 6.95, 'S': 6.28,
    'R': 6.02, 'H': 5.92, 'D': 4.32, 'L': 3.98, 'U': 2.88, 'C': 2.71, 'M': 2.61,
    'F': 2.30, 'Y': 2.11, 'W': 2.09, 'G': 2.03, 'P': 1.82, 'B': 1.49, 'V': 1.11,
    'K': 0.69, 'X': 0.17, 'Q': 0.11, 'J': 0.10, 'Z': 0.07
}

# Function to get the chi-squared statistic
def chi_squared_statistic(text_freq, english_freq, text_length):
    chi_squared = 0.0
    for letter in english_freq:
        observed = text_freq.get(letter, 0)
        expected = english_freq[letter] * text_length / 100
        if expected > 0:  # Avoid division by zero
            chi_squared += (observed - expected) ** 2 / expected
    return chi_squared

# Function to decrypt using a given key
def decrypt_autokey(ciphertext, key):
    decrypted = ""
    extended_key = key.upper()
    for i, char in enumerate(ciphertext):
        if char in string.ascii_uppercase:
            shift_amount = ord(extended_key[i]) - ord('A')
            decrypted += chr((ord(char) - ord('A') - shift_amount) % 26 + ord('A'))
            extended_key += decrypted[-1]
        else:
            decrypted += char
            extended_key += char
    return decrypted

# Genetic Algorithm functions
def mutate_key(key, mutation_rate):
    key_list = list(key)
    for i in range(len(key_list)):
        if random.random() < mutation_rate:
            new_char = chr(random.randint(ord('A'), ord('Z')))
            key_list[i] = new_char
    return ''.join(key_list)

def crossover_keys(key1, key2):
    pos = random.randint(1, len(key1) - 1)
    return key1[:pos] + key2[pos:]

def generate_initial_population(ciphertext, population_size, key_length):
    population = []
    for _ in range(population_size):
        key = ''.join(random.choice(string.ascii_uppercase) for _ in range(key_length))
        decrypted = decrypt_autokey(ciphertext, key)
        text_freq = Counter(decrypted)
        chi_squared = chi_squared_statistic(text_freq, ENGLISH_FREQ, len(decrypted))
        population.append((key, chi_squared))
    return population

def genetic_algorithm(ciphertext, key_length, population_size, generations, mutation_rate):
    population = generate_initial_population(ciphertext, population_size, key_length)
    best_key, best_chi_squared = min(population, key=lambda x: x[1])

    for generation in range(generations):
        new_population = []
        elite = sorted(population, key=lambda x: x[1])[:population_size // 10]
        new_population.extend(elite)
        
        for _ in range(population_size - len(elite)):
            parent1, parent2 = random.sample(population, 2)
            child_key = crossover_keys(parent1[0], parent2[0])
            child_key = mutate_key(child_key, mutation_rate)
            decrypted = decrypt_autokey(ciphertext, child_key)
            text_freq = Counter(decrypted)
            chi_squared = chi_squared_statistic(text_freq, ENGLISH_FREQ, len(decrypted))
            new_population.append((child_key, chi_squared))
        
        population = new_population
        current_best_key, current_best_chi_squared = min(population, key=lambda x: x[1])
        if current_best_chi_squared < best_chi_squared:
            best_key, best_chi_squared = current_best_key, current_best_chi_squared
        
        # Adaptive mutation rate
        mutation_rate = max(0.01, mutation_rate * 0.95 if generation % 50 == 0 else mutation_rate)

    return best_key

def parallel_genetic_algorithm(ciphertext, max_key_length, population_size, generations, mutation_rate, num_processes):
    with Pool(num_processes) as pool:
        key_lengths = [max_key_length] * num_processes
        results = pool.starmap(genetic_algorithm, [(ciphertext, kl, population_size, generations, mutation_rate) for kl in key_lengths])
    best_key = min(results, key=lambda key: chi_squared_statistic(Counter(decrypt_autokey(ciphertext, key)), ENGLISH_FREQ, len(ciphertext)))
    return best_key

def crack_autokey(ciphertext, max_key_length=20, population_size=500, generations=1000):
    num_processes = cpu_count()
    best_key = parallel_genetic_algorithm(ciphertext, max_key_length, population_size, generations, 0.05, num_processes)
    best_decrypted = decrypt_autokey(ciphertext, best_key)
    return best_decrypted, best_key


if __name__ == "__main__":
    freeze_support()
    # Example usage
    # key is password
    ciphertext = "IHWKYVFREZJSEHRSHSXBWIOXBRGNUAPTTWIZENINPWCPONWBNVIFEKLMDSSHWGEMICLLGFDOGOELSTZRTTSIAQYKEKSMZSJUEKHMRRLIIFSIVRMOMOGEEHNUMXONULHGMIKNABUXXNYSTZLSUTAEE"
    start = timer()
    best_decrypted, best_key = crack_autokey(ciphertext)
    print(f"took {(timer()-start)*1000:.2f}ms")
    print("Best Decrypted Text:", best_decrypted)
    print("Chi squared statistic:", chi_squared_statistic(Counter(best_decrypted), ENGLISH_FREQ, len(best_decrypted)))
    print("Best Key:", best_key)

    print()
    plaintext = decrypt_autokey(ciphertext, "PASSWORD")
    print("actual answer: ", plaintext)
    print("Chi squared statistic:", chi_squared_statistic(Counter(plaintext), ENGLISH_FREQ, len(plaintext)))