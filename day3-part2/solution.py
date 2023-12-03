from contextlib import redirect_stdout
from math import prod
from pathlib import Path
import re
from typing import Dict, List, Optional

INPUT_NAME = "input.txt"

def find_above_below(lines: List[List[str]], line_len: int, idx: int, m_start: int, m_end: int) -> List[Optional[int]]:
    if idx < 0 or idx >= line_len:
        return []

    lo, hi = max(m_start-1, 0), min(m_end+1, line_len)
    return [lo + m.start() for m in re.finditer("\*", lines[idx][lo:hi])]

def add_matches(
        gear_candidates: Dict[int, List[int]],
        parsed_number: int,
        lines: List[List[str]], 
        line_len: int, 
        idx: int, 
        m_start: int, 
        m_end: int
    ) -> None:
    # TODO please defaultdict
    # and then you won't need to DRY those repeated lines in a separate method?

    # above
    line_idx = idx - 1
    for m in find_above_below(lines, line_len, line_idx, m_start, m_end):
        packed_coordinates = line_idx * line_len + m
        if packed_coordinates not in gear_candidates:
            gear_candidates[packed_coordinates] = [parsed_number]
        else:
            gear_candidates[packed_coordinates].append(parsed_number)

    #below
    line_idx = idx + 1
    for m in find_above_below(lines, line_len, line_idx, m_start, m_end):
        packed_coordinates = line_idx * line_len + m
        if packed_coordinates not in gear_candidates:
            gear_candidates[packed_coordinates] = [parsed_number]
        else:
            gear_candidates[packed_coordinates].append(parsed_number)

    # to the left
    if m_start > 0 and lines[idx][m_start-1] == '*':
        packed_coordinates = idx * line_len + (m_start - 1)
        if packed_coordinates not in gear_candidates:
            gear_candidates[packed_coordinates] = [parsed_number]
        else:
            gear_candidates[packed_coordinates].append(parsed_number)

    # to the right
    if m_end < line_len-1 and lines[idx][m_end] == '*':
        packed_coordinates = idx * line_len + m_end
        if packed_coordinates not in gear_candidates:
            gear_candidates[packed_coordinates] = [parsed_number]
        else:
            gear_candidates[packed_coordinates].append(parsed_number)


if __name__ == "__main__":
    script_dir = Path(__file__).resolve().parent
    file_path = script_dir / INPUT_NAME

    sol = 0

    with open(script_dir / 'output.txt', 'w') as f:
      with redirect_stdout(f):
        with open(file_path, 'r') as file:
            lines = [line.rstrip() for line in file]
            # TODO this would make more sense to be a defaultdict
            gear_candidates = {}

            for i in range(len(lines)):
                matches = [(m.span()) for m in re.finditer("[0-9]*", lines[i]) if m.start(0) != m.end(0)]
                for m_start, m_end in matches:
                    parsed_number = int(lines[i][m_start:m_end])
                    add_matches(
                        gear_candidates,
                        parsed_number,
                        lines, 
                        len(lines[0]), 
                        i,
                        m_start, 
                        m_end
                    )

            for gear in gear_candidates:
                if len(gear_candidates[gear]) == 2:
                    print(f"Gear at ({gear//len(lines[0])},{gear%len(lines[0])}) is valid")
                    sol += gear_candidates[gear][0] * gear_candidates[gear][1]
                else:
                    print(f"Gear at ({gear//len(lines[0])},{gear%len(lines[0])}) is invalid")

            print(sol)