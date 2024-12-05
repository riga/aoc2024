# coding: utf-8

"""
https://adventofcode.com/2024/day/5
"""

from __future__ import annotations

from collections import defaultdict, deque

from aoc2024 import Solver, Part


def solution(data: list[str], part: Part) -> int | None:
    # split into dependencies and updates
    deps: dict[int, set[int]] = defaultdict(set)
    updates: list[deque[int]] = []
    for line in data:
        if "|" in line:
            a, b = map(int, line.split("|"))
            deps[b].add(a)
        elif "," in line:
            updates.append(deque(map(int, line.split(","))))

    # loop over updates in part a and store incorrect ones for part b
    incorrect_updates: list[deque[int]] = []
    sum_a = 0
    for nums in updates:
        nums_set = set(nums)  # for faster lookup
        printed = set()
        for n in nums:
            # check if n has dependencies that should but are not yet printed
            if n in deps and any(m in nums_set and m not in printed for m in deps[n]):
                # incorrect update found
                incorrect_updates.append(nums)
                break
            printed.add(n)
        else:
            sum_a += nums[len(nums) // 2]

    if part == "a":
        return sum_a

    # part b
    sum_b = 0
    for nums in incorrect_updates:
        # convert to a correct order
        corrected = []
        printed = set()
        nums_set = set(nums)  # for faster lookup
        while nums:
            n = nums.popleft()
            # same check as in part a
            if n in deps and any(m in nums_set and m not in printed for m in deps[n]):
                nums.append(n)
            else:
                corrected.append(n)
                printed.add(n)
        sum_b += corrected[len(corrected) // 2]

    return sum_b


if __name__ == "__main__":
    Solver(year=2024, day=5, truth_a=6267, truth_b=5184).solve(solution, part="x", submit=False)
