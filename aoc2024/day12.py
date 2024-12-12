# coding: utf-8

"""
https://adventofcode.com/2024/day/12
"""

from __future__ import annotations

from collections import defaultdict, deque

from aoc2024 import Solver, Part


def solution(data: list[str], part: Part) -> int | None:
    # parse into complex groups
    groups: dict[str, set[complex]] = defaultdict(set)
    for i, line in enumerate(data):
        for j, c in enumerate(line):
            groups[c].add(complex(i, j))

    # walking directions
    directions = [1, 1j, -1, -1j]

    # same region grouping structure for both parts
    price = 0
    for c, points in groups.items():
        points_left = set(points)
        while points_left:
            area, factor = 0, 0  # factor = perimeter for part a, edges for part b
            # remember seen edges for part b including direction info
            edges_seen: set[tuple[complex, complex]] = set()
            # traverse the region
            q = deque([points_left.pop()])
            while q:
                p = q.popleft()
                area += 1
                # check for edges in all directions
                for d in directions:
                    if (e := p + d) in points_left:
                        q.append(e)
                        points_left.remove(e)
                    if part == "a":
                        # increment perimeter when e is not an edge
                        if e not in points:
                            factor += 1
                    else:  # "b"
                        # increment number of sides when the edge was not seen before
                        if e not in points and (e, d) not in edges_seen:
                            factor += 1
                        # walk along the edge in both neighbor directions and find others that belong to the same side
                        # (complex direction multiplied by +-1j results in the desired perpendicular direction :))
                        for sign in (1, -1):
                            i = 0
                            while True:
                                # check if next neighbor is actually an edge to a point in the region
                                n = e + sign * (d * 1j) * i
                                if n in points or n - d not in points:
                                    break
                                edges_seen.add((n, d))
                                i += 1
            # add price
            price += area * factor

    return price


if __name__ == "__main__":
    Solver(year=2024, day=12, truth_a=1370100, truth_b=818286).solve(solution, part="x", submit=False)
