import operator
from contextlib import redirect_stdout
from pathlib import Path
from typing import Callable, Dict, List, Optional

INPUT_NAME = "input.txt"


class RuleItem:
    category: Optional[str]
    operation: Optional[Callable]
    threshold: Optional[int]
    next_rule: str
    is_accepted: bool

    def __init__(self, s: str) -> "RuleItem":
        if s == "A":
            self.is_accepted = True
        elif s == "R":
            self.is_accepted = False
        else:
            colon_idx = next((i for i, c in enumerate(s) if c == ":"), -1)
            if colon_idx >= 0:
                # Rule that performs a check and defers to another
                self.category = s[0]
                if s[1] == "<":
                    self.operation = operator.lt
                elif s[1] == ">":
                    self.operation = operator.gt
                else:
                    raise NameError
                self.threshold = int(s[2:colon_idx])
                self.next_rule = s[colon_idx + 1 :]
            else:
                # Rule that references another rule (not A or R)
                self.next_rule = s


def parse_rules(lines: List[str]) -> Dict[str, List[RuleItem]]:
    rules = {}
    rules["A"] = [RuleItem("A")]
    rules["R"] = [RuleItem("R")]
    for line in lines:
        separator_idx = line.find("{")
        rule_name = line[:separator_idx]
        rule_items = line[separator_idx + 1 : -1].split(",")
        rules[rule_name] = [RuleItem(r) for r in rule_items]

    return rules


def is_part_accepted(
    part: Dict[str, int], rule_name: str, rules: Dict[str, List[RuleItem]]
) -> bool:
    for current_rule in rules[rule_name]:
        # End state?
        if hasattr(current_rule, "is_accepted"):
            return current_rule.is_accepted
        # Just redirection to another rule?
        if not hasattr(current_rule, "operation"):
            return is_part_accepted(part, current_rule.next_rule, rules)
        # Branching statement?
        if current_rule.operation(part[current_rule.category], current_rule.threshold):
            return is_part_accepted(part, current_rule.next_rule, rules)


if __name__ == "__main__":
    script_dir = Path(__file__).resolve().parent
    file_path = script_dir / INPUT_NAME

    sol = 0

    with open(script_dir / "output.txt", "w") as f:
        with redirect_stdout(f):
            with open(file_path, "r") as file:
                lines = [line.rstrip() for line in file]
                separator_idx = lines.index("")
                rules = parse_rules(lines[:separator_idx])

                for line in lines[separator_idx + 1 :]:
                    part = {}
                    part_attributes = line[1:-1].split(",")
                    for pattr in part_attributes:
                        part[pattr[0]] = int(pattr[2:])

                    if is_part_accepted(part, "in", rules):
                        sol += part["x"] + part["m"] + part["a"] + part["s"]

            print(f"------> {sol}")
