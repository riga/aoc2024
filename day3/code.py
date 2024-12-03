# coding: utf-8

"""
https://adventofcode.com/2024/day/3
"""

from __future__ import annotations

import re

from aoc2024 import Solver, Part


def solution(data: list[str], part: Part) -> int | None:
    # treat data as a single string
    data = "".join(data)

    # precompile the regex looking for mul() calls
    cre = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")

    # part a: just sum products of all matches
    if part == "a":
        sum_a = sum(
            int(a) * int(b)
            for a, b in (
                tuple(map(int, m.groups()))
                for m in cre.finditer(data)
            )
        )
        return sum_a

    # part b: split by stop instruction "don't()" and in each chunk,
    # search for mul() calls after the first "do()"
    data = f"do(){data}"
    sum_b = 0
    for chunk in data.split("don't()"):
        offset = chunk.find("do()")
        if offset == -1:
            continue
        sum_b += sum(
            int(a) * int(b)
            for a, b in (
                tuple(map(int, m.groups()))
                for m in cre.finditer(chunk[offset + 4:])
            )
        )
    return sum_b


if __name__ == "__main__":
    Solver(
        year=2024,
        day=3,
        truth_a=179834255,
        truth_b=80570939,
    ).solve(solution, part="x", submit=False)
