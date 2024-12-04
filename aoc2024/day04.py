# coding: utf-8

"""
https://adventofcode.com/2024/day/4
"""

from __future__ import annotations

from aoc2024 import Solver, Part


def solution(data: list[str], part: Part) -> int | None:
    # dimensions
    m, n = len(data), len(data[0])
    assert m == n

    if part == "a":
        # helper
        n_xmas = [0]
        def count(s: str) -> None:
            n_xmas[0] += s.count("XMAS") + s.count("SAMX")

        # horizontal
        for line in data:
            count(line)

        # vertical
        for j in range(n):
            row = "".join(data[i][j] for i in range(m))
            count(row)

        # diagonals
        # (making use of zip's truncation at the shortest iterable)
        # sweeping left-right and right-left
        for start in range(n):
            count("".join(data[i][j] for i, j in zip(range(0, m), range(start, n))))
            count("".join(data[i][j] for i, j in zip(range(m - 1, -1, -1), range(start, n))))
        # sweeping top-down and bottom-up, skipping the main diagonal
        for start in range(1, m):
            count("".join(data[i][j] for i, j in zip(range(start, m), range(0, n))))
            count("".join(data[i][j] for i, j in zip(range(m - 1 - start, -1, -1), range(0, n))))

        return n_xmas[0]

    # sliding 3x3 window, "convolve" important characters into string and compare against possible targets
    targets = {"MSAMS", "SSAMM", "MMASS", "SMASM"}
    n_x_mas = 0
    for i in range(m - 2):
        for j in range(n - 2):
            line = data[i][j] + data[i][j + 2]
            line += data[i + 1][j + 1]
            line += data[i + 2][j] + data[i + 2][j + 2]
            if line in targets:
                n_x_mas += 1

    return n_x_mas


if __name__ == "__main__":
    Solver(year=2024, day=4, truth_a=2483, truth_b=1925).solve(solution, part="x", submit=False)
