from contextlib import redirect_stdout
from pathlib import Path
from typing import List

INPUT_NAME = "input.txt"

NORTH = (-1, 0)
SOUTH = (1, 0)
EAST  = (0, 1)
WEST  = (0, -1)
DIRECTIONS = {
    None: [NORTH, SOUTH, EAST, WEST],
    "ALL": [NORTH, SOUTH, EAST, WEST],
    "S": [NORTH, SOUTH, EAST, WEST],
    "F": [SOUTH, EAST],
    "7": [SOUTH, WEST],
    "J": [NORTH, WEST],
    "L": [NORTH, EAST],
    "|": [NORTH, SOUTH],
    "-": [EAST, WEST],
    ".": [],
}
STAY = (0, 0)
NORTH_WEST = (-1, -1)
DIRECTIONS_GRID = [STAY, NORTH, WEST, NORTH_WEST]

def is_cell_valid(size_x: int, size_y: int, x: int, y: int) -> bool:
   return 0 <= x and x <  size_x and 0 <= y and y <  size_y

def are_coordinates_valid_grid(size_x: int, size_y: int, x: int, y: int) -> bool:
   return 0 <= x and x <= size_x and 0 <= y and y <= size_y 

def is_valid_transition_cells(target_symbol, reverse_direction) -> bool:
    return reverse_direction in DIRECTIONS[target_symbol]

def is_valid_transition_grid(lines, x, y, dx, dy, size_x, size_y) -> bool:
    # East
    if dx == 0 and dy == 1:
        return (NORTH not in DIRECTIONS[lines[x]  [y]] if is_cell_valid(size_x, size_y,   x, y) else True) \
           or  (SOUTH not in DIRECTIONS[lines[x-1][y]] if is_cell_valid(size_x, size_y, x-1, y) else True)
    
    # West
    if dx == 0 and dy == -1:
        return (NORTH not in DIRECTIONS[lines[x]  [y-1]] if is_cell_valid(size_x, size_y, x,   y-1) else True) \
           or  (SOUTH not in DIRECTIONS[lines[x-1][y-1]] if is_cell_valid(size_x, size_y, x-1, y-1) else True)
    
    # North
    if dx == -1 and dy == 0:
        return (EAST not in DIRECTIONS[lines[x-1][y-1]] if is_cell_valid(size_x, size_y, x-1, y-1) else True) \
           or  (WEST not in DIRECTIONS[lines[x-1]  [y]] if is_cell_valid(size_x, size_y, x-1,   y) else True)

    # South
    if dx == 1 and dy == 0:
        return (EAST not in DIRECTIONS[lines[x][y-1]] if is_cell_valid(size_x, size_y, x, y-1) else True) \
           or  (WEST not in DIRECTIONS[lines[x]  [y]] if is_cell_valid(size_x, size_y, x,   y) else True)
    
    raise ValueError(f"What do you mean ({dx},{dy})?!?")

def is_loop(lines, x, y, start_x, start_y):
    explore_queue = [(x,y)]
    steps = [[float("inf")] * len(lines[0]) for _ in range(len(lines))]
    steps[x][y] = 0

    # traverse the array
    while explore_queue:
        x, y = explore_queue.pop(0)
        for dx, dy in DIRECTIONS[lines[x][y]]:
            if (
                is_cell_valid(len(lines), len(lines[0]), x + dx, y + dy) and
                is_valid_transition_cells(lines[x+dx][y+dy], (-dx, -dy))
            ):
                if x + dx == start_x and y + dy == start_y:
                    return True
                if steps[x+dx][y+dy] == float("inf"):
                    explore_queue.append((x+dx, y+dy))
    return False

def mark_loop(lines, x, y):
    explore_queue = [(x,y)]
    reachable = [[0] * len(lines[0]) for _ in range(len(lines))]
    reachable[x][y] = 0

    # traverse the array
    while explore_queue:
        x, y = explore_queue.pop(0)
        for dx, dy in DIRECTIONS[lines[x][y]]:
            if (
                is_cell_valid(len(lines), len(lines[0]), x + dx, y + dy) and
                is_valid_transition_cells(lines[x+dx][y+dy], (-dx, -dy))
            ):
                if reachable[x+dx][y+dy] == 0:
                    explore_queue.append((x+dx, y+dy))
                    reachable[x+dx][y+dy] = 1
    return reachable

def mark_loop_as_visited(lines, x, y) -> int:
    # Does the loop go:
    for dx, dy in (NORTH, WEST, SOUTH, EAST):
        if is_valid_transition_cells(lines[x+dx][y+dy], (-dx, -dy)) and is_loop(lines, x + dx, y + dy, x, y):
            return mark_loop(lines, x + dx, y + dy)


def flood_fill(
        lines: List[List[int]], reachable
    ) -> None:
    # Here coordinates are no longer cells - but on the grid between them
    # in order to squeeze between pipes
    explore_queue = [(0, 0)]
    visited = [[False] * (len(lines[0]) + 1) for _ in range((len(lines) + 1))]
    visited[0][0] = True

    while explore_queue:
        x, y = explore_queue.pop(0)

        # What grid cells are accesible from the current coordinates?
        for dx, dy in DIRECTIONS_GRID:
            if is_cell_valid(len(lines), len(lines[0]), x + dx, y + dy):
                reachable[x + dx][y + dy] = 1            

        # What coordinates to explore next?
        for dx, dy in DIRECTIONS["ALL"]:
            if (
                are_coordinates_valid_grid(len(lines), len(lines[0]), x + dx, y + dy)
                and is_valid_transition_grid(lines, x, y, dx, dy, len(lines), len(lines[0])) 
                and not visited[x + dx][y + dy]
            ):
                explore_queue.append((x + dx, y + dy))
                visited[x + dx][y + dy] = True

    print("\n".join("".join(str(el) for el in row) for row in reachable))
    return sum(r.count(0) for r in reachable)

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
            
            reachable = mark_loop_as_visited(lines, *start_coordinates)
            lines = [list(line) for line in lines]
            pass
            for i in range(len(lines)):
                for j in range(len(lines[0])):
                    if reachable[i][j] == 0:
                        lines[i][j] = '.'
            lines = [''.join(line) for line in lines]
            
            sol = flood_fill(lines, reachable)
                
        print(f"------> {sol}")