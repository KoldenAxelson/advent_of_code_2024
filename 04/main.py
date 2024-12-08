'''
--- Day 4: Ceres Search ---

"Looks like the Chief's not here. Next!" One of The Historians pulls out a device and pushes the only button on it. After a brief flash, you recognize the interior of the Ceres monitoring station!

As the search for the Chief continues, a small Elf who lives on the station tugs on your shirt; she'd like to know if you could help her with her word search (your puzzle input). She only has to find one word: XMAS.

This word search allows words to be horizontal, vertical, diagonal, written backwards, or even overlapping other words. It's a little unusual, though, as you don't merely need to find one instance of XMAS - you need to find all of them. Here are a few ways XMAS might appear, where irrelevant characters have been replaced with .:

..X...
.SAMX.
.A..A.
XMAS.S
.X....
The actual word search will be full of letters instead. For example:

MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
In this word search, XMAS occurs a total of 18 times; here's the same word search again, but where letters not involved in any XMAS have been replaced with .:

....XXMAS.
.SAMXMS...
...S..A...
..A.A.MS.X
XMASAMX.MM
X.....XA.A
S.S.S.S.SS
.A.A.A.A.A
..M.M.M.MM
.X.X.XMASX
Take a look at the little Elf's word search. How many times does XMAS appear?
'''

# Imports
from enum import Enum
from itertools import product
from dataclasses import dataclass
from typing import TypeAlias, List, Optional, Tuple, Set

# Types                                             # Raw   List    Matrix       Processor: Cell
RawCrossword      : TypeAlias = str                 # XMASX XMASX,  [X,M,A,S,X], [<X>,<M>,<A>,<S>,<X>],
ListCrossword     : TypeAlias = List[str]           # OOOOM OOOOM,  [O,O,O,O,M], [<O>,<O>,<O>,<O>,<M>],
MatrixCrossword   : TypeAlias = List[List[str]]     # OOOOA OOOOA,  [O,O,O,O,A], [<O>,<O>,<O>,<O>,<A>],
ProcessorCrossword: TypeAlias = List[List['Cell']]  # OOOOS OOOOS   [O,O,O,O,S]  [<O>,<O>,<O>,<O>,<S>]

# Global Constants
DEFAULT_INPUT: RawCrossword = """
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
"""

# Helper Functions
def generate_raw_crossword() -> RawCrossword:
    return DEFAULT_INPUT

def get_official_crossword() -> RawCrossword:
    get_official_crossword: RawCrossword = ""
    with open('input.txt','r') as file:
        get_official_crossword = file.read().strip('\n')
    return get_official_crossword

def in_matrix_bounds(row,col,rows,cols) -> bool:
    return 0 <= row < rows and 0 <= col < cols

# Helper Structurs / Classes
class Direction(Enum):
    UP    = 'up'
    RIGHT = 'right'
    DOWN  = 'down'
    LEFT  = 'left'

@dataclass
class Cell():
    # Properties
    value: str
    up   : Optional['Cell']
    right: Optional['Cell']
    down : Optional['Cell']
    left : Optional['Cell']
    is_solution: bool
    solutions: Set
    # Dunder Methods
    def __init__(self, value: str) -> None:
        self.value = value
        self.up, self.right, self.down, self.left = None, None, None, None
        self.is_solution = False
        self.solutions = set()
    def __getitem__(self, direction: Direction) -> Optional['Cell']:
        match direction:
            case Direction.UP   : return self.up
            case Direction.RIGHT: return self.right
            case Direction.DOWN : return self.down
            case Direction.LEFT : return self.left
            case _              : return None
    def __str__(self) -> str:
        return self.value
    # Public Methods
    def set_matches(self) -> None:
        if not self._is_X(): return None
        self._match_direction(Direction.UP)
        self._match_direction(Direction.RIGHT)
        self._match_direction(Direction.DOWN)
        self._match_direction(Direction.LEFT)
        self._match_diagnol((Direction.UP,   Direction.RIGHT))
        self._match_diagnol((Direction.RIGHT,Direction.DOWN ))
        self._match_diagnol((Direction.DOWN, Direction.LEFT ))
        self._match_diagnol((Direction.LEFT, Direction.UP   ))
    # Private Methods
    def _is_X(self) -> bool:
        return self.value == 'X'
    def _match_direction(self,direction:Direction) -> bool:
        if self[direction] is None or \
            self[direction][direction] is None or \
            self[direction][direction][direction] is None: return False
        if f'{self[direction]}' != 'M' or \
            f'{self[direction][direction]}' != 'A' or \
            f'{self[direction][direction][direction]}' != 'S': return False
        self.is_solution = True
        self[direction].is_solution = True
        self[direction][direction].is_solution = True
        self[direction][direction][direction].is_solution = True
        self.solutions.add(direction)
        return True
    def _match_diagnol(self,directions:Tuple[Direction,Direction]) -> bool:
        if self[directions[0]] is None or \
            self[directions[0]][directions[1]] is None or \
            self[directions[0]][directions[1]][directions[0]] is None or \
            self[directions[0]][directions[1]][directions[0]][directions[1]] is None or \
            self[directions[0]][directions[1]][directions[0]][directions[1]][directions[0]] is None or \
            self[directions[0]][directions[1]][directions[0]][directions[1]][directions[0]][directions[1]] is None:
                return False
        if f'{self[directions[0]][directions[1]]}' != 'M' or \
            f'{self[directions[0]][directions[1]][directions[0]][directions[1]]}' != 'A' or \
            f'{self[directions[0]][directions[1]][directions[0]][directions[1]][directions[0]][directions[1]]}' != 'S':
                return False
        self.is_solution = True
        self[directions[0]][directions[1]].is_solution = True
        self[directions[0]][directions[1]][directions[0]][directions[1]].is_solution = True
        self[directions[0]][directions[1]][directions[0]][directions[1]][directions[0]][directions[1]].is_solution = True
        self.solutions.add(directions)
        return True

# Main Class
class Crossword():
    # Dunder Methods
    def __init__(self, raw_crossword: RawCrossword) -> None:
        list_crossword:           ListCrossword      = Crossword._list_crossword(raw_crossword)
        matrix_crossword:         MatrixCrossword    = Crossword._matrix_crossword(list_crossword)
        self.processor_crossword: ProcessorCrossword = Crossword._processor_crossword(matrix_crossword)
    def __str__(self) -> str:
        as_string = ""
        rows, cols = len(self.processor_crossword[0]), len(self.processor_crossword)
        for row,col in product(range(rows),range(cols)):
            cell = self.processor_crossword[row][col]
            as_string += f'{cell if cell.is_solution else "."}{"\n" if col+1 == cols else ""}'
        return as_string
    # Public Methods
    def get_results(self) -> int:
        count = 0
        rows, cols = len(self.processor_crossword[0]), len(self.processor_crossword)
        for row,col in product(range(rows),range(cols)):
            count += len(self.processor_crossword[row][col].solutions)
        return count
    # Private Methods
    @staticmethod
    def _list_crossword(raw_crossword: RawCrossword) -> ListCrossword:
        return [line for line in raw_crossword.split('\n') if line != '']
    @staticmethod
    def _matrix_crossword(list_crossword: ListCrossword) -> MatrixCrossword:
        return [list(character) for character in list_crossword]
    @staticmethod
    def _processor_crossword(matrix_crossword: MatrixCrossword) -> ProcessorCrossword:
        rows, cols = len(matrix_crossword[0]), len(matrix_crossword)
        processor_crossword: ProcessorCrossword = [[Cell(value) for value in list] for list in matrix_crossword]
        for row, col in product(range(rows),range(cols)):
            if in_matrix_bounds(row-1,col  ,rows,cols): processor_crossword[row][col].up    = processor_crossword[row-1][col  ]
            if in_matrix_bounds(row  ,col+1,rows,cols): processor_crossword[row][col].right = processor_crossword[row  ][col+1]
            if in_matrix_bounds(row+1,col  ,rows,cols): processor_crossword[row][col].down  = processor_crossword[row+1][col  ]
            if in_matrix_bounds(row  ,col-1,rows,cols): processor_crossword[row][col].left  = processor_crossword[row  ][col-1]
        for row, col in product(range(rows),range(cols)):
            processor_crossword[row][col].set_matches()
        return processor_crossword

# Execute
if __name__ == "__main__":
    print("Raw Crossword...")
    # raw_crossword = generate_raw_crossword()
    raw_crossword = get_official_crossword()
    print(raw_crossword,end='\n')

    print("Crossword Solver")
    crossword: Crossword = Crossword(raw_crossword)
    print(crossword)

    print(f"Solutions Found: {crossword.get_results()}")
