# coding: utf-8

"""
https://adventofcode.com/2024/day/20
"""

from __future__ import annotations

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
            if (0 <= pos.real < h) and (0 <= pos.imag < w) and new_pos not in walls and new_pos not in distances:
                pos = new_pos
                steps += 1
                break
        else:
            raise ValueError("wrong assumption about maze")

    # go along the path again, at each position scanning for cheats within a search window
    # each cheat is identified by its start and end points only!
    search_window = 2 if part == "a" else 20
    min_improvement = 100
    cheats: set[tuple[complex, complex]] = set()
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
                # must be an improvement
                if steps_left - (distances[new_pos] + abs(i) + abs(j)) < min_improvement:
                    continue
                # add the cheat, identified by the two positions
                cheats.add((pos, new_pos))

    return len(cheats)


if __name__ == "__main__":
    Solver(year=2024, day=20, truth_a=1384, truth_b=1008542).solve(solution, part="x", submit=False)
