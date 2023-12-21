from contextlib import redirect_stdout
from pathlib import Path
from typing import List

INPUT_NAME = "input.txt"
STEP_COUNT = 64

NORTH = (-1, 0)
SOUTH = (1, 0)
EAST = (0, 1)
WEST = (0, -1)
DIRECTIONS = (NORTH, SOUTH, EAST, WEST)


def valid_coordinates(x: int, y: int, size_x: int, size_y: int):
    return 0 <= x and x < size_x and 0 <= y and y < size_y


def steppy_steps(lines: List[str], start_x: int, start_y: int) -> int:
    possible_locations = set()
    possible_locations.add((start_x, start_y))
    for _ in range(STEP_COUNT):
        next_locations = set()
        for x, y in possible_locations:
            for dx, dy in DIRECTIONS:
                if valid_coordinates(
                    x + dy, y + dy, len(lines), len(lines[0])
                ) and lines[x + dx][y + dy] in (".", "S"):
                    next_locations.add((x + dx, y + dy))

        possible_locations = next_locations

    return len(possible_locations)


if __name__ == "__main__":
    script_dir = Path(__file__).resolve().parent
    file_path = script_dir / INPUT_NAME

    sol = 0

    with open(script_dir / "output.txt", "w") as f:
        with redirect_stdout(f):
            with open(file_path, "r") as file:
                lines = [line.rstrip() for line in file]
                for i in range(len(lines)):
                    j = lines[i].find("S")
                    if j >= 0:
                        start_coordinates = (i, j)
                        break

                sol = steppy_steps(lines, i, j)

            print(f"------> {sol}")
