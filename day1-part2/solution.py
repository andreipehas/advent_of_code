from contextlib import redirect_stdout
from pathlib import Path
import regex as re
from typing import Dict, List, Union
from word2number import w2n


INPUT_NAME = "input.txt"

if __name__ == "__main__":
    script_dir = Path(__file__).resolve().parent
    file_path = script_dir / INPUT_NAME
    
    sol = 0
    digits = list("1234567890")
    words = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    pattern = "|".join(digits + words)

    with open(script_dir / 'output.txt', 'w') as f:
      with redirect_stdout(f):

        with open(file_path, 'r') as file:
          lines = [line.rstrip() for line in file]
          for line in lines:
            matches = re.findall(pattern, line, overlapped=True) 
            first_digit = w2n.word_to_num(matches[0])
            last_digit = w2n.word_to_num(matches[-1])
            
            print(line)
            print(first_digit, " ", last_digit)
            
            sol += 10 * int(first_digit) + int(last_digit)

        
        print(sol)