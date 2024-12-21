# coding: utf-8

"""
https://adventofcode.com/2024/day/20
"""

from __future__ import annotations

import more_itertools

from aoc2024 import Solver, Part


def solution(data: list[str], part: Part) -> int | str | None:
    # parse positions
    h, w = len(data), len(data[0])
    start: complex = complex(0, 0)
    end: complex = complex(0, 0)
    walls: set[complex] = set()
    directions = [1, -1, 1j, -1j]
    for i, line in enumerate(data):
        for j, c in enumerate(line):
            if c == "#":
                walls.add(complex(i, j))
            elif c == "S":
                start = complex(i, j)
            elif c == "E":
                end = complex(i, j)

    # bounds helper
    def in_bounds(pos: complex) -> bool:
        return (0 <= pos.real < h) and (0 <= pos.imag < w)

    # sign helper
    def sign(x: int) -> int:
        return 1 if x >= 0 else -1

    # initial walk starting from the end, storing the distance to the end
    # (assuming the path through the maze is unique, i.e., no loops possible, no dead ends)
    distances: dict[complex, int] = {}
    pos, steps = end, 0
    while True:
        distances[pos] = steps
        if pos == start:
            break
        # just one step possible
        for d in directions:
            new_pos = pos + d
            if in_bounds(new_pos) and new_pos not in walls and new_pos not in distances:
                pos = new_pos
                steps += 1
                break
        else:
            raise ValueError("wrong assumption about maze")

    # go along path again, at each position scanning for shortcuts within a search window
    cheats = set()
    start_ends = set()
    search_window = 2 if part == "a" else 20
    min_improvement = 100
    for pos, steps_left in distances.items():
        # skip cases where no improvement is possible
        if steps_left < min_improvement:
            continue
        # within a search window, check if a shortcut is possible
        for i in range(-search_window, search_window + 1):
            for j in range(-(offset := search_window - abs(i)), offset + 1):
                # avoid trivial cheats
                if abs(diff := complex(i, j)) <= 1:
                    continue
                # must be on path
                if (new_pos := pos + diff) not in distances:
                    continue
                # test
                x = (pos, new_pos)
                if x in start_ends:
                    continue
                start_ends.add(x)
                # must be an improvement
                if steps_left - (distances[new_pos] + abs(i) + abs(j)) < min_improvement:
                    continue
                # determine all possible paths to go from pos to new_pos, call each one a cheat
                for ds in more_itertools.distinct_permutations(abs(i) * (sign(i),) + abs(j) * (sign(j) * 1j,)):
                    p, cheat = pos, []
                    for d in ds:
                        p += d
                        if p in walls:
                            cheat.append(p)
                    if cheat:
                        cheats.add(tuple(cheat))

    return len(cheats)


if __name__ == "__main__":
    Solver(year=2024, day=20, truth_a=1384, truth_b=1008542).solve(solution, part="x", submit=False)
