# coding: utf-8

"""
https://adventofcode.com/2024/day/8
"""

from __future__ import annotations

import itertools
from collections import defaultdict

from aoc2024 import Solver, Part


def solution(data: list[str], part: Part) -> int | None:
    # parse into per-type antenna locations, stored as complex numbers (real -> i, imag -> j)
    imax, jmax = len(data), len(data[0])
    antennas: defaultdict[str, set[complex]] = defaultdict(set)
    for i in range(imax):
        for j in range(jmax):
            if data[i][j] != ".":
                antennas[data[i][j]].add(complex(i, j))

    # helper to check if a point is within the map bounds
    def within_bounds(p: complex, imax: int, jmax: int) -> bool:
        return 0 <= p.real < imax and 0 <= p.imag < jmax

    # find unique antinode locations evaluating all pairs of same antennas
    antinodes: set[complex] = set()
    for points in antennas.values():
        for p1, p2 in itertools.combinations(points, 2):
            # difference vector
            diff = p2 - p1

            if part == "a":
                # check single locations on either side
                if within_bounds((p := p2 + diff), imax, jmax):
                    antinodes.add(p)
                if within_bounds((p := p1 - diff), imax, jmax):
                    antinodes.add(p)

            else:  # "b"
                # check all locations on either side
                p = p2
                while within_bounds(p, imax, jmax):
                    antinodes.add(p)
                    p += diff
                p = p1
                while within_bounds(p, imax, jmax):
                    antinodes.add(p)
                    p -= diff

    return len(antinodes)


if __name__ == "__main__":
    Solver(year=2024, day=8, truth_a=280, truth_b=958).solve(solution, part="x", submit=False)
