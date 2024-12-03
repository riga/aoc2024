# coding: utf-8

"""
https://adventofcode.com/2024/day/2
"""

from __future__ import annotations

from aoc2024 import Solver, Part


def solution(data: list[str], part: Part) -> int | None:
    # parse levels
    levels: list[list[int]] = []
    for line in data:
        levels.append(list(map(int, line.split())))

    # helper to check if a sequence is safe
    def is_safe(seq: list[int], *, skip: int = -1) -> bool:
        # compute diffs, optionally skipping one element
        idxs = list(range(len(seq)))
        if skip >= 0:
            idxs.remove(skip)
        diffs = [seq[i] - seq[j] for i, j in zip(idxs[1:], idxs[:-1])]
        # test both directions
        return all(1 <= d <= 3 for d in diffs) or all(1 <= -d <= 3 for d in diffs)

    # count valid sequences, for part b optionally dropping levels and brute-force checking
    return sum(
        1 for seq in levels
        if (
            is_safe(seq) or
            (part == "b" and any(is_safe(seq, skip=i) for i in range(len(seq))))
        )
    )


if __name__ == "__main__":
    Solver(
        year=2024,
        day=2,
        truth_a=564,
        truth_b=604,
    ).solve(solution, part="x", submit=False)
