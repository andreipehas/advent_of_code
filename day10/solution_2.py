# TODO: make sneaking between pipes valid

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

def valid_coordinates(size_x: int, size_y: int, x: int, y: int) -> bool:
   return 0 <= x and x < size_x and 0 <= y and y < size_y

def valid_transition(target_symbol: str, reverse_direction: Tuple[int, int]) -> bool:
    return reverse_direction in DIRECTIONS[target_symbol]

def bfs(lines: List[List[str]], x: int, y: int) -> Tuple[List[List[str]], Tuple[str, str]]:
    explore_queue = []
    steps = [[None] * len(lines[0]) for _ in range(len(lines))]
    steps[x][y] = 'X'

    # north valid start?
    if valid_coordinates(len(lines), len(lines[0]), x - 1, y) and valid_transition(lines[x-1][y], (1, 0)):
        steps[x-1][y] = 'N'
        explore_queue.append((x - 1, y))

    # south valid start?
    if valid_coordinates(len(lines), len(lines[0]), x + 1, y) and valid_transition(lines[x+1][y], (-1, 0)):
        steps[x+1][y] = 'S'
        explore_queue.append((x + 1, y))

    # east valid start?
    if valid_coordinates(len(lines), len(lines[0]), x, y+1) and valid_transition(lines[x][y+1], (0, -1)):
        steps[x][y+1] = 'E'
        explore_queue.append((x, y + 1))

    # west valid start?
    if valid_coordinates(len(lines), len(lines[0]), x, y-1) and valid_transition(lines[x][y-1], (0, 1)):
        steps[x][y-1] = 'W'
        explore_queue.append((x, y - 1))

    # traverse the array
    while explore_queue:
        x, y = explore_queue.pop(0)
        for dx, dy in DIRECTIONS[lines[x][y]]:
            if (
                valid_coordinates(len(lines), len(lines[0]), x + dx, y + dy) and
                valid_transition(lines[x+dx][y+dy], (-dx, -dy))
            ):
                if steps[x+dx][y+dy] and steps[x+dx][y+dy] != 'X' and steps[x+dx][y+dy] != steps[x][y]:
                    return steps, (steps[x][y], steps[x+dx][y+dy])
                if not steps[x+dx][y+dy]:
                    steps[x+dx][y+dy] = steps[x][y]
                    explore_queue.append((x+dx, y+dy))

    return -1

def flood_fill(
        steps: List[List[int]],
        x: int,
        y: int,
        symbols: Tuple[str, str]
    ) -> None:
    explore_queue = [(x, y)]

    while explore_queue:
        x, y = explore_queue.pop(0)
        for dx, dy in DIRECTIONS["S"]:
            if (
                valid_coordinates(len(lines), len(lines[0]), x + dx, y + dy)
                and not steps[x + dx][y + dy] in symbols
            ):
                steps[x + dx][y + dy] = symbols[0]
                explore_queue.append((x + dx, y + dy))

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
            
            steps, symbols = bfs(lines, *start_coordinates)

            for i in range(len(lines)):
                if not lines[i][0] in symbols:
                    flood_fill(steps, i, 0, symbols)

                if not lines[i][len(lines) - 1] in symbols:
                    flood_fill(steps, i, len(lines[0]) - 1, symbols)

            for i in range(len(lines[0])):
                if not lines[0][i] in symbols:
                    flood_fill(steps, 0, i, symbols)

                if not lines[len(lines) - 1][i] in symbols:
                    flood_fill(steps, len(lines) - 1, i, symbols)

            sol = sum(step.count(None) for step in steps)
                
        print(f"------> {sol}")