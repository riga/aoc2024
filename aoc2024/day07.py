# coding: utf-8

"""
https://adventofcode.com/2024/day/7
"""

from __future__ import annotations

import math

from aoc2024 import Solver, Part


def solution(data: list[str], part: Part) -> int | None:
    # helper that checks if a target value can be reached by combining a current value
    # and a list of remaining numbers (dp style)
    def check(target: int, cur: int, nums: tuple[int, ...]) -> bool:
        # stop in case thr current value is already greater
        if cur > target:
            return False
        # at the end, check for equality
        if not nums:
            return cur == target
        # go through all branches, evaluating all operators
        return (
            check(target, cur + nums[0], nums[1:]) or
            check(target, cur * nums[0], nums[1:]) or
            (part == "b" and check(target, cur * 10**(num_digits(nums[0])) + nums[0], nums[1:]))
        )

    # helper to determine the number of digits in a number
    def num_digits(n: int) -> int:
        return int(math.floor(math.log10(n))) + 1

    # parse and check all
    res = 0
    for line in data:
        parts = line.split(":", 1)
        target = int(parts[0])
        nums = tuple(map(int, parts[1].strip().split()))
        if check(target, nums[0], nums[1:]):
            res += target

    return res


if __name__ == "__main__":
    Solver(year=2024, day=7, truth_a=7710205485870, truth_b=20928985450275).solve(solution, part="x", submit=False)
