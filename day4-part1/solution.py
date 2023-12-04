from collections import Counter
from contextlib import redirect_stdout
from pathlib import Path
import re

INPUT_NAME = "input_sample.txt"


if __name__ == "__main__":
    script_dir = Path(__file__).resolve().parent
    file_path = script_dir / INPUT_NAME

    sol = 0

    with open(script_dir / 'output.txt', 'w') as f:
      with redirect_stdout(f):
        with open(file_path, 'r') as file:
            lines = [line.rstrip() for line in file]

            for line in lines:
                winners, numbers = line.split(":")[1].split("|")
                winners = set(w for w in winners.split(" ") if w)
                numbers = Counter(n for n in numbers.split(" ") if n)
                count = 0
                for w in winners:
                   if w in numbers:
                      count += numbers[w]
                if count > 0:
                    sol += 2 ** (count - 1)

            print(sol)