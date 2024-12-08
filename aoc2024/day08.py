# coding: utf-8

"""
https://adventofcode.com/2024/day/8
"""

from __future__ import annotations

import itertools
from collections import defaultdict
from dataclasses import dataclass

from aoc2024 import Solver, Part


@dataclass
class Point:
    i: int
    j: int

    def __hash__(self) -> int:
        return hash((self.i, self.j))

    def __add__(self, other: Point) -> Point:
        return Point(self.i + other.i, self.j + other.j)

    def __sub__(self, other: Point) -> Point:
        return Point(self.i - other.i, self.j - other.j)

    def in_bounds(self, imax: int, jmax: int) -> bool:
        return 0 <= self.i < imax and 0 <= self.j < jmax


def solution(data: list[str], part: Part) -> int | None:
    # parse into per-type antenna locations
    imax, jmax = len(data), len(data[0])
    antennas: defaultdict[str, set[Point]] = defaultdict(set)
    for i in range(imax):
        for j in range(jmax):
            if data[i][j] != ".":
                antennas[data[i][j]].add(Point(i, j))

    # find unique antinode locations evaluating all pairs of same antennas
    antinodes: set[Point] = set()
    for points in antennas.values():
        for p1, p2 in itertools.combinations(points, 2):
            # difference vector
            diff = p2 - p1

            if part == "a":
                # check single locations on either side
                if (p := p2 + diff).in_bounds(imax, jmax):
                    antinodes.add(p)
                if (p := p1 - diff).in_bounds(imax, jmax):
                    antinodes.add(p)

            else:  # "b"
                # check all locations on either side
                p = p2
                while p.in_bounds(imax, jmax):
                    antinodes.add(p)
                    p += diff
                p = p1
                while p.in_bounds(imax, jmax):
                    antinodes.add(p)
                    p -= diff

    return len(antinodes)


if __name__ == "__main__":
    Solver(year=2024, day=8, truth_a=280, truth_b=958).solve(solution, part="x", submit=False)
