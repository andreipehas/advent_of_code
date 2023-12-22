from contextlib import redirect_stdout
from pathlib import Path
from typing import List, NamedTuple

INPUT_NAME = "input.txt"


class Rule(NamedTuple):
    start: int
    end: int
    offset: int


def parse_seeds(line: str) -> List[int]:
    colon_idx = line.find(":")
    return [int(seed) for seed in line[colon_idx + 1 :].split()]


def parse_ruleset(lines: List[str]) -> List[Rule]:
    parsed_ints = [[int(x) for x in line.split()] for line in lines]
    return [
        Rule(source, source + length - 1, destination - source)
        for destination, source, length in parsed_ints
    ]


def transform(seed: int, ruleset: List[Rule]) -> None:
    for rule in ruleset:
        if rule.start <= seed and seed <= rule.end:
            return seed + rule.offset
    return seed


if __name__ == "__main__":
    script_dir = Path(__file__).resolve().parent
    file_path = script_dir / INPUT_NAME

    with open(script_dir / "output.txt", "w") as f:
        with redirect_stdout(f):
            with open(file_path, "r") as file:
                lines = [line.rstrip() for line in file]
                seeds = parse_seeds(lines[0])
                print(seeds)

            map_separator_idxs = [
                i for i, line in enumerate(lines) if "map" in line
            ] + [len(lines) + 1]

            for i in range(1, len(map_separator_idxs)):
                ruleset = parse_ruleset(
                    lines[map_separator_idxs[i - 1] + 1 : map_separator_idxs[i] - 1]
                )
                seeds = [transform(seed, ruleset) for seed in seeds]
                print(seeds)

            print(f"------> {min(seeds)}")
