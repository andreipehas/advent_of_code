from contextlib import redirect_stdout
from pathlib import Path
from tqdm import tqdm
from typing import List

INPUT_NAME = "input.txt"
CYCLE_COUNT = 1000000000 - 1

def move_col_north(lines: List[List[str]], col_idx: int) -> None:
    next_pos = -1

    for line_idx in range(len(lines)):
        if lines[line_idx][col_idx] == 'O':
            next_pos = next(
               (
                  i
                  for i in range(next_pos + 1, line_idx)
                  if lines[i][col_idx] == '.'
                ), 
                line_idx
            )
            lines[line_idx][col_idx] = '.'
            lines[next_pos][col_idx] = 'O'
        elif lines[line_idx][col_idx] == '#':
            next_pos = line_idx

def move_col_south(lines: List[List[str]], col_idx: int) -> None:
    next_pos = len(lines)

    for line_idx in reversed(range(len(lines))):
        if lines[line_idx][col_idx] == 'O':
            next_pos = next(
               (
                  i
                  for i in reversed(range(line_idx, next_pos))
                  if lines[i][col_idx] == '.'
                ), 
                line_idx
            )
            lines[line_idx][col_idx] = '.'
            lines[next_pos][col_idx] = 'O'
        elif lines[line_idx][col_idx] == '#':
            next_pos = line_idx

def move_line_west(line: List[str]) -> None:
    next_pos = -1

    for col_idx in range(len(line)):
        if line[col_idx] == 'O':
            next_pos = next(
               (
                  i
                  for i in range(next_pos + 1, col_idx)
                  if line[i] == '.'
                ), 
                col_idx
            )
            line[col_idx] = '.'
            line[next_pos] = 'O'
        elif line[col_idx] == '#':
            next_pos = col_idx

def move_line_east(line: List[str]) -> None:
    next_pos = len(line)

    for col_idx in reversed(range(len(line))):
        if line[col_idx] == 'O':
            next_pos = next(
               (
                  i
                  for i in reversed(range(col_idx, next_pos))
                  if line[i] == '.'
                ), 
                col_idx
            )
            line[col_idx] = '.'
            line[next_pos] = 'O'
        elif line[col_idx] == '#':
            next_pos = col_idx

def score(lines: List[List[str]]) -> int:
    return sum(
        len(lines) - i
        if lines[i][j] == 'O'
        else 0
        for i in range(len(lines))
        for j in range(len(lines[0]))
    )

def cycle_once(lines: List[str]) -> None:
    for i in range(len(lines[0])):
        move_col_north(lines, i)

    for i in range(len(lines)):
        move_line_west(lines[i])

    for i in range(len(lines[0])):
        move_col_south(lines, i)

    for i in range(len(lines)):
        move_line_east(lines[i])
    
    return lines

def cycle(lines: List[List[str]], count: int) -> List[List[str]]:
    prev_seen = {}
    
    for it_count in tqdm(range(count)):
        cycle_once(lines)

        hash_key = hash(str(lines))
        if hash_key in prev_seen:
            print(f"CYCLE DETECTED: {prev_seen[hash_key]} and {it_count} are identical")
            break
        prev_seen[hash_key] = it_count
    
    steps_remaining = (CYCLE_COUNT - it_count) % (it_count - prev_seen[hash_key])
    for _ in tqdm(range(steps_remaining)):
        cycle_once(lines)

    return lines

if __name__ == "__main__":
    script_dir = Path(__file__).resolve().parent
    file_path = script_dir / INPUT_NAME

    sol = 0

    with open(script_dir / 'output.txt', 'w') as f:
      with redirect_stdout(f):
        with open(file_path, 'r') as file:
            lines = [list(line.rstrip()) for line in file]
            cycle(lines, CYCLE_COUNT)
            sol = score(lines)

        print(f"------> {sol}")