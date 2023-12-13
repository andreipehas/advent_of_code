from contextlib import redirect_stdout
from pathlib import Path
from typing import List, Tuple

INPUT_NAME = "input.txt"

def valid_palindrome_with_smudge_after_line_idx(input: List[str], idx: int) -> bool:
   stop = min(idx + 1, len(input) - idx - 1)

   return [
      input[idx-offset][j]==input[idx+offset+1][j] 
      for offset in range(stop) 
      for j in range(len(input[0]))
   ].count(False) == 1

def valid_palindrome_with_smudge_after_column_idx(input: List[str], idx: int) -> bool:
   stop = min(idx + 1, len(input[0]) - idx - 1)

   return [
      input[j][idx-offset]==input[j][idx+offset+1] 
      for offset in range(stop) 
      for j in range(len(input))
   ].count(False) == 1

def solve(input: List[str]) -> Tuple[int, int]:
   lpal, cpal = 0, 0
   
   # find palindromes on lines
   for i in range(len(input) - 1):
      if valid_palindrome_with_smudge_after_line_idx(input, i):
         lpal += i + 1
   
   # find palindromes on columns
   for i in range(len(input[0]) - 1):
      if valid_palindrome_with_smudge_after_column_idx(input, i):
         cpal += i + 1

   return (lpal, cpal)

if __name__ == "__main__":
    script_dir = Path(__file__).resolve().parent
    file_path = script_dir / INPUT_NAME

    sol = 0

    with open(script_dir / 'output.txt', 'w') as f:
      with redirect_stdout(f):
        with open(file_path, 'r') as file:
            lines = [list(line.rstrip()) for line in file]
            input_boundaries = [-1] + [idx for idx, line in enumerate(lines) if line == []] + [len(lines)]
            for i in range(len(input_boundaries) - 1):
                lpal, cpal = solve(lines[input_boundaries[i] + 1 : input_boundaries[i+1]])
                sol += 100 * lpal + cpal

        print(sol)