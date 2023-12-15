from contextlib import redirect_stdout
from pathlib import Path

INPUT_NAME = "input.txt"

def rolling_hash(text: str) -> int:
    value = 0
    for c in text:
        value = 17 * (value + ord(c)) % 256
    print(f"{value} <- {text}")
    return value

if __name__ == "__main__":
    script_dir = Path(__file__).resolve().parent
    file_path = script_dir / INPUT_NAME

    sol = 0

    with open(script_dir / 'output.txt', 'w') as f:
      with redirect_stdout(f):
        with open(file_path, 'r') as file:
            lines = [line.rstrip() for line in file]
            inputs = lines[0].split(",")
            sol = sum(rolling_hash(input) for input in inputs)
            
        print(f"------> {sol}")