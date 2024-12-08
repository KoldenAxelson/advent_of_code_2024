from random import randint
from typing import List, Tuple, Set

# Scale the difficulty/complexity by incrementing this number
# This controls how many items are in each list for the problem
LIST_LENGTH = 3

def make_random_list() -> List[int]:
    '''Returns a list of random numbers between 0-9'''
    return [randint(0,9) for _ in range(0,LIST_LENGTH)]

def get_official_lists() -> Tuple[List[int],List[int]]:
    official_list_1: List[int] = []
    official_list_2: List[int] = []
    raw_input: str = ""
    with open("input.txt",'r') as file:
        raw_input = file.read().strip('\n')
    raw_list: List[str] = raw_input.splitlines()
    for line in raw_list:
        list_line = line.split("   ")
        official_list_1.append(int(list_line[0]))
        official_list_2.append(int(list_line[1]))
    return official_list_1,official_list_2


def print_list_update(message:str,list_a:List[int],list_b:List[int]):
    '''Shows 2 Lists with an prepended message'''
    print(f'{message}\n{list_a}\n{list_b}',end='\n\n')

def compare_lists(list_1: List[int], list: List[int]) -> int:
    set_of_1: Set[int] = set(list_1)
    compare_scores: List[int] = []
    for num in set_of_1:
        score: int = num * sum([1 for x in list_2 if x == num])
        compare_scores.append(score)
    return sum(compare_scores)

# Initialize the lists
# list_1 = make_random_list()
# list_2 = make_random_list()
list_1, list_2 = get_official_lists()
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
print(f'Answer_2:  {compare_lists(list_1,list_2)}')
