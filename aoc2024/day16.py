# coding: utf-8

"""
https://adventofcode.com/2024/day/16
"""

from __future__ import annotations

import heapq
import operator
import functools
from dataclasses import dataclass

from aoc2024 import Solver, Part, Point


# derived types
class Direction(Point): pass  # noqa: E701


@dataclass
class Path:
    pos: Point
    dir: Direction
    score: int
    visited: set[Point]

    def __lt__(self, other: Path) -> bool:  # for heapq ordering
        return self.score < other.score


def solution(data: list[str], part: Part) -> int | None:
    # find start and end points, remember walls
    start: Point = Point()
    end: Point = Point()
    walls: set[Point] = set()
    for i, line in enumerate(data):
        for j, c in enumerate(line):
            if not start and c == "S":
                start = Point(i, j)
            elif not end and c == "E":
                end = Point(i, j)
            elif c == "#":
                walls.add(Point(i, j))

    # walk one step at a time, always choosing the most promising path
    directions = [Direction(1j), Direction(-1j), Direction(1), Direction(-1)]  # EWSN
    paths: list[Path] = [Path(start, directions[0], 0, {start})]
    visited: dict[tuple[Point, Direction], int] = {}
    best_paths: list[Path] = []
    while paths:
        path = heapq.heappop(paths)
        # additional stopping criterion for part b (no effect for part a):
        # no need to continue if there were better paths
        if best_paths and path.score > best_paths[0].score:
            break
        # check if end is reached
        if path.pos == end:
            best_paths.append(path)
            # we can stop here for part a, but need to keep looking for part b
            if part == "a":
                break
            continue
        # check if visited already with a better score
        if visited.get((path.pos, path.dir), float("inf")) < path.score:
            continue
        visited[(path.pos, path.dir)] = path.score
        # check possible next moves
        for d in directions:
            # skip going backwards
            if d == -path.dir:
                continue
            # skip walls
            if (new_pos := path.pos + d) in walls:
                continue
            # add to paths, either walk straight or turn
            if d is path.dir:
                new_path = Path(new_pos, d, path.score + 1, path.visited | {new_pos})
            else:
                new_path = Path(path.pos, d, path.score + 1000, path.visited)
            heapq.heappush(paths, new_path)

    if part == "a":
        # just return score
        return best_paths[0].score

    # part b: intersect visited fields
    return len(functools.reduce(operator.or_, (p.visited for p in best_paths)))


if __name__ == "__main__":
    Solver(year=2024, day=16, truth_a=83432, truth_b=467).solve(solution, part="x", submit=False)
