'''
--- Day 5: Print Queue ---

Satisfied with their search on Ceres, the squadron of scholars suggests subsequently scanning the stationery stacks of sub-basement 17.

The North Pole printing department is busier than ever this close to Christmas, and while The Historians continue their search of this historically significant facility, an Elf operating a very familiar printer beckons you over.

The Elf must recognize you, because they waste no time explaining that the new sleigh launch safety manual updates won't print correctly. Failure to update the safety manuals would be dire indeed, so you offer your services.

Safety protocols clearly indicate that new pages for the safety manuals must be printed in a very specific order. The notation X|Y means that if both page number X and page number Y are to be produced as part of an update, page number X must be printed at some point before page number Y.

The Elf has for you both the page ordering rules and the pages to produce in each update (your puzzle input), but can't figure out whether each update has the pages in the right order.

For example:

47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47

The first section specifies the page ordering rules, one per line. The first rule, 47|53, means that if an update includes both page number 47 and page number 53, then page number 47 must be printed at some point before page number 53. (47 doesn't necessarily need to be immediately before 53; other pages are allowed to be between them.)

The second section specifies the page numbers of each update. Because most safety manuals are different, the pages needed in the updates are different too. The first update, 75,47,61,53,29, means that the update consists of page numbers 75, 47, 61, 53, and 29.

To get the printers going as soon as possible, start by identifying which updates are already in the right order.

In the above example, the first update (75,47,61,53,29) is in the right order:

75 is correctly first because there are rules that put each other page after it: 75|47, 75|61, 75|53, and 75|29.
47 is correctly second because 75 must be before it (75|47) and every other page must be after it according to 47|61, 47|53, and 47|29.
61 is correctly in the middle because 75 and 47 are before it (75|61 and 47|61) and 53 and 29 are after it (61|53 and 61|29).
53 is correctly fourth because it is before page number 29 (53|29).
29 is the only page left and so is correctly last.
Because the first update does not include some page numbers, the ordering rules involving those missing page numbers are ignored.

The second and third updates are also in the correct order according to the rules. Like the first update, they also do not include every page number, and so only some of the ordering rules apply - within each update, the ordering rules that involve missing page numbers are not used.

The fourth update, 75,97,47,61,53, is not in the correct order: it would print 75 before 97, which violates the rule 97|75.

The fifth update, 61,13,29, is also not in the correct order, since it breaks the rule 29|13.

The last update, 97,13,75,29,47, is not in the correct order due to breaking several rules.

For some reason, the Elves also need to know the middle page number of each update being printed. Because you are currently only printing the correctly-ordered updates, you will need to find the middle page number of each correctly-ordered update. In the above example, the correctly-ordered updates are:

75,47,61,53,29
97,61,53,29,13
75,29,13
These have middle page numbers of 61, 53, and 29 respectively. Adding these page numbers together gives 143.

Of course, you'll need to be careful: the actual list of page ordering rules is bigger and more complicated than the above example.

Determine which updates are already in the correct order. What do you get if you add up the middle page number from those correctly-ordered updates?
'''
'''
Simplified Question...

1.) Get a Raw String of Data
2.) Format by 2 Sections
3.) Section 1 PageRules
4.) Section 2 PageOrders
5.) Use PageRules to determine valid/invalid PageOrders
6.) Sum the middle value of each PageOrder

1|2 <== 1 comes before 2
3|4
5|6

1,2,3
4,5,6
6,5,4 <== Invalid: Omit

2+5 = 7
'''

# Imports
from typing import TypeAlias, Tuple, List, Optional

# Types
RawPageData  : TypeAlias = str
RawPageRules : TypeAlias = str
RawPageOrders: TypeAlias = str
RawSections  : TypeAlias = Tuple[RawPageRules,RawPageOrders]
PageRule     : TypeAlias = Tuple[int,int]
PageOrder    : TypeAlias = List[int]
PageRules    : TypeAlias = List[PageRule]
PageOrders   : TypeAlias = List[PageOrder]

# Global Constants
DEFAULT_INPUT: RawPageData = """
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
""".strip('\n')

# Classes
class Solver():
    # Dunder Methods
    def __init__(self, raw_page_data: RawPageData) -> None:
        raw_sections    : RawSections = Solver._raw_sections(raw_page_data)
        self.page_rules : PageRules   = Solver._page_rules(raw_sections[0])
        self.page_orders: PageOrders = Solver._page_orders(raw_sections[1])

    # Public Methods
    # PART ONE
    def check(self, page_order: PageOrder, page_rule: PageRule) -> Optional[bool]:
        try:
            rule_before_idx: int = page_order.index(page_rule[0])
            rule_after_idx : int = page_order.index(page_rule[1])
            return rule_before_idx < rule_after_idx
        except ValueError:
            # We know most rules wont apply to each order
            return None

    def validate(self, page_order: PageOrder) -> bool:
        for page_rule in self.page_rules:
            match self.check(page_order, page_rule):
                case True : continue
                case False: return False
                case _    : continue # Handles None and the Unexpected
        return True

    def valid_orders(self) -> PageOrders:
        valid_orders: PageOrders = []
        for page_order in self.page_orders:
            if self.validate(page_order):
                valid_orders.append(page_order)
        return valid_orders

    def solve_part_one(self) -> None:
        solved_sum = 0
        for valid_order in self.valid_orders():
            idx = len(valid_order) // 2
            solved_sum += valid_order[idx]
        print(f'Solved 1: {solved_sum}')

    # PART 2
    def invalid_orders(self) -> PageOrders:
        invalid_orders: PageOrders = []
        for page_order in self.page_orders:
            if not self.validate(page_order):
                invalid_orders.append(page_order)
        return invalid_orders

    def fix_order(self, page_order: PageOrder) -> None:
        made_change = True
        while made_change:
            made_change = False
            for page_rule in self.page_rules:
                try:
                    rule_before_idx: int = page_order.index(page_rule[0])
                    rule_after_idx : int = page_order.index(page_rule[1])
                    if rule_before_idx > rule_after_idx:
                        page_order[rule_before_idx],page_order[rule_after_idx] = page_order[rule_after_idx],page_order[rule_before_idx]
                        made_change = True
                        break
                except ValueError:
                    continue

    def solve_part_two(self) -> None:
        solved_sum = 0
        invalid_orders: PageOrders = self.invalid_orders()
        for invalid_order in invalid_orders:
            self.fix_order(invalid_order)
            idx = len(invalid_order) // 2
            solved_sum += invalid_order[idx]
        print(f'Solved 2: {solved_sum}')

    # Private Methods
    @staticmethod
    def _raw_sections(raw_page_data: RawPageData) -> RawSections:
        raw_sections = raw_page_data.split('\n\n')
        raw_page_rules: RawPageRules = raw_sections[0]
        raw_page_orders: RawPageOrders = raw_sections[1]
        return raw_page_rules,raw_page_orders

    @staticmethod
    def _page_rules(raw_page_rules: RawPageRules) -> PageRules:
        return [(int(line.split('|')[0]), int(line.split('|')[1])) for line in raw_page_rules.strip().splitlines()]

    @staticmethod
    def _page_orders(raw_page_orders: RawPageOrders) -> PageOrders:
        return [[int(num) for num in line.split(',')] for line in raw_page_orders.strip().splitlines()]

# Execute
if __name__ == "__main__":
    with open('input.txt','r') as file:
        print("Initialize Input...")
        input = file.read().strip('\n')
        # input = DEFAULT_INPUT
        print(input,end="\n\n")

        print("Initialize Solver...")
        solver: Solver = Solver(input)
        print(solver,end="\n\n")

        solver.solve_part_one()
        solver.solve_part_two()
