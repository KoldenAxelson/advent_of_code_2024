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

def _get_official_input() -> CorruptedData:
    corrupt_data: CorruptedData = ""
    with open("input.txt",'r') as file:
        corrupt_data = file.read().strip('\n')
    return corrupt_data

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
    def _is_valid_section(section: str, full_context: str, start_idx: int) -> bool:
        # Check if this is actually a valid mul() instruction
        if full_context[start_idx-4:start_idx] != "mul(":
            return False

        # We're only passing strings that should look like XXX,YYY
        if not "," in section: return False
        split_section = section.split(',')
        if len(split_section) != 2: return False
        if len(split_section[0]) > 3: return False
        if len(split_section[1]) > 3: return False
        if not split_section[0].isdigit(): return False
        if not split_section[1].isdigit(): return False
        return True

    @staticmethod
    def _uncorrupt_data(corrupted_data: CorruptedData) -> UncorruptedData:
        uncorrupted_data: UncorruptedData = []
        # "mul(0,0)" is 8 characters
        # CorruptedData less than 8 characters is all junk data
        if len(corrupted_data) < 8: return uncorrupted_data

        # Get "mul(XXX,YYY)" Section
        idx_a = corrupted_data.find("mul(")
        if idx_a == -1: return uncorrupted_data

        # Find the next closing parenthesis
        idx_b = corrupted_data.find(")", idx_a)
        if idx_b == -1: return uncorrupted_data

        section = corrupted_data[idx_a+4:idx_b]

        # Validate and Recurse
        # Depending on if a valid solution is found we set the next search index
        if DataSolver._is_valid_section(section, corrupted_data, idx_a+4):
            uncorrupted_data.append(section)
            new_idx = idx_b + 1
        else:
            new_idx = idx_a + 4

        remaining_data = DataSolver._uncorrupt_data(corrupted_data[new_idx:])
        uncorrupted_data.extend(remaining_data)
        return uncorrupted_data

    @staticmethod
    def _parse_arguments(uncorrupted_data: UncorruptedData) -> ParsedArguments:
        # Data has been validated so it's clear to make assumptions
        return [(int(section.split(',')[0]),int(section.split(',')[1])) for section in uncorrupted_data]

# Execution
if __name__ == "__main__":
    print("Input Data...")
    input_data: CorruptedData = _get_official_input()
    print(input_data,end='\n\n')

    print("Data Solver...")
    data_solver: DataSolver = DataSolver(input_data)
    print(data_solver,end='\n\n')

    print("Solution: ",end="")
    print(data_solver.solution(),end="\n\n")
