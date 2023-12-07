from contextlib import redirect_stdout
from math import ceil, prod, sqrt
from pathlib import Path

INPUT_NAME = "input.txt"

def solve(time: int, threshold: int) -> int:
  delta = time * time - 4 * threshold
  if delta < 0:
    return 0
  sol_1 = (time - sqrt(delta)) / 2
  sol_2 = (time + sqrt(delta)) / 2


  current_sol = int(sol_2) - ceil(sol_1) + 1
  if sol_1 % 1 == 0:
     current_sol -= 1
  if sol_2 % 1 == 0:
     current_sol -= 1

  return max(current_sol, 0)

if __name__ == "__main__":
    script_dir = Path(__file__).resolve().parent
    file_path = script_dir / INPUT_NAME

    sol = 0

    with open(script_dir / 'output.txt', 'w') as f:
      with redirect_stdout(f):
        with open(file_path, 'r') as file:
            times, distances = (line.split()[1:] for line in file)
            sol = prod(
              solve(int(times[i]), int(distances[i]))
              for i in range(len(times))
            )
            
        print(sol)