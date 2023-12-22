from contextlib import redirect_stdout
from pathlib import Path
from typing import List, NamedTuple

INPUT_NAME = "input.txt"


class Interval(NamedTuple):
    start: int
    end: int

    def is_valid(self) -> bool:
        return self.start <= self.end

    def __repr__(self) -> str:
        return f"[{self.start},{self.end}]"


class Rule(NamedTuple):
    start: int
    end: int
    offset: int

    def __repr__(self) -> str:
        return f"[{self.start},{self.end}] -> {'+' if self.offset > 0 else ''}{self.offset}"


def parse_seeds(line: str) -> List[Interval]:
    colon_idx = line.find(":")
    parsed_ints = [int(seed) for seed in line[colon_idx + 1 :].split()]
    return [Interval(x, x + y) for x, y in zip(parsed_ints[::2], parsed_ints[1::2])]


def parse_ruleset(lines: List[str]) -> List[Rule]:
    parsed_ints = [[int(x) for x in line.split()] for line in lines]
    return [
        Rule(source, source + length - 1, destination - source)
        for destination, source, length in parsed_ints
    ]


def transform(still_to_check: List[Interval], ruleset: List[Rule]) -> None:
    final_intervals = []
    for rule in ruleset:
        new_intervals = []
        for interval in still_to_check:
            # Do they intesect?
            # [interval.start, interval.end] and [rule.start, rule.end]
            intersection = Interval(
                max(interval.start, rule.start), min(interval.end, rule.end)
            )
            if intersection.is_valid():
                # before intersection
                before = Interval(interval.start, intersection.start - 1)
                if before.is_valid():
                    new_intervals.append(before)
                # intersection
                final_intervals.append(
                    Interval(
                        intersection.start + rule.offset, intersection.end + rule.offset
                    )
                )
                # after intersection
                after = Interval(intersection.end + 1, interval.end)
                if after.is_valid():
                    new_intervals.append(after)
            else:
                new_intervals.append(interval)
        still_to_check = new_intervals

    return still_to_check + final_intervals


if __name__ == "__main__":
    script_dir = Path(__file__).resolve().parent
    file_path = script_dir / INPUT_NAME

    with open(script_dir / "output.txt", "w") as f:
        with redirect_stdout(f):
            with open(file_path, "r") as file:
                lines = [line.rstrip() for line in file]
                seed_groups = parse_seeds(lines[0])
                print(seed_groups)

            map_separator_idxs = [
                i for i, line in enumerate(lines) if "map" in line
            ] + [len(lines) + 1]

            for i in range(1, len(map_separator_idxs)):
                ruleset = parse_ruleset(
                    lines[map_separator_idxs[i - 1] + 1 : map_separator_idxs[i] - 1]
                )
                new_seed_groups = []
                for group in seed_groups:
                    new_seed_groups += transform([group], ruleset)
                seed_groups = new_seed_groups
                print(seed_groups)

            interval_starts = [x[0] for x in seed_groups]
            print(f"------> {min(interval_starts)}")
