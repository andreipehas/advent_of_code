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

def traverse(
        explore_queue: List[Tuple[int, int]], 
        steps: List[List[int]], 
        xstop: int, 
        ystop: int
    ) -> bool:
    symbol = lines[xstop][ystop]

    for (x, y) in explore_queue:
        for dx, dy in DIRECTIONS[lines[x][y]]:
            if (valid_coordinates(len(lines), x + dx, y + dy) and valid_transition(lines[x+dx][y+dy], (-dx, -dy))):
                if x + dx == xstop and y + dy == ystop:
                    if (x, y) == explore_queue[0]:
                        continue
                    return True
                steps[x + dx][y + dy] = symbol
                explore_queue.append((x + dx, y + dy))
    
    return False

def bfs(lines: List[List[str]], x: int, y: int) -> str:
    steps = [[float("inf")] * len(lines) for _ in range(len(lines))]

    # north valid start?
    if valid_coordinates(len(lines), x-1, y) and (lines[x-1][y] == "F" or lines[x-1][y] == "7" or lines[x-1][y] == '|'):
        steps[x][y] = 'N'
        steps[x-1][y] = 'N'
        if traverse([(x-1, y)], steps, x, y):
            return steps, 'N'

    # south valid start?
    if valid_coordinates(len(lines), x+1, y) and (lines[x+1][y] == "J" or lines[x+1][y] == "L" or lines[x+1][y] == '|'):
        steps[x][y] = 'S'
        steps[x+1][y] = 'S'
        if traverse([(x+1, y)], steps, x, y):
            return steps, 'S'

    # east valid start?
    if valid_coordinates(len(lines), x, y+1) and (lines[x][y+1] == "7" or lines[x][y+1] == "J" or lines[x][y+1] == '-'):
        steps[x][y] = 'E'
        steps[x][y+1] = 'E'
        if traverse([(x, y+1)], steps, x, y):
            return steps, 'E'

    # west valid start?
    if valid_coordinates(len(lines), x, y-1) and (lines[x][y-1] == "L" or lines[x][y-1] == "F" or lines[x][y-1] == '-'):
        steps[x][y] = 'W'
        steps[x][y-1] = 'W'
        if traverse([(x, y-1)], steps, x, y):
            return steps, 'W'

def flood_fill(steps: List[List[int]], explore_queue: List[Tuple[int, int]], symbol: str) -> None:
    for (x, y) in explore_queue:
        # TODO this can be cleaner
        for dx, dy in DIRECTIONS["S"]:
            if (valid_coordinates(len(lines), x + dx, y + dy) and steps[x + dx][y + dy] != symbol):
                steps[x + dx][y + dy] = symbol
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
            
            steps, symbol = bfs(lines, *start_coordinates)
            for i in range(len(lines)):
                if lines[i][0] != symbol:
                    flood_fill(steps, [(i, 0)], symbol)
                if lines[0][i] != symbol:
                    flood_fill(steps, [(0, i)], symbol)
                if lines[i][len(lines) - 1] != symbol:
                    flood_fill(steps, [(i, len(lines) - 1)], symbol)
                if lines[len(lines) - 1][i] != symbol:
                    flood_fill(steps, [(len(lines) - 1, i)], symbol)
            sol = sum(step.count(float("inf")) for step in steps)
                

        print(f"------> {sol}")