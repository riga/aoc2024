# coding: utf-8

"""
https://adventofcode.com/2024/day/10
"""

from __future__ import annotations

from collections import deque

from aoc2024 import Solver, Part


def solution(data: list[str], part: Part) -> int | None:
    imax, jmax = len(data), len(data[0])

    # convert to complex mapping
    heights: dict[complex, int] = {}
    for i, line in enumerate(data):
        for j, c in enumerate(line):
            heights[complex(i, j)] = int(c)

    # find heads
    heads = [p for p, h in heights.items() if h == 0]

    # walking directions
    directions = [1 + 0j, -1 + 0j, 1j, -1j]

    # walking helper returning the number of reachable tops given a starting point
    # note: part a could be solved faster by using a decicated function that drops duplicates right away
    #       instead of at the end, but the penalty is not too high and the code is more readable
    def num_reachable_tops(head: complex, unique: bool) -> int:
        q = deque([head])
        height = 0
        # check each height
        while height < 9:
            height += 1
            for _ in range(len(q)):
                h = q.popleft()
                # check each direction
                for d in directions:
                    p = h + d
                    if (0 <= p.real < imax) and (0 <= p.imag < jmax) and heights[p] == height:
                        q.append(p)
        return len(set(q) if unique else q)

    # count reachable tops, dropped duplicates for part a
    return sum(num_reachable_tops(h, unique=(part == "a")) for h in heads)


if __name__ == "__main__":
    Solver(year=2024, day=10, truth_a=737, truth_b=1619).solve(solution, part="x", submit=False)
