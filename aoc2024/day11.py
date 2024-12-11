# coding: utf-8

"""
https://adventofcode.com/2024/day/11
"""

from __future__ import annotations

import functools

from aoc2024 import Solver, Part


def solution(data: list[str], part: Part) -> int | None:
    # parse stones
    stones = list(map(int, data[0].split()))

    # helper to count stones given a starting stone and the number of blinks
    @functools.cache
    def count(stone: int, n: int) -> int:
        # no blink left
        if n == 0:
            return 1
        # 0 -> single stone, move to one
        if stone == 0:
            return count(1, n - 1)
        # even nums -> split in half
        if (l := len(s := str(stone))) % 2 == 0:
            return count(int(s[:l // 2]), n - 1) + count(int(s[l // 2:]), n - 1)
        # otherwise -> single stone, times 2024
        return count(stone * 2024, n - 1)

    # sum over all stones
    return sum(count(stone, 25 if part == "a" else 75) for stone in stones)


if __name__ == "__main__":
    Solver(year=2024, day=11, truth_a=204022, truth_b=241651071960597).solve(solution, part="x", submit=False)
