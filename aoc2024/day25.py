# coding: utf-8

"""
https://adventofcode.com/2024/day/25
"""

from __future__ import annotations

from aoc2024 import Solver, Part


def solution(data: list[str], part: Part) -> int | str | None:
    # parse into locks and keys
    locks: list[list[int]] = []
    keys: list[list[int]] = []
    i = 0
    while i < len(data):
        is_lock = "#" in data[i]
        lines = data[i + 1:i + 6]
        heights = [
            sum(1 for i, line in enumerate(lines) if line[j] == "#")
            for j in range(len(lines[0]))
        ]
        (locks if is_lock else keys).append(heights)
        i += 7

    def key_fits_lock(key: list[int], lock: list[int]) -> bool:
        return all(k <= 5 - l for k, l in zip(key, lock))

    # part a: try all combinations
    if part == "a":
        return sum(
            key_fits_lock(key, lock)
            for key in keys
            for lock in locks
        )

    # no part b this time
    return None


if __name__ == "__main__":
    Solver(year=2024, day=25, truth_a=3291, truth_b=None).solve(solution, part="a", submit=False)
