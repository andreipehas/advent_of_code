from contextlib import redirect_stdout
from pathlib import Path
import re
from typing import Dict, Tuple

INPUT_NAME = "input.txt"

def walk(path: str, graph: Dict[str, Tuple[str, str]]) -> int:
    i = 0
    state = 'AAA'
    while state != "ZZZ":
        if path[i % len(path)] == 'L':
            state = graph[state][0]
        else:
            state = graph[state][1]
        i += 1
    
    return i

if __name__ == "__main__":
    script_dir = Path(__file__).resolve().parent
    file_path = script_dir / INPUT_NAME

    sol = 0
    states = {}

    with open(script_dir / 'output.txt', 'w') as f:
      with redirect_stdout(f):
        with open(file_path, 'r') as file:
            lines = [line.rstrip() for line in file]
            for line in lines[2:]:
               matches = re.findall("[A-Z]+", line)
               states[matches[0]] = (matches[1], matches[2])
            
            sol = walk(lines[0], states)

        print(f"------> {sol}")