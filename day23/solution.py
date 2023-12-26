from contextlib import redirect_stdout
from pathlib import Path
import sys
from typing import List, NamedTuple, Set

INPUT_NAME = "input.txt"


class Coordinates(NamedTuple):
    x: int
    y: int


NORTH = Coordinates(-1, 0)
SOUTH = Coordinates(1, 0)
EAST = Coordinates(0, 1)
WEST = Coordinates(0, -1)
DIRECTIONS = {
    ".": [NORTH, SOUTH, EAST, WEST],
    "^": [NORTH],
    ">": [EAST],
    "v": [SOUTH],
    "<": [WEST],
}


def valid_coordinates(
    size_x: int,
    size_y: int,
    coords: Coordinates,
    lines: List[str],
    visited: Set[Coordinates],
) -> bool:
    return (
        0 <= coords.x
        and coords.x < size_x
        and 0 <= coords.y
        and coords.y < size_y
        and lines[coords.x][coords.y] != "#"
        and coords not in visited
    )


def dfs(lines: List[str], visited: Set[Coordinates], current: Coordinates) -> int:
    current_sol = -1

    for d in DIRECTIONS[lines[current.x][current.y]]:
        next_coords = Coordinates(current.x + d.x, current.y + d.y)
        if valid_coordinates(len(lines), len(lines[0]), next_coords, lines, visited):
            if next_coords.x == len(lines) - 1:
                return len(visited)
            visited.add(next_coords)
            current_sol = max(current_sol, dfs(lines, visited, next_coords))
            visited.remove(next_coords)

    return current_sol


if __name__ == "__main__":
    script_dir = Path(__file__).resolve().parent
    file_path = script_dir / INPUT_NAME
    sol = 0

    #print(sys.getrecursionlimit())
    sys.setrecursionlimit(10000)
    #print(sys.getrecursionlimit())

    with open(script_dir / "output.txt", "w") as f:
        with redirect_stdout(f):
            with open(file_path, "r") as file:
                lines = [line.rstrip() for line in file]
                start_y = lines[0].find(".")
                start_coords = Coordinates(0, start_y)
                visited = set(start_coords)
                sol = dfs(lines, visited, start_coords)

            print(f"------> {sol - 1}")
