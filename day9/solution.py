from contextlib import redirect_stdout
from pathlib import Path
import re
from typing import List

INPUT_NAME = "input.txt"

def solve(line: List[int]) -> int:
    print(line)
    if all(element == line[0] for element in line):
        return line[0]

    new_line = [line[i] - line[i-1] for i in range(1, len(line))]
    
    return line[-1] + solve(new_line)


if __name__ == "__main__":
    script_dir = Path(__file__).resolve().parent
    file_path = script_dir / INPUT_NAME
    sol = 0

    with open(script_dir / 'output.txt', 'w') as f:
      with redirect_stdout(f):
        with open(file_path, 'r') as file:
            lines = [line.rstrip() for line in file]
            for line in lines:
               current_line = [int(x) for x in re.findall("[\-0-9]+", line)]
               current_sol = solve(current_line)
               print(f">{current_sol}")
               sol += current_sol

        print(f"------> {sol}")