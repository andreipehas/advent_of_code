from contextlib import redirect_stdout
from math import gcd
from pathlib import Path
import re
from typing import Dict, Tuple

INPUT_NAME = "input.txt"

def walk(path: str, graph: Dict[str, Tuple[str, str]], state) -> int:
    i = 0
    while state[-1] != 'Z':
        if path[i % len(path)] == 'L':
            state = graph[state][0]
        else:
            state = graph[state][1]
        i += 1
    
    return i

def lcm(a: int, b: int) -> int:
   return a * b // gcd(a, b)

if __name__ == "__main__":
    script_dir = Path(__file__).resolve().parent
    file_path = script_dir / INPUT_NAME

    sol = 1
    states = {}
    start_states = []

    with open(script_dir / 'output.txt', 'w') as f:
      with redirect_stdout(f):
        with open(file_path, 'r') as file:
            lines = [line.rstrip() for line in file]
            for line in lines[2:]:
               matches = re.findall("[0-9A-Z]+", line)
               states[matches[0]] = (matches[1], matches[2])
               if matches[0][-1] == 'A':
                  start_states.append(matches[0])
            
            for state in start_states:
                current_sol = walk(lines[0], states, state)
                sol = lcm(sol, current_sol)

        print(f"------> {sol}")