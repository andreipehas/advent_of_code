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
    explore_queue = [(x,y)]
    steps = [[float("inf")] * len(lines) for _ in range(len(lines))]
    steps[x][y] = 0

    # traverse the array
    while explore_queue:
        x, y = explore_queue.pop(0)
        for dx, dy in DIRECTIONS[lines[x][y]]:
            if (
                valid_coordinates(len(lines), x + dx, y + dy) and
                valid_transition(lines[x+dx][y+dy], (-dx, -dy))
            ):
                if steps[x+dx][y+dy] == steps[x][y] + 1:
                    return steps[x][y] + 1
                if steps[x+dx][y+dy] == float("inf"):
                    steps[x+dx][y+dy] = steps[x][y] + 1
                    explore_queue.append((x+dx, y+dy))

    return float("inf")

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