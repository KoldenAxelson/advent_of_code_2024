"""
--- Day X: Elf Supply Chain ---

The elves at the North Pole have a complex supply chain system for their toy workshop.
Each toy component moves through different stations, and the elves need to optimize their
workflow.

The input is a series of lines, where each line represents a component's journey through
stations. Each station is represented by a letter, followed by the time (in minutes) spent
at that station in parentheses. Stations are separated by -> to show the path.

Example input:
A(5)->B(3)->D(2)
B(4)->C(6)->D(2)
A(3)->C(4)->B(1)

The elves need to know:
1. The longest possible path (in total minutes) any component takes
2. Which stations are "bottlenecks" (most used stations)

For the example above:
- Path 1 takes 10 minutes (5 + 3 + 2)
- Path 2 takes 12 minutes (4 + 6 + 2)
- Path 3 takes 8 minutes (3 + 4 + 1)
- The longest path is 12 minutes
- Station B and D appear in the most paths, making B and D bottlenecks

What is the sum of the longest path (in minutes) and the number of bottleneck stations?

For the example above, the answer would be 14 (12 + 2 bottleneck stations)
"""

from random import randint
from typing import TypeAlias, Set, List, Tuple, Dict

'''
We'll organize our types in order of our data processing pipeline
We're getting the Raw String, Convert it to a Dict, Handle it as a List.
'''
# Types
RawStation : TypeAlias = str
RawElfPath : TypeAlias = str
RawElfPaths: TypeAlias = str
Station    : TypeAlias = Tuple[str,int]
ElfPath    : TypeAlias = Dict[str,int]
ElfPaths   : TypeAlias = List[ElfPath]
PathData   : TypeAlias = Tuple[ElfPath,int]

# Global Constants
ELF_STATIONS    = ['A','B','C','D','E']
LENGTH_OF_PATH  = len(ELF_STATIONS) - 1
NUMBER_OF_PATHS = 3

'''
This is an additional step not detailed in the task
But this ensures we get a random set of data each time
Having this will make our solution more robust
'''
# Step 0 - Generate Test Data
def generate_path_indicies() -> Set[int]:
    '''Get a unique set of indecies for our Elf Path'''
    indicies: Set[int] = set()
    while len(indicies) < NUMBER_OF_PATHS:
        indicies.add(randint(0,LENGTH_OF_PATH))
    return indicies

def generate_raw_elf_path() -> RawElfPath:
    '''Generates a raw elf path with times between 1 and 9 minutes'''
    stations: List[str] = [f'{ELF_STATIONS[index]}({randint(1,9)})' for index in generate_path_indicies()]
    return "->".join(stations)

def generate_raw_elf_paths() -> RawElfPaths:
    '''Generates raw elf paths as a multi-line string'''
    raw_elf_paths = ""
    list_raw_elf_paths = [generate_raw_elf_path() for _ in range(0,NUMBER_OF_PATHS)]
    for raw_elf_path in list_raw_elf_paths:
        # Intentionally left in the trailing new_line character to handle messy data
        raw_elf_paths += f'{raw_elf_path}\n'
    return raw_elf_paths

'''
We want to take the raw data and format it like this
Each path is a dictionary to handle larger sizes to not slow performance
[
    {'A':1,'B':3,'C':5},
    {'B':1,'A':6,'D':2},
    {'C':6,'D':2,'A':6}
]
'''
# Step 1 - Parse the Data
def list_raw_elf_paths(raw_elf_paths: RawElfPaths) -> List[RawElfPath]:
    '''Get Raw Elf Paths into a List to handle the data'''
    return [raw_elf_path for raw_elf_path in raw_elf_paths.split('\n') if raw_elf_path != '']

def parse_raw_stations(raw_elf_path: RawElfPath) -> List[RawStation]:
    '''Get Raw Station into a List to handle the data'''
    return [raw_station for raw_station in raw_elf_path.split("->")]

def parse_raw_station(raw_station: RawStation) -> Station:
    '''Get Raw Elf Path into a Tuple to handle the data'''
    station_id = raw_station[0]
    minutes = int(raw_station[1::].strip("(").strip(")"))
    return (station_id, minutes)

def elf_path_from_stations(stations: List[Station]) -> ElfPath:
    '''Get Full Elf Path from Station List'''
    return {station[0]:station[1] for station in stations}

def parse_raw_elf_path(raw_elf_path: RawElfPath) -> ElfPath:
    '''Get Elf Path from Raw Data'''
    raw_stations: List[RawStation] = parse_raw_stations(raw_elf_path)
    stations:     List[Station]    = [parse_raw_station(raw_station) for raw_station in raw_stations]
    return elf_path_from_stations(stations)

def parse_raw_elf_paths(raw_elf_paths: RawElfPaths) -> ElfPaths:
    '''Get Elf Paths from Raw Data'''
    raw_elf_path_list: List[RawElfPath] = list_raw_elf_paths(raw_elf_paths)
    return [parse_raw_elf_path(raw_elf_path) for raw_elf_path in raw_elf_path_list]

'''
We've got to take this parsed data and...
1.) Find the bottlenecks
2.) Convert each path into a length
3.) Find the longest path
'''
# Step 2 - Get Answers from Data
def station_occurrences(elf_paths: ElfPaths) -> Dict[str,int]:
    '''Get a Dictionary of the sum of occurrences of each station.'''
    return {station:sum(1 for station_id in elf_paths if station in station_id) for station in ELF_STATIONS}

def get_bottleneck_stations(elf_paths: ElfPaths) -> List[str]:
    '''Get a List of the most occurring stations'''
    occurrences = station_occurrences(elf_paths)
    max_occurrences = max(occurrences.values())
    return [station for station, count in occurrences.items() if count == max_occurrences]

def get_path_data(elf_path: ElfPath, bottlenecks: List[str]) -> PathData:
    '''Sums up the minutes in each path, and adds a minute per bottleneck'''
    path_length = sum(elf_path.values())
    bottleneck_count = sum(1 for bottleneck in bottlenecks if bottleneck in elf_path)
    return (elf_path,path_length + bottleneck_count)

def get_paths_data(elf_paths: ElfPaths) -> List[PathData]:
    '''Get the Elf Paths as a list of Path Data'''
    bottlenecks: List[str] = get_bottleneck_stations(elf_paths)
    return [get_path_data(elf_path, bottlenecks) for elf_path in elf_paths]

def get_longest_path(elf_paths: ElfPaths) -> PathData:
    '''Gets the longest path out of all the Elf Paths'''
    return max(get_paths_data(elf_paths), key=lambda elf_path_data: elf_path_data[1])


# Execution
if __name__ == "__main__":
    raw_elf_paths = generate_raw_elf_paths()
    print("Raw Elf Paths...")
    print(raw_elf_paths)

    raw_elf_paths_list = list_raw_elf_paths(raw_elf_paths)
    print("List of Raw Elf Paths...")
    print(raw_elf_paths_list,end='\n\n')

    print("List of all Raw Stations...")
    for raw_elf_path in raw_elf_paths_list:
        print(parse_raw_stations(raw_elf_path))
    print("")

    print("List of all Parsed Stations...")
    for raw_elf_path in raw_elf_paths_list:
        for raw_station in parse_raw_stations(raw_elf_path):
            print(parse_raw_station(raw_station),end=" ")
        print("")
    print("")

    print("List all Elf Paths...")
    elf_paths = parse_raw_elf_paths(raw_elf_paths)
    for elf_path in elf_paths:
        print(elf_path)
    print("")

    print("Find all Bottlenecks...")
    print(get_bottleneck_stations(elf_paths))
    print("")

    print("Convert Elf Paths to Path Data...")
    for elf_path_data in get_paths_data(elf_paths):
        print(elf_path_data)
    print("")

    print("Find the longest path...")
    longest_path_data = get_longest_path(elf_paths)
    print(longest_path_data[0],end='\n\n')

    print(f"Final Answer: {longest_path_data[1]}")
