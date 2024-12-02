from random import randint
from typing import List

# Scale the difficulty/complexity by incrementing this number
# This controls how many items are in each list for the problem
LIST_LENGTH = 3

def make_random_list() -> List[int]:
    '''Returns a list of random numbers between 0-9'''
    return [randint(0,9) for _ in range(0,LIST_LENGTH)]

def print_list_update(message:str,list_a:List[int],list_b:List[int]):
    '''Shows 2 Lists with an prepended message'''
    print(f'{message}\n{list_a}\n{list_b}',end='\n\n')

# Initialize the lists
list_1 = make_random_list()
list_2 = make_random_list()
print_list_update("Initial Lists...",list_1,list_2)

# Sort the lists
list_1.sort()
list_2.sort()
print_list_update("Sorted Lists...",list_1,list_2)

# Compare the lists
compared_result = [abs(x-y) for x,y in zip(list_1,list_2)]
print(f'Compared Lists...\n{compared_result}\n')

# Sum the result
print(f'Answer: {sum(compared_result)}')
