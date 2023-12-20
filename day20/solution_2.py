import operator
from contextlib import redirect_stdout
from copy import deepcopy
from itertools import combinations
from math import prod
from pathlib import Path
from typing import Callable, Dict, Iterator, List, Optional

INPUT_NAME = "input_sample.txt"
CATEGORIES = ("x", "m", "a", "s")


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


class Condition:
    def __init__(self, category, lower_bound, upper_bound) -> None:
        self.category = category
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

    def update_lower_bound(self, new_value: int) -> None:
        self.lower_bound = max(self.lower_bound, new_value)

    def update_upper_bound(self, new_value: int) -> None:
        self.upper_bound = min(self.upper_bound, new_value)

    def is_valid(self) -> bool:
        return self.lower_bound <= self.upper_bound

    def __str__(self):
        return f"{str(self.lower_bound).rjust(4)} < {self.category} < {str(self.upper_bound).rjust(4)}"


class ConditionSet:
    mapping: Dict[str, Condition]

    def __init__(self):
        self.mapping = {cat: Condition(cat, 1, 4000) for cat in CATEGORIES}

    def all_valid(self) -> bool:
        return all(cat.is_valid() for _, cat in self.mapping.items())

    def __str__(self):
        inner_list = ",".join(str(s) for _, s in self.mapping.items())
        return f"{{ {inner_list} }}"

    def update_lower_bound(self, category: str, new_value: int) -> None:
        self.mapping[category].update_lower_bound(new_value)

    def update_upper_bound(self, category: str, new_value: int) -> None:
        self.mapping[category].update_upper_bound(new_value)

    def result(self) -> int:
        return prod(
            self.mapping[cat].upper_bound - self.mapping[cat].lower_bound - 1
            for cat in CATEGORIES
        )


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


def determine_accepted_part_formula(
    conditions: ConditionSet, rule_name: str, rules: Dict[str, List[RuleItem]]
) -> Iterator[ConditionSet]:
    if conditions.all_valid():
        for current_rule in rules[rule_name]:
            # End state?
            if hasattr(current_rule, "is_accepted"):
                if current_rule.is_accepted:
                    yield conditions

            # Just redirection to another rule?
            elif not hasattr(current_rule, "operation"):
                yield from determine_accepted_part_formula(
                    conditions, current_rule.next_rule, rules
                )

            # Branching statement?
            elif current_rule.operation == operator.gt:
                new_conds = deepcopy(conditions)
                new_conds.update_lower_bound(
                    current_rule.category, current_rule.threshold + 1
                )
                yield from determine_accepted_part_formula(
                    new_conds, current_rule.next_rule, rules
                )

                conditions.update_upper_bound(
                    current_rule.category, current_rule.threshold
                )
            elif current_rule.operation == operator.lt:
                new_conds = deepcopy(conditions)
                new_conds.update_upper_bound(
                    current_rule.category, current_rule.threshold - 1
                )
                yield from determine_accepted_part_formula(
                    new_conds, current_rule.next_rule, rules
                )

                conditions.update_lower_bound(
                    current_rule.category, current_rule.threshold
                )


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

                sol, conditions = 0, ConditionSet()
                accepted_conditions = [
                    cond
                    for cond in determine_accepted_part_formula(conditions, "in", rules)
                ]
                for ac in accepted_conditions:
                    print(str(ac))

                # TODO now actually compute the answer
                pass

            print("-" * 45)
            print(f"------> {sol}")
