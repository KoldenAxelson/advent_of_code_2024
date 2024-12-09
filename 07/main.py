# Imports
import sys
from enum import Enum
from itertools import product
from typing import TypeAlias, List, Tuple, Dict

# Types
InputData : TypeAlias = str
InputLine : TypeAlias = str
Problems  : TypeAlias = List['Problem']
Equation  : TypeAlias = List[int]
Operations: TypeAlias = List['Operation']

# Exceptions
# Didn't feel the need to in this context
# Dataset is already pre-verified and we're optimizing for it

# Global Constants
DEFAULT_INPUT: InputData = """
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
"""

# Helper Functions
def get_input_data(use_official_data=False) -> InputData:
    input_data: str = DEFAULT_INPUT.strip('\n')
    if use_official_data:
        with open('input.txt','r') as file:
            input_data = file.read().strip('\n')
    return input_data

def eval_l2r(equation_string: str) -> int:
    op_map = {op.value[0]: op.value[1] for op in Operation.ALL()}
    num_string = equation_string
    for op in op_map.keys():
        num_string = num_string.replace(op, ' ')
    numbers = [int(n) for n in num_string.split()]
    operators = [op for op in equation_string if op in op_map.keys()]
    result = numbers[0]
    for i in range(len(operators)):
        result = op_map[operators[i]](result, numbers[i + 1])
    return int(result)

# Just to help with Progression Visualization for Longer Datasets
def create_buffer(stats: Dict[str,str]) -> None:
    print((len(stats) + 10) * '\n')

def remove_buffer(stats: Dict[str,str]) -> None:
    sys.stdout.write('\033[F' * (len(stats) + 10))
    sys.stdout.write('\033[J')

def show_stats(stats: Dict[str,str]) -> None:
    # Clear the entire section first
    sys.stdout.write('\033[F' * (len(stats) + 10))
    sys.stdout.write('\033[J')
    for k,v in stats.items():
        if k == 'Progress':
            progress_data = [int(num) for num in v.split('/')]
            current = progress_data[0]
            maximum = progress_data[1]
            progress = int(50 * current / maximum)
            percentage = (current / maximum) * 100
            progress_bar = f'[{"|" * progress}{" " * (50-progress)}] {percentage:.1f}%'
            print(progress_bar)
        else:
            print(f'{k}: {v}')
    sys.stdout.write('\033[F' * (len(stats) + 10))

# Helper Classes
class Operation(Enum):
    ADD = ('+', lambda x,y: x+y)
    MUL = ('*', lambda x,y: x*y)
    CON = ('|', lambda x,y: int(f'{x}{y}'))
    NOF = ('~', lambda x,y: 0) # No Operation Found
    @staticmethod
    def P1() -> Operations:
        return [Operation.ADD, Operation.MUL] # Not using CON for Part 1
    @staticmethod
    def P2() -> Operations:
        return [Operation.ADD, Operation.MUL, Operation.CON]
    @staticmethod
    def ALL() -> Operations:
        return Operation.P1() # Set ALL to Current Part

class Problem():
    # Properties
    is_valid:   bool       = False
    solution:   int        = 0
    equation:   Equation   = []
    operations: Operations = []

    # Dunder Methods
    def __init__(self, input_line: InputLine) -> None:
        list_values: List[int] = Problem._list_values(input_line)
        self.solution = list_values[0]
        self.equation = list_values[1:]
        self.operations = [Operation.NOF for _ in range(len(self.equation)-1)]
        valid_operations = Problem._valid_operations(self.solution, self.equation)
        self.is_valid = len(valid_operations) > 0
        if self.is_valid:
            self.operations = valid_operations[0]

    def __str__(self) -> str:
        validity_string = 'O' if self.is_valid else 'X'
        equation_string = Problem._equation_string(self.equation, self.operations)
        return f'{validity_string} {self.solution}={equation_string}'

    # Public Methods

    # Private Methods
    @staticmethod
    def _list_values(input_line: InputLine) -> List[int]:
        return [int(num) for num in input_line.replace(':','').split(' ')]
    @staticmethod
    def _possible_operations(length: int) -> List[Tuple[Operation, ...]]:
        operations = Operation.ALL()
        return [combo for combo in list(product(operations, repeat=length))]
    @staticmethod
    def _equation_string(equation: Equation, operations: Operations) -> str:
        equation_string = ""
        for i,e in enumerate(equation):
            if i != 0:
                equation_string += operations[i-1].value[0]
            equation_string += f'{e}'
        return equation_string
    @staticmethod
    def _valid_operations(solution: int, equation: List[int]) -> List[Operations]:
        valid_operations: List[Operations] = []
        possible_operations = Problem._possible_operations(len(equation)-1)
        for operation in possible_operations:
             if solution == eval_l2r(Problem._equation_string(equation,list(operation))):
                 valid_operations.append(list(operation))
        return valid_operations

# Main Classes
class Solver():
    # Properties
    problems: Problems = []
    # Dunder Methods
    def __init__(self, input_data: InputData) -> None:
        input_lines = input_data.splitlines()
        stats: Dict[str,str] = {}
        stats['Progress'] = f'0/{len(input_lines)}'
        create_buffer(stats)
        for index, input_line in enumerate(input_lines):
            stats['Progress'] = f'{index}/{len(input_lines)}'
            show_stats(stats)
            self.problems.append(Problem(input_line))
        remove_buffer(stats)
    def __str__(self) -> str:
        as_string: str = ""
        for problem in self.problems:
            as_string += f'{problem}' + '\n'
        return as_string
    # Public Methods
    def solve(self) -> int:
        valid_problem_solutions: List[int] = []
        for problem in self.problems:
            if problem.is_valid:
                valid_problem_solutions.append(problem.solution)
        return sum(valid_problem_solutions)

# Execution
if __name__ == "__main__":
    print("Initialize Input Data...")
    input_data = get_input_data(use_official_data=True)
    print(input_data,end='\n\n')

    print("Initialize Solver...",end='\n\n\n')
    solver = Solver(input_data)
    print(solver,end='\n')

    print(f"Answer: {solver.solve()}")
