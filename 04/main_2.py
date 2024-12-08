from enum import Enum
from itertools import product
from dataclasses import dataclass
from typing import TypeAlias, List, Optional, Tuple, Set

# Types
RawCrossword      : TypeAlias = str
ListCrossword     : TypeAlias = List[str]
MatrixCrossword   : TypeAlias = List[List[str]]
ProcessorCrossword: TypeAlias = List[List['Cell']]

class Direction(Enum):
    UP    = 'up'
    RIGHT = 'right'
    DOWN  = 'down'
    LEFT  = 'left'
    UP_LEFT = 'up_left'
    UP_RIGHT = 'up_right'
    DOWN_LEFT = 'down_left'
    DOWN_RIGHT = 'down_right'

@dataclass
class Cell():
    value: str
    up   : Optional['Cell']
    right: Optional['Cell']
    down : Optional['Cell']
    left : Optional['Cell']
    up_left: Optional['Cell']
    up_right: Optional['Cell']
    down_left: Optional['Cell']
    down_right: Optional['Cell']
    is_solution: bool
    solutions: Set

    def __init__(self, value: str) -> None:
        self.value = value
        self.up, self.right, self.down, self.left = None, None, None, None
        self.up_left, self.up_right = None, None
        self.down_left, self.down_right = None, None
        self.is_solution = False
        self.solutions = set()

    def __getitem__(self, direction: Direction) -> Optional['Cell']:
        match direction:
            case Direction.UP: return self.up
            case Direction.RIGHT: return self.right
            case Direction.DOWN: return self.down
            case Direction.LEFT: return self.left
            case Direction.UP_LEFT: return self.up_left
            case Direction.UP_RIGHT: return self.up_right
            case Direction.DOWN_LEFT: return self.down_left
            case Direction.DOWN_RIGHT: return self.down_right
            case _: return None

    def __str__(self) -> str:
        return self.value

    def set_matches(self) -> None:
        if not self._is_A(): return None
        self._check_x_pattern()

    def _is_A(self) -> bool:
        return self.value == 'A'

    def _check_mas_segment(self, first: Optional['Cell'], second: Optional['Cell']) -> bool:
        """Check if cells form either MAS or SAM"""
        if not first or not second: return False
        return ((first.value == 'M' and second.value == 'S') or
                (first.value == 'S' and second.value == 'M'))

    def _check_x_pattern(self) -> None:
        """Check for X pattern centered on A"""
        # Check upper-left to lower-right diagonal
        diagonal1 = self._check_mas_segment(self.up_left, self.down_right)

        # Check upper-right to lower-left diagonal
        diagonal2 = self._check_mas_segment(self.up_right, self.down_left)

        if diagonal1 and diagonal2:
            self.is_solution = True
            self.up_left.is_solution = True
            self.up_right.is_solution = True
            self.down_left.is_solution = True
            self.down_right.is_solution = True
            self.solutions.add(("diagonal"))

class Crossword():
    def __init__(self, raw_crossword: RawCrossword) -> None:
        list_crossword: ListCrossword = self._list_crossword(raw_crossword)
        matrix_crossword: MatrixCrossword = self._matrix_crossword(list_crossword)
        self.processor_crossword: ProcessorCrossword = self._processor_crossword(matrix_crossword)

    def __str__(self) -> str:
        as_string = ""
        rows, cols = len(self.processor_crossword[0]), len(self.processor_crossword)
        for row,col in product(range(rows),range(cols)):
            cell = self.processor_crossword[row][col]
            as_string += f'{cell if cell.is_solution else "."}{"\n" if col+1 == cols else ""}'
        return as_string

    def get_results(self) -> int:
        count = 0
        rows, cols = len(self.processor_crossword[0]), len(self.processor_crossword)
        for row,col in product(range(rows),range(cols)):
            count += len(self.processor_crossword[row][col].solutions)
        return count

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

        # Set up all cell connections including diagonals
        for row, col in product(range(rows),range(cols)):
            if row > 0:
                processor_crossword[row][col].up = processor_crossword[row-1][col]
                if col > 0:
                    processor_crossword[row][col].up_left = processor_crossword[row-1][col-1]
                if col < cols-1:
                    processor_crossword[row][col].up_right = processor_crossword[row-1][col+1]
            if col < cols-1:
                processor_crossword[row][col].right = processor_crossword[row][col+1]
            if row < rows-1:
                processor_crossword[row][col].down = processor_crossword[row+1][col]
                if col > 0:
                    processor_crossword[row][col].down_left = processor_crossword[row+1][col-1]
                if col < cols-1:
                    processor_crossword[row][col].down_right = processor_crossword[row+1][col+1]
            if col > 0:
                processor_crossword[row][col].left = processor_crossword[row][col-1]

        # Find patterns
        for row, col in product(range(rows),range(cols)):
            processor_crossword[row][col].set_matches()

        return processor_crossword

def get_official_crossword() -> RawCrossword:
    with open('input.txt','r') as file:
        return file.read().strip('\n')

if __name__ == "__main__":
    raw_crossword = get_official_crossword()
    print("Raw Crossword...")
    print(raw_crossword, end='\n\n')

    print("X-MAS Pattern Finder")
    crossword = Crossword(raw_crossword)
    print(crossword)

    print(f"X-MAS Patterns Found: {crossword.get_results()}")
