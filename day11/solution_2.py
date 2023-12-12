from contextlib import redirect_stdout
from itertools import accumulate, combinations
from pathlib import Path
from typing import List, Tuple

INPUT_NAME = "input.txt"

def detect_galaxies(lines: List[List[int]]) -> List[int]:
  galaxy_on_line, galaxy_on_column = [999999] * len(lines[0]), [999999] * len(lines)
  for i in range(len(lines)):
    for j in range(len(lines[0])):
      if lines[i][j] == '#':
        galaxy_on_line[i] = 0
        galaxy_on_column[j] = 0

  offset_lines = list(accumulate(galaxy_on_line))
  offset_columns = list(accumulate(galaxy_on_column))
  galaxies = []

  for i in range(len(lines)):
    for j in range(len(lines[0])):
      if lines[i][j] == '#':
        galaxies.append((i + offset_lines[i], j + offset_columns[j]))

  return galaxies

def manhattan_distance(t1: Tuple[int, int], t2: Tuple[int, int]) -> int:
  return abs(t1[0] - t2[0]) + abs(t1[1] - t2[1])

def compute_min_distances(galaxies: List[Tuple[int, int]]) -> int:
  return sum(manhattan_distance(t1, t2) for (t1, t2) in combinations(galaxies, 2))

if __name__ == "__main__":
    script_dir = Path(__file__).resolve().parent
    file_path = script_dir / INPUT_NAME
    sol = 0

    with open(script_dir / 'output.txt', 'w') as f:
      with redirect_stdout(f):
        with open(file_path, 'r') as file:
          lines = [line.rstrip() for line in file]
          galaxies = detect_galaxies(lines)
          sol = compute_min_distances(galaxies)

        print(f"------> {sol}")