# Original Question
'''
--- Day 3: Mull It Over ---

"Our computers are having issues, so I have no idea if we have any Chief Historians in stock! You're welcome to check the warehouse, though," says the mildly flustered shopkeeper at the North Pole Toboggan Rental Shop. The Historians head out to take a look.

The shopkeeper turns to you. "Any chance you can see why our computers are having issues again?"

The computer appears to be trying to run a program, but its memory (your puzzle input) is corrupted. All of the instructions have been jumbled up!

It seems like the goal of the program is just to multiply some numbers. It does that with instructions like mul(X,Y), where X and Y are each 1-3 digit numbers. For instance, mul(44,46) multiplies 44 by 46 to get a result of 2024. Similarly, mul(123,4) would multiply 123 by 4.

However, because the program's memory has been corrupted, there are also many invalid characters that should be ignored, even if they look like part of a mul instruction. Sequences like mul(4*, mul(6,9!, ?(12,34), or mul ( 2 , 4 ) do nothing.

For example, consider the following section of corrupted memory:

xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))
Only the four highlighted sections are real mul instructions. Adding up the result of each instruction produces 161 (2*4 + 5*5 + 11*8 + 8*5).

Scan the corrupted memory for uncorrupted mul instructions. What do you get if you add up all of the results of the multiplications?
'''
# Simplified Question
'''
from typing import Self
Input: str = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
Parse: str = " mul(2,4)                    mul(5,5)                mul(11,8)mul(8,5) "
Calcu: int = (2*4)+(5*5)+(11*8)+(8*5)
Solve: int = 161

Parameters:
    1. mul arguments can be 1-3 digits
    2. mul function calls are always a continuous string of digits

Solutions:
    1. Could implement a Regex to quickly sort out the function (Shortest: Black Box)
    2. Could implement a Two-Pointers Solution (Longest: Easier to Read)

Decision:
    Going to go with a Verbose and Understandable Solution. Aiming for Teachable Code.
'''
# Imports
from typing import TypeAlias, List, Tuple

# Types
CorruptedData  : TypeAlias = str                    # "xxxmul(2,2)xxxmul(2,2)xxxmul(2,2)"
UncorruptedData: TypeAlias = List[str]              # ["2,2","2,2","2,2"]
ParsedArguments: TypeAlias = List[Tuple[int,int]]   # [(2,2),(2,2),(2,2)]

# Global Constants
DEFAULT_INPUT: CorruptedData = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"

# Helper Functions
def _generate_test_input() -> CorruptedData:
    return DEFAULT_INPUT

# Main Class
class DataSolver():
    # Dunder Methods
    def __init__(self, corrupted_data: CorruptedData) -> None:
        uncorrupted_data:       UncorruptedData = DataSolver._uncorrupt_data(corrupted_data)
        self.parsed_arguments:  ParsedArguments = DataSolver._parse_arguments(uncorrupted_data)
    def __str__(self) -> str:
        return f'{self.parsed_arguments}'
    # Public Methods
    def solution(self) -> int:
        solution = 0
        for x,y in self.parsed_arguments:
            solution += x * y
        return solution
    # Private Methods
    @staticmethod
    def _is_valid_section(section: str) -> bool:
        # We're only passing strings that should look like XXX,YYY
        if not "," in section: return False
        split_section = section.split(',')
        if len(split_section) != 2: return False
        if len(split_section[0]) > 3: return False
        if len(split_section[1]) > 3: return False
        if not split_section[0].isalnum(): return False
        if not split_section[1].isalnum(): return False
        return True
    @staticmethod
    def _uncorrupt_data(corrupted_data: CorruptedData) -> UncorruptedData:
        uncorrupted_data: UncorruptedData = []
        # "mul(0,0)" is 8 characters
        # CorruptedData less than 8 characters is all junk data
        if len(corrupted_data) < 8: return uncorrupted_data

        # Get "mul(XXX,YYY)" Section
        idx_a = corrupted_data.find("mul(")
        idx_b = corrupted_data.find(")")
        section = corrupted_data[idx_a+4:idx_b]

        # Validate and Recurse
        # Depending on if a valid solution is found we set the next search index
        new_idx = idx_a + 4
        if DataSolver._is_valid_section(section):
            uncorrupted_data.append(section)
            new_idx = idx_b + 2
        uncorrupted_data.extend(DataSolver._uncorrupt_data(corrupted_data[new_idx:]))
        return uncorrupted_data
    @staticmethod
    def _parse_arguments(uncorrupted_data: UncorruptedData) -> ParsedArguments:
        # Data has been validated so it's clear to make assumptions
        return [(int(section.split(',')[0]),int(section.split(',')[1])) for section in uncorrupted_data]

# Execution
if __name__ == "__main__":
    print("Input Data...")
    input_data: CorruptedData = _generate_test_input()
    print(input_data,end='\n\n')

    print("Data Solver...")
    data_solver: DataSolver = DataSolver(input_data)
    print(data_solver,end='\n\n')

    print("Solution: ",end="")
    print(data_solver.solution(),end="\n\n")
