from contextlib import redirect_stdout
from pathlib import Path
from typing import List

INPUT_NAME = "input.txt"

def move_col_north(lines: List[str], col: int) -> int:
    sol = 0
    next_pos = -1

    for line_idx in range(len(lines)):
        if lines[line_idx][col] == 'O':
            next_pos = next(
               (
                  i
                  for i in range(next_pos + 1, line_idx)
                  if lines[i][col] == '.'
                  or lines[i][col] == 'O'
                ), 
                line_idx
            )
            sol += len(lines) - next_pos
            print(f"O spotted at {next_pos}, {col} -> adding {len(lines) - next_pos}")
        elif lines[line_idx][col] == '#':
            next_pos = line_idx

    return sol

if __name__ == "__main__":
    script_dir = Path(__file__).resolve().parent
    file_path = script_dir / INPUT_NAME

    sol = 0

    with open(script_dir / 'output.txt', 'w') as f:
      with redirect_stdout(f):
        with open(file_path, 'r') as file:
            lines = [line.rstrip() for line in file]
            for i in range(len(lines[0])):
               sol += move_col_north(lines, i)

        print(f"------> {sol}")