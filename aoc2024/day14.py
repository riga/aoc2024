# coding: utf-8

"""
https://adventofcode.com/2024/day/14
"""

from __future__ import annotations

import re
import heapq
import operator
import functools
from collections import defaultdict
from dataclasses import dataclass

from aoc2024 import Solver, Part


@dataclass
class Robot:
    p: complex
    v: complex

    @property
    def x(self) -> int:
        return int(self.p.real)

    @property
    def y(self) -> int:
        return int(self.p.imag)


def solution(data: list[str], part: Part) -> int | None:
    w, h = 101, 103
    robots: list[Robot] = []
    cre = re.compile(r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)$")
    for line in data:
        m = cre.match(line)
        assert m
        robots.append(Robot(
            p=complex(int(m.group(1)), int(m.group(2))),
            v=complex(int(m.group(3)), int(m.group(4))),
        ))

    if part == "a":
        # advance each robot, then increment qudrant counts
        counts = [[0, 0], [0, 0]]
        for robot in robots:
            # advance
            robot.p += 100 * robot.v
            robot.p = complex(robot.x % w, robot.y % h)
            # divide
            if robot.x != w // 2 and robot.y != h // 2:
                counts[int(robot.x < w // 2)][int(robot.y < h // 2)] += 1
        # build product
        return functools.reduce(operator.mul, sum(counts, []))

    # part b
    # it is unclear what the tree looks like, but a *guess* is that there should be at least one
    # straight, horizontal line (the first tree layer) with a minimum length; if so, print the map and check :)

    interactive = False  # disable for submission

    # helper function to check if there is a straight line
    def has_line(xs: list[int], min_len: int = 10) -> bool:
        last_x, l = -1, 0
        while xs:
            if (x := heapq.heappop(xs)) == last_x + 1:
                l += 1
                if l == min_len:
                    return True
            else:
                l = 0
            last_x = x
        return False

    for t in range(1, 100_001):
        # advance each robot, remember the x coordinates of robots per y coordinate for the line check
        x_per_y: dict[int, list[int]] = defaultdict(list)
        for robot in robots:
            robot.p += robot.v
            robot.p = complex(robot.x % w, robot.y % h)
            heapq.heappush(x_per_y[robot.y], robot.x)  # likely overkill
        # check if there is a straight line
        for xs in x_per_y.values():
            if has_line(xs):
                if interactive:
                    # print robots
                    positions = set([robot.p for robot in robots])
                    for y in range(h):
                        print("".join(("*" if complex(x, y) in positions else " ") for x in range(w)))
                    print(f"{t=}")
                    while (inp := input("accept? y/n: ").strip()) not in {"y", "n"}:
                        continue
                    if inp == "n":
                        continue
                return t

    raise ValueError("no solution found after 100k iterations :(")


if __name__ == "__main__":
    Solver(year=2024, day=14, truth_a=230172768, truth_b=8087).solve(solution, part="x", submit=False)
