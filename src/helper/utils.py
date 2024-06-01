import itertools
from collections import deque

ENGLISH_FREQ = {
    'E': 12.02, 'T': 9.10, 'A': 8.12, 'O': 7.68, 'I': 7.31, 'N': 6.95, 'S': 6.28,
    'R': 6.02, 'H': 5.92, 'D': 4.32, 'L': 3.98, 'U': 2.88, 'C': 2.71, 'M': 2.61,
    'F': 2.30, 'Y': 2.11, 'W': 2.09, 'G': 2.03, 'P': 1.82, 'B': 1.49, 'V': 1.11,
    'K': 0.69, 'X': 0.17, 'Q': 0.11, 'J': 0.10, 'Z': 0.07
}

def chi_squared_statistic(text_freq: dict[str, str], text_length: int):
    chi_squared = 0.0
    for letter in ENGLISH_FREQ:
        observed = text_freq.get(letter, 0)
        expected = ENGLISH_FREQ[letter] * text_length / 100
        if expected > 0:  # Avoid division by zero
            chi_squared += (observed - expected) ** 2 / expected
    return chi_squared

# https://stackoverflow.com/a/40389411
def dict_format_table(myDict, colList=None):
   """ Pretty print a list of dictionaries (myDict) as a dynamically sized table.
   If column names (colList) aren't specified, they will show in random order.
   Author: Thierry Husson - Use it as you want but don't blame me.
   """
   if not colList: colList = list(myDict[0].keys() if myDict else [])
   myList = [colList] # 1st row = header
   for item in myDict: myList.append([str(item[col] if item[col] is not None else '') for col in colList])
   colSize = [max(map(len,col)) for col in zip(*myList)]
   formatStr = ' | '.join(["{{:<{}}}".format(i) for i in colSize])
   myList.insert(1, ['-' * i for i in colSize]) # Seperating line
   return "\n".join([formatStr.format(*item) for item in myList])

# https://stackoverflow.com/a/33938783
def find_in_list_of_list(mylist, char):
    for sub_list in mylist:
        if char in sub_list:
            return (mylist.index(sub_list), sub_list.index(char))
    return -1

def list_shift_column(matrix, col_idx, num_shifts):
    if not matrix or col_idx < 0 or col_idx >= len(matrix[0]):
        raise Exception("Column index is out of range")
        
    num_rows = len(matrix)
    num_shifts = num_shifts % num_rows  # Normalize the number of shifts
    
    if num_shifts == 0:
        return matrix  # No need to shift if the number of shifts is a multiple of the number of rows
    
    # Temporary list to store the values that will be wrapped around
    temp = [matrix[i][col_idx] for i in range(num_rows - num_shifts, num_rows)]
    
    # Shift elements in the specified column upwards
    for i in range(num_rows - 1, num_shifts - 1, -1):
        matrix[i][col_idx] = matrix[i - num_shifts][col_idx]
    
    # Place the stored values into the first rows
    for i in range(num_shifts):
        matrix[i][col_idx] = temp[i]

# https://stackoverflow.com/a/12739974
def list_2_dict(l):
    return dict(itertools.zip_longest(*[iter(l)] * 2, fillvalue=""))

def list_duplicates(l):
    seen = set()
    dupes = []
    for x in l:
        if x in seen:
            dupes.append(x)
        else:
            seen.add(x)
    return dupes

def dict_swap_keys_and_values(dct):
    return dict((v, k) for k, v in dct.items())

# https://stackoverflow.com/a/21139641
# shift dct (dict) values by n to right if n is positive
# and to left if n is negative; returns new dictionary
def dict_shift_values(dct, n):
    shift_values = deque(dct.values())
    shift_values.rotate(n)
    return dict(zip(dct.keys(), shift_values))

def dict_shift_keys(dct, n):
    shift_keys = deque(dct.keys())
    shift_keys.rotate(n)
    return dict(zip(shift_keys, dct.values()))
