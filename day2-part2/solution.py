from contextlib import redirect_stdout
from pathlib import Path

INPUT_NAME = "input.txt"

def solve(game_list: str) -> int:
    current = {}
    
    for game in game_list:
        for entry in game.split(","):
            count, colour = entry.strip().split(" ")
            current[colour] = max(current.get(colour, 0), int(count))
    
    print(current)
    return current.get("red", 1) * current.get("green", 1) * current.get("blue", 1)

if __name__ == "__main__":
    script_dir = Path(__file__).resolve().parent
    file_path = script_dir / INPUT_NAME

    sol = 0

    with open(script_dir / 'output.txt', 'w') as f:
      with redirect_stdout(f):
        with open(file_path, 'r') as file:
            lines = [line.rstrip() for line in file]

            for idx, line in enumerate(lines):
                game_list = line.split(":")[1].split(";")
                sol += solve(game_list)

            print(sol)