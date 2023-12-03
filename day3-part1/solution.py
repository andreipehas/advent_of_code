from contextlib import redirect_stdout
from pathlib import Path
import re
from typing import List

INPUT_NAME = "input.txt"

def valid_above_below(lines: List[List[str]], line_len: int, idx: int, m_start: int, m_end: int) -> bool:
    if idx < 0 or idx >= line_len:
        return False

    return any(
        lines[idx][x] != '.' 
        for x in range(
            max(m_start-1, 0), 
            min(m_end+1, line_len)
        )
    )

def is_valid(lines: List[List[str]], line_len: int, idx: int, m_start: int, m_end: int) -> bool:
    return valid_above_below(lines, line_len, idx-1, m_start, m_end) \
        or valid_above_below(lines, line_len, idx+1, m_start, m_end) \
        or (m_start > 0 and lines[idx][m_start-1] != '.') \
        or (m_end < line_len-1 and lines[idx][m_end] != '.')

if __name__ == "__main__":
    script_dir = Path(__file__).resolve().parent
    file_path = script_dir / INPUT_NAME

    sol = 0

    with open(script_dir / 'output.txt', 'w') as f:
      with redirect_stdout(f):
        with open(file_path, 'r') as file:
            lines = [line.rstrip() for line in file]
            for i in range(len(lines)):
                matches = [(m.span()) for m in re.finditer("[0-9]*", lines[i]) if m.start(0) != m.end(0)]
                for m_start, m_end in matches:
                    parsed_number = int(lines[i][m_start:m_end])
                    if is_valid(lines, len(lines[0]), i, m_start, m_end):
                        print(f"{parsed_number} is valid")
                        sol += parsed_number
                    else:
                        print(f"{parsed_number} is invalid")

            print(sol)