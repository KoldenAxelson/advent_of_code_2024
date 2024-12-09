# Imports
from copy import deepcopy
from itertools import product
from dataclasses import dataclass
from collections import defaultdict
from typing import TypeAlias, List, Tuple, Dict, Set, Any

# Types
RawInput          : TypeAlias = str
Position          : TypeAlias = Tuple[int,int]
NodeMatrix        : TypeAlias = List[List['Node']]
Frequencies       : TypeAlias = Dict[str,List['Node']]
ProgressStatistics: TypeAlias = Dict[str,str]


# Exceptions
class CustomException(Exception):
    """Define custom exceptions specific to the problem"""
    pass

# Global Constants
DEFAULT_INPUT: RawInput = """
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
""".strip('\n')

# Helper Functions
def get_input(use_official_data: bool = False) -> RawInput:
    """Returns either test data or data from input.txt"""
    input_data: RawInput = DEFAULT_INPUT
    if use_official_data:
        with open('input.txt', 'r') as file:
            input_data = file.read().strip('\n')
    return input_data

def rows_cols(matrix: List[List[Any]]) -> Tuple[int,int]:
    """Gets the rows and cols of a matrix"""
    # I could cache this, but it's not an intesive function
    # And I'd have to have a hashable input, that'd decrease readability
    return len(matrix),len(matrix[0])

def in_bounds(position: Position, matrix: List[List[Any]]) -> bool:
    """Checks if position is in the bounds of a matrix"""
    row , col  = position[0],position[1]
    rows, cols = rows_cols(matrix)
    return (0 <= row < rows) and (0 <= col < cols)

# Helper Classes
@dataclass
class Node:
    """Define core data structures needed for the problem"""
    # Properties
    value: str
    position: Position
    nodes: List['Node']
    owned_antinodes: Dict[Position,str]
    active_antinodes: Set[str]

    '''
    #......     Node-x-1            Node-x-2        Node-0,0      Node-6,6
    .......      - x                 - x             - .           - .
    ..x....      - (2,2)             - (4,4)         - (0,0)       - (6,6)
    .......      - [<nx2>]           - [<nx1>]       - None        - None
    ....x..      - {(0,0), x}        - {(6,6), x}    - {}          - {}
    .......      - []                - []            - [x]         - [x]
    ......#     antinode.pos = ???
    '''

    '''
    ......#     Node-x-1            Node-x-2        Node-0,6      Node-6,0
    .......      - x                 - x             - .           - .
    ....x..      - (2,4)             - (4,2)         - (0,6)       - (6,0)
    .......      - [<nx2>]           - [<nx1>]       - None        - None
    ..x....      - {(0,6), x}        - {(6,0), x}    - {}          - {}
    .......      - []                - []            - [x]         - [x]
    #......     antinode.pos = ???
    '''

    # Dunder Methods
    def __init__(self, value: str) -> None:
       self.value = value
       self.owned_antinodes = {}
       self.active_antinodes = set()

    def __str__(self) -> str:
        as_string = f'{self.value}'
        if as_string == '.' and len(self.active_antinodes) != 0: as_string = '#'
        return as_string

    # Public Methods
    def process(self) -> None:
        for node in self.nodes:
            x = Node._offset(self.position[0],node.position[0])
            y = Node._offset(self.position[1],node.position[1])
            # print(f'Node({self.position[0]},{self.position[1]}) with Node({node.position[0]},{node.position[1]}) has Antinode({x},{y})')
            self.owned_antinodes[(x,y)] = self.value

    def boost_process(self, matrix: List[List[Any]]) -> None:
        for node in self.nodes:
            a = node.position[0]                    # 2
            b = node.position[1]                    # 2
            x = Node._offset(self.position[0],a)    # 2+(2-0)=4
            y = Node._offset(self.position[1],b)    # 2+(2-0)=4
            while in_bounds((x,y),matrix):
                self.owned_antinodes[(x,y)] = self.value
                c,d = x,y                           # 4,4        6,6
                x = Node._offset(a,x)               # 4+(4-2)=6  6+(6-4)=8
                y = Node._offset(b,y)               # 4+(4-2)=6  6+(6-4)=8
                a,b = c,d                           # 4,4        6,6

    # Private Methods
    @staticmethod
    def _offset(a: int, b: int) -> int:
        return b + (b - a)

# Main Class
class Solver:
    # Dunder Methods
    def __init__(self, raw_input: RawInput) -> None:
        """Initialize solver with input data"""
        self.node_matrix = self._process_input(raw_input)

    def __str__(self) -> str:
        """String representation of current state"""
        as_string = ""
        rows, cols = rows_cols(self.node_matrix)
        for row,col in product(range(rows),range(cols)):
            as_string += f'{self.node_matrix[row][col]}' + ('\n' if col+1 == cols else '')
        return as_string

    # Public Methods
    def solve_part_one(self) -> int:
        """Solve part one of the problem"""
        node_matrix: NodeMatrix = deepcopy(self.node_matrix)
        self.node_matrix = Solver._activate_nodes(self.node_matrix)
        result = 0
        rows, cols = rows_cols(self.node_matrix)
        for row, col in product(range(rows),range(cols)):
            result += 1 if len(self.node_matrix[row][col].active_antinodes) != 0 else 0
        print(self,end='')
        self.node_matrix = node_matrix
        return result

    def solve_part_two(self) -> int:
        """Solve part two of the problem"""
        node_matrix: NodeMatrix = deepcopy(self.node_matrix)
        self.node_matrix = Solver._activate_boosted_nodes(self.node_matrix)
        result = 0
        rows, cols = rows_cols(self.node_matrix)
        for row, col in product(range(rows),range(cols)):
            result += 1 if len(self.node_matrix[row][col].active_antinodes) != 0 else 0
            if len(self.node_matrix[row][col].active_antinodes) == 0 and self.node_matrix[row][col].value != '.':
                result += 1
        print(self,end='')
        self.node_matrix = node_matrix
        return result

    # Private Methods
    @staticmethod
    def _inactive_node_matrix(raw_input: RawInput) -> NodeMatrix:
        return [[Node(value) for value in line] for line in raw_input.splitlines()]

    @staticmethod
    def _frequencies(node_matrix: NodeMatrix) -> Frequencies:
        frequencies: Frequencies = defaultdict(list)
        rows, cols = rows_cols(node_matrix)
        for row, col in product(range(rows),range(cols)):
            if node_matrix[row][col].value != '.':
                frequencies[node_matrix[row][col].value].append(node_matrix[row][col])
        return frequencies

    @staticmethod
    def _place_nodes(node_matrix: NodeMatrix) -> NodeMatrix:
        rows, cols = rows_cols(node_matrix)
        for row, col in product(range(rows),range(cols)):
            node_matrix[row][col].position = row, col
        return node_matrix

    @staticmethod
    def _connect_nodes(node_matrix: NodeMatrix, frequencies: Frequencies) -> NodeMatrix:
        rows, cols = rows_cols(node_matrix)
        for row, col in product(range(rows),range(cols)):
            if node_matrix[row][col].value != '.':
                node: Node = node_matrix[row][col]
                # We dont want to add a node to its own list of nodes
                node.nodes = [n for n in frequencies[node.value] if node.position != n.position]
                node_matrix[row][col] = node
        return node_matrix

    @staticmethod
    def _activate_nodes(node_matrix: NodeMatrix) -> NodeMatrix:
        rows, cols = rows_cols(node_matrix)
        for row, col in product(range(rows),range(cols)):
            if node_matrix[row][col].value != '.':
                node_matrix[row][col].process()
                for antinode in node_matrix[row][col].owned_antinodes.items():
                    (x,y), value = antinode
                    if in_bounds((x,y), node_matrix):
                        node_matrix[x][y].active_antinodes.add(value)
        return node_matrix

    @staticmethod
    def _activate_boosted_nodes(node_matrix: NodeMatrix) -> NodeMatrix:
        rows, cols = rows_cols(node_matrix)
        for row, col in product(range(rows),range(cols)):
            if node_matrix[row][col].value != '.':
                node_matrix[row][col].boost_process(node_matrix)
                for antinode in node_matrix[row][col].owned_antinodes.items():
                    (x,y), value = antinode
                    if in_bounds((x,y), node_matrix):
                        node_matrix[x][y].active_antinodes.add(value)
        return node_matrix

    @staticmethod
    def _process_input(raw_input: RawInput) -> NodeMatrix:
        """Convert raw input into processed data structures"""
        node_matrix: NodeMatrix = Solver._inactive_node_matrix(raw_input)
        node_matrix = Solver._place_nodes(node_matrix)
        frequencies: Frequencies = Solver._frequencies(node_matrix)
        node_matrix = Solver._connect_nodes(node_matrix, frequencies)
        return node_matrix

# Execute
if __name__ == "__main__":
    print("Initialize Input Data...")
    input_data = get_input(use_official_data=True)
    print(input_data, end='\n\n')

    print("Initialize Solver...",end="\n\n")
    solver = Solver(input_data)

    print("Solve Part One...")
    part_one_solution = solver.solve_part_one()
    print(f"Solution: {part_one_solution}", end='\n\n')

    print("Solve Part Two...")
    part_two_solution = solver.solve_part_two()
    print(f"Solution: {part_two_solution}")
