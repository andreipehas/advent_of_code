from collections import Counter
from contextlib import redirect_stdout
from pathlib import Path
from typing import List, Tuple

INPUT_NAME = "input.txt"

def is_five_of_a_kind(tally: List[Tuple[int, int]], joker_count) -> bool:
   return joker_count == 5 or tally[0][1] + joker_count == 5

def is_four_of_a_kind(tally: List[Tuple[int, int]], joker_count) -> bool:
   return joker_count == 4 or tally[0][1] + joker_count == 4

def is_full_house(tally: List[Tuple[int, int]], joker_count) -> bool:
   return len(tally) >= 2 and tally[0][1] + tally[1][1] + joker_count == 5

def is_three_of_a_kind(tally: List[Tuple[int, int]], joker_count) -> bool:
   return joker_count == 3 or tally[0][1] + joker_count == 3

def is_two_pair(tally: List[Tuple[int, int]], joker_count) -> bool:
   return len(tally) >= 2 and tally[0][1] + tally[1][1] + joker_count == 4

def is_one_pair(tally: List[Tuple[int, int]], joker_count) -> bool:
   return joker_count == 2 or tally[0][1] + joker_count == 2

def determine_type(hand: str) -> int:
    c = Counter(hand)
    joker_count = c['1']
    del c['1']
    tally = c.most_common(5)

    if is_five_of_a_kind(tally, joker_count):
       return 6
    
    if is_four_of_a_kind(tally, joker_count):
       return 5
    
    # Full house?
    if is_full_house(tally, joker_count):
       return 4
    
    # Three of a kind?
    if is_three_of_a_kind(tally, joker_count):
       return 3
    
    # Two pair?
    if is_two_pair(tally, joker_count):
       return 2
    
    # One pair?
    if is_one_pair(tally, joker_count):
       return 1
    
    # high card?
    return 0

def transform_hand(hand: str) -> str:
    hand = hand.replace('J', '1')
    hand = hand.replace('T', 'a')
    #hand = hand.replace('J', 'b')
    hand = hand.replace('Q', 'c')
    hand = hand.replace('K', 'd')
    hand = hand.replace('A', 'e')

    return hand

def unscrample_hand(hand: str) -> str:
    hand = hand.replace('1', 'J')
    hand = hand.replace('a', 'T')
    #hand = hand.replace('b', 'J')
    hand = hand.replace('c', 'Q')
    hand = hand.replace('d', 'K')
    hand = hand.replace('e', 'A')

    return hand

if __name__ == "__main__":
    script_dir = Path(__file__).resolve().parent
    file_path = script_dir / INPUT_NAME

    sol = 0

    with open(script_dir / 'output.txt', 'w') as f:
      with redirect_stdout(f):
        with open(file_path, 'r') as file:
            lines = [line.rstrip() for line in file]
            types = [[] for _ in range(7)]

            # There's no duplicates in the input, so a hand maps to a single bid
            mapping = {}

            for line in lines:
                hand, bid = line.split()
                hand = transform_hand(hand)
                mapping[hand] = int(bid)
                idx  = determine_type(hand)
                types[idx].append(hand)
            
            i = 0
            for type in types:
                for hand in sorted(type):
                    i += 1
                    print(i, unscrample_hand(hand), mapping[hand])
                    sol += i * mapping[hand]
                    del mapping[hand]
                print("NEXT")
            
        print(f"------> {sol}")