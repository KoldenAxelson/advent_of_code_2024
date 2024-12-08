from typing import TypeAlias, List, Tuple
from dataclasses import dataclass
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(message)s'
)
logger = logging.getLogger(__name__)

# Types
CorruptedData: TypeAlias = str
ParsedArguments: TypeAlias = List[Tuple[int, int]]

@dataclass
class Instruction:
    """Represents a found instruction in the input"""
    type: str  # 'mul', 'do', 'dont'
    position: int
    x: int | None = None  # Only for mul instructions
    y: int | None = None  # Only for mul instructions

    def __str__(self) -> str:
        if self.type == 'mul':
            return f"mul({self.x},{self.y}) at {self.position}"
        return f"{self.type}() at {self.position}"

    def result(self) -> int:
        """Calculate result for multiplication"""
        if self.type == 'mul' and self.x is not None and self.y is not None:
            return self.x * self.y
        return 0

class DataSolver:
    def __init__(self, corrupted_data: CorruptedData) -> None:
        # First find all valid instructions
        logger.debug("Finding all instructions...")
        self.instructions = self._find_all_instructions(corrupted_data)

        # Then process them in order
        logger.debug("\nProcessing instructions...")
        self.result = self._process_instructions()

    def solution(self) -> int:
        return sum(x * y for x, y in self.result)

    def _is_valid_mul(self, text: str, start: int) -> tuple[bool, tuple[int, int] | None]:
        """Check if this is a valid mul(X,Y) instruction"""
        # Must start with mul(
        if not text.startswith("mul(", start):
            return False, None

        # Find closing parenthesis
        try:
            close_idx = text.index(")", start + 4)
        except ValueError:
            return False, None

        # Get the content between parentheses
        content = text[start+4:close_idx]

        # Must contain exactly one comma
        if content.count(",") != 1:
            return False, None

        # Split into x and y parts
        try:
            x_str, y_str = content.split(",")

            # Validate the numbers
            if not (x_str.isdigit() and y_str.isdigit()):
                return False, None

            # Check length constraints (1-3 digits)
            if not (0 < len(x_str) <= 3 and 0 < len(y_str) <= 3):
                return False, None

            return True, (int(x_str), int(y_str))

        except ValueError:
            return False, None

    def _find_all_instructions(self, text: str) -> List[Instruction]:
        """Find all valid instructions in order"""
        instructions = []
        pos = 0

        while pos < len(text):
            # Look for specific instruction types
            if text.startswith("mul(", pos):
                valid, numbers = self._is_valid_mul(text, pos)
                if valid and numbers:
                    x, y = numbers
                    instructions.append(Instruction("mul", pos, x, y))
                    logger.debug(f"Found multiplication: mul({x},{y})")
                pos += 1
            elif text.startswith("don't()", pos) and (pos == 0 or not text[pos-1].isalpha()):
                instructions.append(Instruction("dont", pos))
                logger.debug(f"Found don't() at position {pos}")
                pos += 6
            elif text.startswith("do()", pos) and (pos == 0 or not text[pos-1].isalpha()):
                instructions.append(Instruction("do", pos))
                logger.debug(f"Found do() at position {pos}")
                pos += 4
            else:
                pos += 1

        return instructions

    def _process_instructions(self) -> ParsedArguments:
        """Process instructions in order, tracking state"""
        valid_muls: ParsedArguments = []
        enabled = True
        running_sum = 0

        logger.debug("\nProcessing sequence:")
        logger.debug("Starting state: enabled")

        for inst in self.instructions:
            if inst.type == "do":
                enabled = True
                logger.debug(f"State change -> enabled (do)")
            elif inst.type == "dont":
                enabled = False
                logger.debug(f"State change -> disabled (don't)")
            elif inst.type == "mul" and enabled:
                assert inst.x is not None and inst.y is not None
                valid_muls.append((inst.x, inst.y))
                running_sum += inst.result()
                logger.debug(f"VALID mul({inst.x},{inst.y}) = {inst.result()} (sum: {running_sum})")
            elif inst.type == "mul":  # mul but disabled
                assert inst.x is not None and inst.y is not None
                logger.debug(f"SKIP  mul({inst.x},{inst.y}) - disabled")

        logger.debug(f"\nFinal sum: {running_sum}")
        return valid_muls

def get_input() -> str:
    with open("input.txt", 'r') as file:
        return file.read().strip()

if __name__ == "__main__":
    input_data = get_input()
    solver = DataSolver(input_data)
    print("\nFinal Solution:", solver.solution())
