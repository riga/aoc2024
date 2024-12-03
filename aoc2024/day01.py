# coding: utf-8

"""
https://adventofcode.com/2024/day/1
"""

from __future__ import annotations

import heapq
from collections import defaultdict

from aoc2024 import Solver, Part


def solution(data: list[str], part: Part) -> int | None:
    heapl: list[int] = []
    heapr: list[int] = []
    counts: dict[int, int] = defaultdict(int)

    # parse pairs into lists
    for line in data:
        l, r = map(int, line.split())
        heapq.heappush(heapl, l)
        heapq.heappush(heapr, r)
        counts[r] += 1

    # part one: sum up differences between min pairs
    if part == "a":
        sum_diff = 0
        while heapl:
            l, r = heapq.heappop(heapl), heapq.heappop(heapr)
            sum_diff += abs(r - l)
        return sum_diff

    # part two: compute score
    else:
        return sum(
            l * counts.get(l, 0)
            for l in heapl
        )


if __name__ == "__main__":
    Solver(
        year=2024,
        day=1,
        truth_a=1319616,
        truth_b=27267728,
    ).solve(solution, part="x", submit=False)
