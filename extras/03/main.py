"""
--- Day X: Elf Signal Processing ---

The elves use a complex signal processing system to coordinate toy production across
workshops. Each workshop contains signal processors that transform and combine signals
in sequence.

Input format:
First line: Processor chain configuration as [width]x[height] (e.g., "3x4" creates
a 3-wide, 4-high grid of processors)
Following lines: Initial signals entering from the top, as comma-separated values:
signal_values | processing_rules

Example input:
3x4
1.0,2.0,3.0 | ADD,SPLIT,COMBINE
2.0,1.0,4.0 | SPLIT,COMBINE,ADD

Each processor can:
- ADD: Sum its inputs
- SPLIT: Divide signal equally among outputs
- COMBINE: Multiply inputs together

Signals flow down and right. Each processor maintains its state between signals and
can affect how future signals are processed based on its history.

Calculate:
1. The final output values at the bottom of the grid
2. The change in each processor's state after all signals
3. The sum of all signals that reached dead ends (signals that couldn't flow further)

Processors should be implemented as objects that can be easily extended with new
processing rules.
"""

# Imports
from math import prod
from random import randint
from itertools import product
from enum import Enum
from typing import TypeAlias, Optional, Tuple, List, Callable

# Global Constants
MAX_INIT_SIGNAL_VALUE: int            = 6       # Change if you want bigger Matrix Numbers
MATRIX_SIZE          : Tuple[int,int] = (4,3)   # Change to determine Grid Size (WxL)

# Enums
class Process(Enum):
    ADD     = 'ADD'
    SPLIT   = 'SPLIT'
    COMBINE = 'COMBINE'

# Helper Functions
def in_bounds(value:int,limit:int) -> bool:
    '''Used for List Indicies to make sure it's in bounds of list'''
    return 0 <=value < limit

def in_matrix_bounds(row:int,col:int) -> bool:
    '''Checks coordinates against our Matrix Size'''
    return in_bounds(row,MATRIX_SIZE[1]) and in_bounds(col,MATRIX_SIZE[0])

# Secondary Class
class Signal():
    '''A Signal has a number on a grid with a reference to 2 adjectent cells'''
    # These references are important for performing Matrix operations.
    def __init__(self, value: float, down: Optional['Signal'], right: Optional['Signal']) -> None:
        self.value = value
        self.down = down
        self.right = right

# Types
# This hints to what order we handle our pipeline
TestData      : TypeAlias = str                  # {See Full Test Data}
TestRow       : TypeAlias = str                  #  "1.0,2.0,3.0 | ADD,SPLIT,COMBINE"
DataRow       : TypeAlias = Tuple[str,str]       # ("1.0,2.0,3.0","ADD,SPLIT,COMBINE")
FloatSection  : TypeAlias = List[float]          # [ 1.0,2.0,3.0 ]
ProcessSection: TypeAlias = List[Process]        # [<ADD>,<SPLIT>,<COMBINE>]
SignalMatrix  : TypeAlias = List[List[Signal]]   # Matrix of Linked Signals
ProcessMatrix : TypeAlias = List[List[Process]]  # Matrix of Commands to be executed on SignalMatrix

# Main Class
class Processor():
    # Dunder Methods
    def __init__(self, data: TestData) -> None:
        '''Initializer that orchestrates our data pipeline'''
        # See the "Types" section for our data processing pipeline
        raw_rows       = Processor._raw_rows(data)
        row_sections   = [Processor._row_sections(raw_row) for raw_row in raw_rows]
        float_sections, process_sections = zip(*row_sections)
        float_matrix   = [Processor._list_from_float_string(float_string) for float_string in float_sections]
        process_matrix = [Processor._list_from_process_string(process_string) for process_string in process_sections]
        self.signal_matrix : SignalMatrix  = Processor._create_signal_matrix(float_matrix)
        self.process_matrix: ProcessMatrix = process_matrix

    def __str__(self) -> str:
        '''Display a Float Table with gratious spacing for big numbers'''
        as_string = ""
        for signal_row in self.signal_matrix:
            as_string += ','.join(f'{signal.value:>8.2f}' for signal in signal_row) + '\n'
        return as_string

    # Public Methods
    def add(self, index: int) -> None:
        '''
        Gets the sum of the entire Row, increment the following row's first element by that sum
        add(index=0) ==>
             old           new
        [1.0,1.0,1.0] [1.0,1.0,1.0]
        [0.0,0.0,0.0] [3.0,0.0.0.0]
        '''
        row_sum = sum(signal.value for signal in self.signal_matrix[index])
        if in_matrix_bounds(index + 1,0):
            self.signal_matrix[index+1][0].value += row_sum

    def split(self, index: int) -> None:
        '''
        Get the half-value of each Signal, increment the signals down and down-right signals by that value
        split(index=0) ==>
              old             i=0             i=1             i=2
        [1.0, 3.0, 5.0] [1.0, 3.0, 5.0] [1.0, 3.0, 5.0] [1.0, 3.0, 5.0]
                         ^^^                  ^^^                  ^^^
        [0.0, 0.0, 0.0] [0.5, 0.5, 0.0] [0.5, 2.0, 1.5] [0.5, 2.0, 4.0]
                        +0.5 +0.5            +1.5 +1.5            +2.5 +N/A
        '''
        for signal in self.signal_matrix[index]:
            value = signal.value / 2
            if signal.down is not None:
                signal.down.value += value
                if signal.down.right is not None:
                    signal.down.right.value += value

    def combine(self, index: int) -> None:
        '''
        Gets the product of the entire Row, increment the following row's first element by that product
        add(index=0) ==>
             old           new
        [2.0,2.0,2.0] [2.0,2.0,2.0]
        [0.0,0.0,0.0] [8.0,0.0.0.0]
        '''
        row_product = prod(signal.value for signal in self.signal_matrix[index])
        if in_matrix_bounds(index + 1,0):
            self.signal_matrix[index+1][0].value += row_product

    def process_function(self, process: Process) -> Callable:
        '''Our Processes are in an Enum, so this is the most elegant solution'''
        match process:
            case Process.ADD    : return self.add
            case Process.SPLIT  : return self.split
            case Process.COMBINE: return self.combine
            # We'll fail gracefully, instead of breaking our app.
            # Since the process commands return None, a blank lambda will not cause our app to crash.
            case _              : print(f"Unrecognized Process: {process}"); return lambda: None

    def solve(self) -> None:
        '''Takes the Process Matrix and applies it to the Signal Matrix'''
        for index, processes in enumerate(self.process_matrix):
            for process in processes:
                self.process_function(process)(index)

    # Private Methods
    # They're all static because they're there to process the TestData passed into the __init__
    # They're not handling any self references because they're not here to handle the business logic
    # See the "Typing" section to see examples of how it processes the TestData
    # See the __init__ function to see usage examples of the functions
    @staticmethod
    def _raw_rows(test_data: TestData) -> List[TestRow]:
        '''
        Turn the TestData string into a List seperated by new-line characters, and excludes blank rows
        old                         | new
        """                         | [
        1.0,2.0,3.0 | ADD,ADD,ADD   |   "1.0,2.0,3.0 | ADD,ADD,ADD"
        0.0,0.0,0.0 | ADD,ADD,ADD   |   "0.0,0.0,0.0 | ADD,ADD,ADD"
                                    |   "" # This is discarded and not added to the array
        """                         | ]
        '''
        return [test_row for test_row in test_data.split('\n') if test_row != '']

    @staticmethod
    def _row_sections(test_row: TestRow) -> DataRow:
        '''
        Turn a TestRow string into a more accessible DataRow Tuple[str,str]
        old                         | new
        "1.0,2.0,3.0 | ADD,ADD,ADD" | ("1.0,2.0,3.0","ADD,ADD,ADD")
        '''
        sections = [section for section in test_row.split(' | ')]
        return sections[0],sections[1]

    @staticmethod
    def _list_from_float_string(float_string: str) -> FloatSection:
        '''
        Get the Float String from a DataRow Section, and make it into a usable Float List
        old           | new
        "1.0,2.0,3.0" | [1.0,2.0,3.0]
        '''
        return [float(value) for value in float_string.split(',')]

    @staticmethod
    def _list_from_process_string(process_string: str) -> ProcessSection:
        '''
        Get the Process String from a DataRow Section, and make it into a usable Process List
        old           | new
        "ADD,ADD,ADD" | [<Process.ADD>,<Process.ADD>,<Process.ADD>]
        '''
        return [Process(process.upper()) for process in process_string.split(',')]

    @staticmethod
    def _create_signal_matrix(values: List[List[float]]) -> SignalMatrix:
        '''
        Creates a Signal Matrix from a Matrix of Floats

        1.) Populate the Signal Grid with Signals that dont have reference to down or right
        2.) Iterate through the signals, check the location, if the location exist, update the down/right reference
        3.) Return the Signal Grid
        '''
        cols, rows = MATRIX_SIZE
        signal_grid = [[Signal(values[row][col], None, None) for col in range(cols)] for row in range(rows)]
        for row, col in product(range(rows),range(cols)):
            if row + 1 < rows:
                signal_grid[row][col].down  = signal_grid[row + 1][col]
            if col + 1 < cols:
                signal_grid[row][col].right = signal_grid[row][col + 1]
        return signal_grid

# Local Functions
def generate_test_data() -> TestData:
    '''
    We're generating out our sample data to help with robust development.
      This function will be more than one responsibility because it's for sample data generation,
    and we don't want to make useful tools that might help solve the problem at hand by making
    sample data.
    '''
    # Let's Handle making our test data first
    # Make a Matrix of float values that'll be our Signal Values
    # Add a Helper to get a random Process to help with generation
    # Make a X by 3 Matrix of random processes to slot in the post section
    float_matrix = [[float(randint(0,MAX_INIT_SIGNAL_VALUE)) for _ in range(MATRIX_SIZE[0])] for _ in range(MATRIX_SIZE[1])]
    def random_process() -> Process:
        match randint(0,2):
            case 0: return Process.ADD
            case 1: return Process.SPLIT
            case _: return Process.COMBINE # If we get 2 we just also handle the default as well
    process_list = [[random_process() for _ in range(3)] for _ in range(MATRIX_SIZE[1])]

    # Now we've got to get the data into a string to return
    # Since this question is partly string manipulation, we shouldn't pass on any non-string data
    # Each row should look like this: "1.0,1.0,1.0 | ADD,ADD,ADD"
    test_data: TestData = ""
    for values, processes in zip(float_matrix,process_list):
        test_data += ','.join([str(value) for value in values])
        test_data += ' | '
        test_data += ','.join([process.value for process in processes])
        test_data += '\n'
    return test_data

# Execute
if __name__ == "__main__":
    print("Raw Data...")
    raw_data = generate_test_data()
    print(raw_data,end='\n')

    print("Processor Object...")
    processor = Processor(raw_data)
    print(processor,end='\n')

    print("Solved Data ...")
    processor.solve()
    print(processor,end='\n')
