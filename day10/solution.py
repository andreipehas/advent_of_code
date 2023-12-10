from contextlib import redirect_stdout
from pathlib import Path
from typing import List, Tuple

INPUT_NAME = "input.txt"

NORTH = (-1, 0)
SOUTH = (1, 0)
EAST  = (0, 1)
WEST  = (0, -1)
DIRECTIONS = {
    "S": [NORTH, SOUTH, EAST, WEST],
    "F": [SOUTH, EAST],
    "7": [SOUTH, WEST],
    "J": [NORTH, WEST],
    "L": [NORTH, EAST],
    "|": [NORTH, SOUTH],
    "-": [EAST, WEST],
    ".": [],
    }

def valid_coordinates(size: int, x: int, y: int) -> bool:
   return 0 <= x and x < size and 0 <= y and y < size

def valid_transition(target_symbol: str, reverse_direction: Tuple[int, int]) -> bool:
    return reverse_direction in DIRECTIONS[target_symbol]

def bfs(lines: List[List[str]], x: int, y: int) -> int:
    explore_queue = []
    steps = [[float("inf")] * len(lines) for _ in range(len(lines))]
    steps[x][y] = 0
    sol = float("inf")

    # north valid start?
    if valid_coordinates(len(lines), x-1, y) and (lines[x-1][y] == "F" or lines[x-1][y] == "7" or lines[x-1][y] == '|'):
        explore_queue.append((x-1, y))
        steps[x-1][y] = 1

    # south valid start?
    if valid_coordinates(len(lines), x+1, y) and (lines[x+1][y] == "J" or lines[x+1][y] == "L" or lines[x+1][y] == '|'):
        explore_queue.append((x+1, y))
        steps[x+1][y] = 1

    # east valid start?
    if valid_coordinates(len(lines), x, y+1) and (lines[x][y+1] == "7" or lines[x][y+1] == "J" or lines[x][y+1] == '-'):
        explore_queue.append((x, y+1))
        steps[x][y+1] = 1

    # west valid start?
    if valid_coordinates(len(lines), x, y-1) and (lines[x][y-1] == "L" or lines[x][y-1] == "F" or lines[x][y-1] == '-'):
        explore_queue.append((x, y-1))
        steps[x][y-1] = 1

    # traverse the array
    for (x, y) in explore_queue:
        for dx, dy in DIRECTIONS[lines[x][y]]:
            if (
                valid_coordinates(len(lines), x + dx, y + dy) and
                valid_transition(lines[x+dx][y+dy], (-dx, -dy))
            ):
                if steps[x+dx][y+dy] == steps[x][y] + 1:
                    sol = min(sol, steps[x][y] + 1)
                if steps[x+dx][y+dy] == float("inf"):
                    steps[x+dx][y+dy] = steps[x][y] + 1
                    explore_queue.append((x+dx, y+dy))
            
    
    return sol

if __name__ == "__main__":
    script_dir = Path(__file__).resolve().parent
    file_path = script_dir / INPUT_NAME
    sol = 0

    with open(script_dir / 'output.txt', 'w') as f:
      with redirect_stdout(f):
        with open(file_path, 'r') as file:
            lines = [line.rstrip() for line in file]
            for i in range(len(lines)):
                j = lines[i].find('S')
                if j >= 0:
                    start_coordinates = (i, j)
                    break
            
            sol = bfs(lines, *start_coordinates)

        print(f"------> {sol}")