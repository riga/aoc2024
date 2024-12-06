# coding: utf-8

"""
https://adventofcode.com/2024/day/6
"""

from __future__ import annotations

from aoc2024 import Solver, Part


Point = tuple[int, int]
Points = set[Point]
Direction = tuple[int, int]
PointsWithDirection = set[tuple[Point, Direction]]


def solution(data: list[str], part: Part) -> int | None:
    # find the starting point
    imax, jmax = len(data), len(data[0])
    start: Point
    for i in range(imax):
        if "^" in data[i]:
            start = i, data[i].index("^")
            break

    # walking rules
    up, down, left, right = (-1, 0), (1, 0), (0, -1), (0, 1)
    next_dir = {
        up: right,
        right: down,
        down: left,
        left: up,
    }

    # helper to walk over the map, returns visited points or an empty set in case a loop is found
    def walk(*, insert_obstacle: Point | None = None) -> Points:
        seen: Points = set()
        seen_dir: PointsWithDirection = set()
        point, direction = start, up
        while True:
            # loop detected if the point was already visited with the same direction
            if (pwd := (point, direction)) in seen_dir:
                return set()
            seen_dir.add(pwd)
            # store the current point
            seen.add(point)
            # if the next move brings us out of bounds, the walking is done
            inext, jnext = point[0] + direction[0], point[1] + direction[1]
            if not (0 <= inext < imax) or not (0 <= jnext < jmax):
                return seen
            # switch directions if the next move is an obstacle, otherwise advance
            if data[inext][jnext] == "#" or (inext, jnext) == insert_obstacle:
                direction = next_dir[direction]
            else:
                point = inext, jnext

    # get points visited by the guard, don't assume a loop in part a
    points = walk()
    if part == "a":
        return len(points)

    # part b
    # the optimal solution would be:
    #   - at every new position, open up a temporary walking branch after switching the next direction
    #   - go straight on this branch
    #   - if an obstacle is found or the end of the map is reached, stop this branch and make a step on the main branch
    #   - if a points is found that was already seen while walking in the same direction, an obstacle could have been
    #     placed in front of the point the temporary branch started from
    # ... but brute force is also rather quick, so check potential obstacles at all positions we visited in part a
    return sum(
        1 for point in points - {start}
        if not walk(insert_obstacle=point)
    )


if __name__ == "__main__":
    Solver(year=2024, day=6, truth_a=4696, truth_b=1443).solve(solution, part="x", submit=False)
