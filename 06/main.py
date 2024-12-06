# Imports
import sys
from enum import Enum
#from time import sleep
from copy import deepcopy
from itertools import product
from typing import TypeAlias, List, Tuple, Set, Optional, Any, cast

# Types
RawGameBoard  : TypeAlias = str
RawGameMatrix : TypeAlias = List[List[str]]
GameBoard     : TypeAlias = List[List['Cell']]
Position      : TypeAlias = Tuple[int,int]
Vector        : TypeAlias = Tuple[int,int]
PlayerData    : TypeAlias = Optional[Tuple['Player',Position]]
Task          : TypeAlias = bool

# Exceptions
class RepeatRock(Exception):
    pass
class EndOfGame(Exception):
    pass

# Global Constants
ROCK_CHAR    : str          = '#'
EMPTY_CHAR   : str          = '.'
VISITED_CHAR : str          = 'X'
STEP_DELAY   : float        = 0.2
DEFAULT_INPUT: RawGameBoard = '''
..#.....
.......#
..^.....
......#.
......#.
......#.
......#.
......#.
'''.strip("\n")

# Helpers (Structs, Methods, Etc)
class Direction(Enum):
    NORTH = '^'
    SOUTH = 'v'
    EAST  = '>'
    WEST  = '<'

def input_file() -> RawGameBoard:
    with open('input.txt','r') as file:
        return file.read().strip('\n')

def matrix_string(matrix: List[List[Any]]) -> str:
    as_string: str = ""
    for list in matrix:
        for cell in list:
            as_string += f'{cell}'
        as_string += '\n'
    return as_string

# Helper Classes
class Cell():
    value:            str  = EMPTY_CHAR
    can_visit:        bool = True
    has_been_visited: bool = False
    def __init__(self,has_been_visited:bool=False) -> None:
        self.has_been_visited = has_been_visited
        if has_been_visited:
            self.value = VISITED_CHAR
    def __str__(self) -> str:
        return self.value

class Rock(Cell):
    value    : str  = ROCK_CHAR
    can_visit: bool = False
    def __init__(self) -> None:
        self.directions: Set[Direction] = set()

class Player(Cell):
    has_been_visited: bool = True
    def __init__(self, direction:Direction) -> None:
        self.value = direction.value
        self.direction = direction

# Main Class
class Solver():
    # Dunder Methods
    def __init__(self, raw_game_board: RawGameBoard):
        raw_game_matrix = Solver._raw_game_matrix(raw_game_board)
        self.game_board = Solver._game_board(raw_game_matrix)
        player_data     = Solver._player_position(self.game_board)
        self.obstruction_point: int = 0
        if player_data is not None :
            self.player,self.position = player_data
    def __str__(self) -> str:
        return matrix_string(self.game_board)
    # Public Methods
    def step(self) -> Task:
        vector: Vector = 0,0
        match self.player.direction:
            case Direction.NORTH: vector = -1, 0
            case Direction.SOUTH: vector =  1, 0
            case Direction.EAST : vector =  0, 1
            case Direction.WEST : vector =  0,-1
        try:
            rows,cols = len(self.game_board),len(self.game_board[0])
            while self.game_board[self.position[0]+vector[0]][self.position[1]+vector[1]].can_visit:
                self.game_board[self.position[0]][self.position[1]] = Cell(True)
                self.game_board[self.position[0]+vector[0]][self.position[1]+vector[1]] = self.player
                self.position = self.position[0]+vector[0], self.position[1]+vector[1]
                x,y = self.position[0]+vector[0],self.position[1]+vector[1]
                if isinstance(self.game_board[x][y],Rock):
                    rock: Rock = cast(Rock,self.game_board[x][y])
                    if self.player.direction in rock.directions:
                        self.obstruction_point += 1
                        raise RepeatRock
                    rock.directions.add(self.player.direction)
                if not (0 <= x < rows) or not (0 <= y < cols):
                    raise EndOfGame
        except (IndexError, EndOfGame,RepeatRock):
            return False
        match self.player.direction:
            case Direction.NORTH: self.player.value = Direction.EAST.value ; self.player.direction = Direction.EAST
            case Direction.SOUTH: self.player.value = Direction.WEST.value ; self.player.direction = Direction.WEST
            case Direction.EAST : self.player.value = Direction.SOUTH.value; self.player.direction = Direction.SOUTH
            case Direction.WEST : self.player.value = Direction.NORTH.value; self.player.direction = Direction.NORTH
        return True
    def solve_part_one(self) -> None:
        count: int = 0
        running: bool = True
        while running:
            running = self.step()
            count += 1
        rows,cols,count = len(self.game_board),len(self.game_board[0]),0
        for row,col in product(range(rows),range(cols)):
            if self.game_board[row][col].has_been_visited:
                count += 1
        print(f'Solution: {count} visited cells')
    def solve_part_two(self) -> None:
        rows, cols = len(self.game_board), len(self.game_board[0])
        total_cells = rows * cols
        current = 0
        cached_player: Player = deepcopy(self.player)
        cached_position: Position = deepcopy(self.position)
        print('\n' * 4)
        for row, col in product(range(rows), range(cols)):
            current += 1
            cell = self.game_board[row][col]
            progress = int(50 * current / total_cells)  # 50 character progress bar
            percentage = (current / total_cells) * 100
            status_lines = [
                f'\rProgress: [{"|" * progress}{" " * (50-progress)}] {percentage:.1f}%',
                f'Testing position: ({row}, {col})',
                f'Cells checked: {current}/{total_cells}',
                f'Obstruction Points Found: {self.obstruction_point}'
            ]
            sys.stdout.write('\033[F' * 4)
            for line in status_lines:
                sys.stdout.write('\033[K' + line + '\n')
            sys.stdout.flush()
            if isinstance(cell, Player) or isinstance(cell, Rock):
                continue
            cached_game: GameBoard = deepcopy(self.game_board)
            self.game_board[row][col] = Rock()
            while self.step():
                   pass
            self.player = cached_player
            self.position = cached_position
            self.game_board = cached_game
        print('\n' * 4)
        print(f'Solution: {self.obstruction_point}')
    # Private Methods
    @staticmethod
    def _raw_game_matrix(raw_game_board: RawGameBoard) -> RawGameMatrix:
        return [[cell for cell in list(lines)] for lines in raw_game_board.splitlines()]
    @staticmethod
    def _empty_game_board(rows: int, cols: int) -> GameBoard:
        return [[Cell() for _ in range(rows)] for _ in range(cols)]
    @staticmethod
    def _game_board(raw_game_matrix: RawGameMatrix) -> GameBoard:
        rows, cols = len(raw_game_matrix),len(raw_game_matrix[0])
        game_board: GameBoard = Solver._empty_game_board(rows,cols)
        for row,col in product(range(rows),range(cols)):
            match raw_game_matrix[row][col]:
                case Direction.NORTH.value      : game_board[row][col] = Player(Direction.NORTH)
                case Direction.SOUTH.value      : game_board[row][col] = Player(Direction.SOUTH)
                case Direction.EAST.value       : game_board[row][col] = Player(Direction.EAST )
                case Direction.WEST.value       : game_board[row][col] = Player(Direction.WEST )
                case value if value == ROCK_CHAR: game_board[row][col] = Rock()
                case _                          : continue # It's already an empty cell
        return game_board
    @staticmethod
    def _player_position(game_board: GameBoard) -> PlayerData:
        rows, cols = len(game_board),len(game_board[0])
        for row,col in product(range(rows),range(cols)):
            if isinstance(game_board[row][col],Player):
                player  : Player   = cast(Player,game_board[row][col])
                position: Position = row,col
                return player,position
        return None

# Execution
if __name__ == "__main__":
    print('Initialize Input...')
    input: RawGameBoard = DEFAULT_INPUT
    input = input_file() # If we're using the official input
    print(input,end='\n\n')

    print("Initialize Solver..")
    solver: Solver = Solver(input)
    print(solver,end='\n\n')

    # Run one or the other...
    #solver.solve_part_one()
    solver.solve_part_two()
