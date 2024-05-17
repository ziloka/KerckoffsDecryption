from itertools import permutations

def generate_permutations(data):
    keys = list(data.keys())
    values = list(data.values())
    all_permutations = permutations(values)
    
    result = []
    for perm in all_permutations:
        result.append(dict(zip(keys, perm)))
    
    return result

# Example usage
data = {'7954481': 'A', '52123': 'B', '59207': 'C'}
permuted_dicts = generate_permutations(data)

for perm_dict in permuted_dicts:
    print(perm_dict)
