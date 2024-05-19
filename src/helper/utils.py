import itertools
from collections import deque

# https://stackoverflow.com/a/40389411
def printTable(myDict, colList=None):
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
   return [formatStr.format(*item) for item in myList].join("\n")

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

# https://stackoverflow.com/a/55092246
# rollup = lambda a: a[1:] + a[:1]
# rolldown = lambda a: a[-1:] + a[:-1]
# rollleft = lambda a: [row[1:] + row[:1] for row in a]
# rollright = lambda a: [row[-1:] + row[:-1] for row in a]

# shiftedup= lambda a: a[1:] + [[0] * len(a[0])]
