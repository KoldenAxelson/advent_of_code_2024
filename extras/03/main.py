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
