from pathlib import Path

INPUT_NAME = "input.txt"

if __name__ == "__main__":
    script_dir = Path(__file__).resolve().parent
    file_path = script_dir / INPUT_NAME
    sol = 0

    with open(file_path, 'r') as file:
      lines = [line.rstrip() for line in file]
      for line in lines:
        first_digit = None
        last_digit = None
        for c in line:
            if c.isdigit():
               first_digit = c if not first_digit else first_digit
               last_digit = c
        sol += 10 * int(first_digit) + int(last_digit)

    print(sol)