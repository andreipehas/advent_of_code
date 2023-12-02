from contextlib import redirect_stdout
from pathlib import Path

INPUT_NAME = "input.txt"

def solve(game_list: str) -> bool:
    for game in game_list:
        current = {}
        for entry in game.split(","):
            count, colour = entry.strip().split(" ")
            current[colour] = current.get(colour, 0) + int(count)
            if current[colour] > threshold.get(colour, 0):
                print(f"Game {idx+1} is incorrect: it has {count} of {colour}")
                return False
    
    return True

if __name__ == "__main__":
    script_dir = Path(__file__).resolve().parent
    file_path = script_dir / INPUT_NAME

    threshold = {"red": 12, "green": 13, "blue": 14}
    sol = 0

    with open(script_dir / 'output.txt', 'w') as f:
      with redirect_stdout(f):
        with open(file_path, 'r') as file:
            lines = [line.rstrip() for line in file]

            for idx, line in enumerate(lines):
                game_list = line.split(":")[1].split(";")
                if solve(game_list):
                    print(f"Game {idx+1} is correct")
                    sol += idx + 1

            print(sol)