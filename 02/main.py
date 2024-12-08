from random import randint
from typing import TypeAlias, List, Tuple

Report      : TypeAlias = List[int]
ReportResult: TypeAlias = Tuple[bool,str]

def randbool() -> bool:
    return randint(0,1) == 1

def make_report() -> Report:
    report: List[int] = [randint(0,9) for _ in range(0,5)]
    if randbool():
        report.sort(reverse=randbool())
    return report

def get_official_reports() -> List[Report]:
    reports: List[List[int]] = []
    raw_input: str = ""
    with open("input.txt",'r') as file:
        raw_input = file.read().strip("\n")
    raw_lines: List[str] = raw_input.splitlines()
    for line in raw_lines:
        report = [int(num) for num in line.split()]
        reports.append(report)
    return reports

def int_to_at_most(n:int) -> str:
    match n:
        case 1: return "1"
        case 2: return "1 or 2"
        case 3: return "1, 2, or 3"
        case _: return ""

def check_report(report: Report) -> ReportResult:
    biggest_change = 0
    is_rising = report[0] < report[1]
    for i, n in enumerate(report):
        if i == len(report) - 1: break
        if n == report[i+1]:                  return (False, f"Unsafe:\t[{n}, {report[i+1]}] is neither an increase or a decrease.")
        if n > report[i+1] and     is_rising: return (False, f"Unsafe:\t[{report[0]}, {report[1]}] is increasing but [{n}, {report[i+1]}] is decreasing.")
        if n < report[i+1] and not is_rising: return (False, f"Unsafe:\t[{report[0]}, {report[1]}] is decreasing but [{n}, {report[i+1]}] is increasing.")
        change = abs(n-report[i+1])
        if change > 3:                        return (False, f"Unsafe:\t[{n}, {report[i+1]}] is {'an increase' if is_rising else 'a decrease'} of {change}")
        biggest_change = change if change > biggest_change else biggest_change
    return (True, f"Safe:\tthe levels are all {'increasing' if is_rising else 'decreasing'} by {int_to_at_most(biggest_change)}.")

def check_report_with_dampener(report: Report) -> ReportResult:
    """Check if a report is safe either as-is or with one number removed"""

    # First check if it's safe without any removals
    base_check = check_report(report)
    if base_check[0]:
        return base_check

    # If not safe, try removing each number one at a time
    for i in range(len(report)):
        # Create new sequence without the current number
        dampened = report[:i] + report[i+1:]
        dampened_check = check_report(dampened)
        if dampened_check[0]:
            return (True, f"Safe with dampener removing position {i}")

    return (False, "Unsafe even with dampener")

# reports = [make_report() for _ in range(0,9)]
reports: List[Report] = get_official_reports()
for report in reports:
    print(f'{str(report).ljust(50)}\t{check_report(report)[1]}')

print(f'\nTotal Safe Reports: {sum([1 for report in reports if check_report(report)[0]])}')

safe_count = sum(1 for report in reports if check_report_with_dampener(report)[0])
print(f"Total safe reports with dampener: {safe_count}")
