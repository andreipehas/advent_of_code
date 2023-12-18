from enum import Enum
from contextlib import redirect_stdout
from pathlib import Path
from typing import List

INPUT_NAME = "input.txt"

class Direction(Enum):
	NORTH = (-1, 0)
	SOUTH = ( 1, 0)
	EAST  = ( 0, 1)
	WEST  = ( 0,-1)

NEXT_COORDINATES = {
	'.': {x: [x] for x in Direction},
	'\\': {
		Direction.NORTH: [Direction.WEST],
		Direction.SOUTH: [Direction.EAST],
		Direction.EAST: [Direction.SOUTH],
		Direction.WEST: [Direction.NORTH],
	},
	'/': {
		Direction.NORTH: [Direction.EAST],
		Direction.SOUTH: [Direction.WEST],
		Direction.WEST: [Direction.SOUTH],
		Direction.EAST: [Direction.NORTH],
	},
	'|': {
		Direction.NORTH: [Direction.NORTH],
		Direction.SOUTH: [Direction.SOUTH],
		Direction.EAST: [Direction.NORTH, Direction.SOUTH],
		Direction.WEST: [Direction.NORTH, Direction.SOUTH],
	},
	'-': {
		Direction.NORTH: [Direction.EAST, Direction.WEST],
		Direction.SOUTH: [Direction.EAST, Direction.WEST],
		Direction.EAST: [Direction.EAST],
		Direction.WEST: [Direction.WEST],
	},
}

def valid_coordinates(x: int, y: int, len_x: int, len_y: int) -> bool:
   return 0 <= x and x < len_x and 0 <= y and y < len_y

def traverse(lines: List[str]) -> int:
	explore_queue = [(0, 0, Direction.EAST)]
	visited = [[None] * len(lines[0]) for _ in range(len(lines))]
	sol = 0

	while explore_queue:
		x, y, current_dir = explore_queue.pop()
		if not visited[x][y]:
			sol += 1
			visited[x][y] = []
		if not current_dir in visited[x][y]:
			visited[x][y].append(current_dir)
			for next_dirs in NEXT_COORDINATES[lines[x][y]][current_dir]:
				if valid_coordinates(
					x + next_dirs.value[0],
					y + next_dirs.value[1], 
					len(lines[0]), len(lines)
				):
					explore_queue.append(
						(x + next_dirs.value[0], y + next_dirs.value[1], next_dirs)
					)

	return sol
				

if __name__ == "__main__":
	script_dir = Path(__file__).resolve().parent
	file_path = script_dir / INPUT_NAME

	sol = 0

	with open(script_dir / 'output.txt', 'w') as f:
		with redirect_stdout(f):
			with open(file_path, 'r') as file:
				lines = [list(line.rstrip()) for line in file]
				sol = traverse(lines)
					
			print(f"------> {sol}")