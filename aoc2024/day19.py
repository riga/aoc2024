# coding: utf-8

"""
https://adventofcode.com/2024/day/19
"""

from __future__ import annotations

import functools

from aoc2024 import Solver, Part


def solution(data: list[str], part: Part) -> int | str | None:
    # parse data
    towels = set(data[0].replace(" ", "").split(","))
    max_towel_len = max(map(len, towels))
    designs = data[1:]

    # helper to count the number of possible towel designs
    @functools.cache
    def count_combinations(design: str) -> int:
        # check if the full design is already possible, plus all possible splits
        # up to the maximum towel length
        return int(design in towels) + sum(
            count_combinations(design[i:])
            for i in range(1, max_towel_len + 1)
            if design[:i] in towels
        )

    # part a: just count how many designs are possible
    if part == "a":
        return sum(count_combinations(design) > 0 for design in designs)

    # part b: return the sum of options
    return sum(map(count_combinations, designs))


if __name__ == "__main__":
    Solver(year=2024, day=19, truth_a=272, truth_b=1041529704688380).solve(solution, part="x", submit=False)
