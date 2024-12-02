from random import randint
from typing import List, Tuple, TypeAlias

'''
We'll be getting a Raw String
"1,2,3,4,5,6,7 | 1,2,3"

EncodedTransmission is the left-side
TransmissionDecoder is the right-side
ProcessedTransmission is just so we can work with the data easier
'''
# Types
RawTransmission      : TypeAlias = str
EncodedTransmission  : TypeAlias = List[int]
TransmissionDecoder  : TypeAlias = List[int]
Transmission         : TypeAlias = Tuple[
    EncodedTransmission,
    TransmissionDecoder
]

# Constants
TRANSMISSION_FILE: str = 'input.txt'
ENCODED_DATA_MAX: int  = 7

'''
This is not in the scope of the question.
I added it to give me more robust and varied examples
'''
# Step 0 - Generate New Test Data
def list_to_basic(list: List) -> str:
    '''
    Get a list:   [1,2,3]
    Return a str: "1,2,3"
    '''
    return str(list).strip('[').strip(']').replace(' ','')

def generate_encoded_transmission() -> EncodedTransmission:
    '''Generates an Encoded Transmission with values between 1-9'''
    return [randint(1,9) for _ in range(0,ENCODED_DATA_MAX)]

def generate_transmission_decoder() -> TransmissionDecoder:
    '''Generates Transmission Decoder and validates it before returning it'''
    transmission_decoder: TransmissionDecoder = []
    while sum(transmission_decoder) > ENCODED_DATA_MAX or len(transmission_decoder) == 0:
        transmission_decoder = [randint(1,3) for _ in range(0,randint(0,3))]
    return transmission_decoder

def generate_raw_transmission() -> RawTransmission:
    '''
    Generate a raw transmission...
    "1,2,3,4,5,6,7 | 1,2,3"
    '''
    return f'{list_to_basic(generate_encoded_transmission())} | {list_to_basic(generate_transmission_decoder())}'

def populate_new_test_data() -> None:
    '''Overwrite the input.txt file with new test data'''
    with open(TRANSMISSION_FILE,'w') as file:
        for _ in range(0,4):
            file.write(generate_raw_transmission()+'\n')

# Step 1 - Retrieve Transmissions
def retrieve_transmissions() -> List[RawTransmission]:
    '''Read the input file and get the transmissions as a list'''
    raw_transmissions: List[RawTransmission] = []
    with open('input.txt','r') as file:
        for raw_transmission in file.read().split('\n'):
            raw_transmissions.append(raw_transmission)
    # Added a filter to remove empty lines
    return [raw_transmission for raw_transmission in raw_transmissions if raw_transmission != '']

# Step 2 - Convert Raw Transmission into Useable Format
def parse_raw_transmissions(raw_transmissions: List[RawTransmission]) -> List[Transmission]:
    '''Take in a list of raw transmissions and parse them into useable data'''
    transmissions: List[Transmission] = []
    for raw_transmission in raw_transmissions:
        encoded_transmission_raw, transmission_decoder_raw = raw_transmission.split(" | ")
        encoded_transmission = [int(number) for number in encoded_transmission_raw.split(",")]
        transmission_decoder = [int(number) for number in transmission_decoder_raw.split(",")]
        transmissions.append((encoded_transmission,transmission_decoder))
    return transmissions

# Step 3 - Apply the Decoder
def decode_transmission(transmission: Transmission) -> int:
    '''
    Seperate the encoded transmission up by chunks dictated by the decoder.
    Sum all of the differences between the highest and lowest of the chunk.
    '''
    encoded_transmission, transmission_decoder = transmission
    transmission_index = 0
    transmission_value = 0
    for chunk_size in transmission_decoder:
        chunk = encoded_transmission[transmission_index:transmission_index+chunk_size]
        transmission_index += chunk_size
        transmission_value += max(chunk) - min(chunk)
    return transmission_value


if __name__ == "__main__":
    # Make/Display New Test Data
    populate_new_test_data()
    print("Raw Data...")
    with open(TRANSMISSION_FILE,'r') as file:
        print(file.read())

    # Retrieve the Raw Transmissions
    raw_transmissions = retrieve_transmissions()
    print("Retrieving raw transmissions...")
    print(raw_transmissions,end="\n\n")

    # Parse the Raw Transmissions
    transmissions = parse_raw_transmissions(raw_transmissions)
    print("Parsing raw transmissions...")
    print(transmissions,end="\n\n")

    # Get Decoded Values
    transmission_values = [decode_transmission(transmission) for transmission in transmissions]
    print("Successfully Decoded!")
    for index, value in enumerate(transmission_values):
        print(f'Transmission {index+1}: {value}')
