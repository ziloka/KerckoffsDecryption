import sys
import string
import random
from collections import Counter
from timeit import default_timer as timer

seed = random.randrange(sys.maxsize)
random.seed(seed)

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
    pos = random.randint(1, min(len(key1), len(key2)))
    return key1[:pos] + key2[pos:]

def generate_initial_population(ciphertext, population_size, max_key_length):
    population = []
    for _ in range(population_size):
        key_length = random.randint(1, max_key_length)
        key = ''.join(random.choice(string.ascii_uppercase) for _ in range(key_length))
        decrypted = decrypt_autokey(ciphertext, key)
        text_freq = Counter(decrypted)
        chi_squared = chi_squared_statistic(text_freq, ENGLISH_FREQ, len(decrypted))
        population.append((key, chi_squared))
    return population

def genetic_algorithm(ciphertext, max_key_length, population_size, generations, mutation_rate):
    population = generate_initial_population(ciphertext, population_size, max_key_length)
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
        if generation % 50 == 0:
            mutation_rate *= 0.95

    return best_key

def crack_autokey(ciphertext, max_key_length=20, population_size=100, generations=500):
    best_key = genetic_algorithm(ciphertext, max_key_length, population_size, generations, 0.05)
    best_decrypted = decrypt_autokey(ciphertext, best_key)
    return best_decrypted, best_key

if __name__ == "__main__":
    # Example usage
    # key: password, has a chi squared value of 11.8
    ciphertext = "IHWKYVFREZJSEHRSHSXBWIOXBRGNUAPTTWIZENINPWCPONWBNVIFEKLMDSSHWGEMICLLGFDOGOELSTZRTTSIAQYKEKSMZSJUEKHMRRLIIFSIVRMOMOGEEHNUMXONULHGMIKNABUXXNYSTZLSUTAEE"
    start = timer()
    best_decrypted, best_key = crack_autokey(ciphertext, max_key_length=20, population_size=100, generations=500)
    print(f"Time taken: {(timer()-start)*1000:.2f}ms")
    print("seed: ", seed) # 1840704045573419828, 4098024409606275208, 2730598923906855722, 5218436368185893926, 961567004807804403
    print("Best Decrypted Text:", best_decrypted)
    print("Best Key:", best_key)
    print("Chi Squared:", chi_squared_statistic(Counter(best_decrypted), ENGLISH_FREQ, len(best_decrypted)))

    # key: passnord has a chi squared of 8.790756492927203

    # print()
    # plaintext = decrypt_autokey(ciphertext, "PASSWORD")
    # print("Plaintext:", plaintext)
    # print("Ciphertext:", ciphertext)
    # print("Key:", "PASSWORD")
    # print("Chi Squared:", chi_squared_statistic(Counter(plaintext), ENGLISH_FREQ, len(plaintext)))