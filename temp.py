# from itertools import permutations

# def generate_permutations(data):
#     keys = list(data.keys())
#     values = list(data.values())
#     all_permutations = permutations(values)
    
#     result = []
#     for perm in all_permutations:
#         result.append(dict(zip(keys, perm)))
    
#     return result

# # Example usage
# data = {'7954481': 'A', '52123': 'B', '59207': 'C', '7699855': 'D', '652655': 'E', '945432286': 'F', '4045': 'G', '7906967': 'H', '605858': 'I', '920376451': 'J', '20': 'K', '338': 'L', '641971': 'M', '50461': 'N', '7811539': 'O', '89447709': 'P', '391': 'Q', '7756659': 'R', '55709': 'S', '7080686': 'T', '341': 'U', '308': 'V', '4530': 'W', '7614435': 'X', '7073281': 'Y', '21': 'Z'}
# permuted_dicts = generate_permutations(data)

# for perm_dict in permuted_dicts:
#     print(perm_dict)

import json
from itertools import permutations

def generate_permutations(data):
    keys = list(data.keys())
    values = list(data.values())
    all_permutations = permutations(values)
    
    file = open("part2_permutations.txt", "rw")
    for perm in all_permutations:
        file.write(json.dump(dict(zip(keys, perm))))
        file.write("\n")


# Example usage
data = {'7954481': 'A', '52123': 'B', '59207': 'C', '7699855': 'D', '652655': 'E', '945432286': 'F', '4045': 'G', '7906967': 'H', '605858': 'I', '920376451': 'J', '20': 'K', '338': 'L', '641971': 'M', '50461': 'N', '7811539': 'O', '89447709': 'P', '391': 'Q', '7756659': 'R', '55709': 'S', '7080686': 'T', '341': 'U', '308': 'V', '4530': 'W', '7614435': 'X', '7073281': 'Y', '21': 'Z'}
permuted_dicts = generate_permutations(data)

for perm_dict in permuted_dicts:
    print(perm_dict)