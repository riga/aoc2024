# coding: utf-8

"""
https://adventofcode.com/2024/day/13
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from aoc2024 import Solver, Part


@dataclass
class Game:
    ax: int
    ay: int
    bx: int
    by: int
    px: int
    py: int

    @property
    def linear_dependent_buttons(self) -> bool:
        return self.ax * self.by == self.ay * self.bx


def solution(data: list[str], part: Part) -> int | None:
    # parse games
    games: list[Game] = []
    cre = re.compile(r".+\: X(\+|=)(?P<x>\d+), Y(\+|=)(?P<y>\d+)$")
    offset = 0 if part == "a" else 10000000000000
    while data:
        ma = cre.match(data.pop(0))
        mb = cre.match(data.pop(0))
        mp = cre.match(data.pop(0))
        assert ma and mb and mp
        games.append(Game(
            ax=int(ma.group("x")), ay=int(ma.group("y")),
            bx=int(mb.group("x")), by=int(mb.group("y")),
            px=int(mp.group("x")) + offset, py=int(mp.group("y")) + offset,
        ))

    # strategy: two unknowns and two equations, so we can just solve analytically (by hand or via matrix inversion);
    #           however, there is an edge case if the buttons result in linear independent moves (i.e., they construct a
    #           non-invertible matrix), in which case a more iterative approach is needed; knowing aoc, this is likely
    #           not realized in the puzzle input, but still check

    tokens = 0
    for g in games:
        assert not g.linear_dependent_buttons
        nb = (g.ax * g.py - g.px * g.ay) / (g.ax * g.by - g.ay * g.bx) * 1.0  # enforce float
        na = (g.px - nb * g.bx) / g.ax
        # require integer solutions
        if not na.is_integer() or not nb.is_integer():
            continue
        # cap for part a
        if part == "a" and (na > 100 or nb > 100):
            continue
        tokens += 3 * int(na) + int(nb)

    return tokens


if __name__ == "__main__":
    Solver(year=2024, day=13, truth_a=30413, truth_b=92827349540204).solve(solution, part="x", submit=False)
