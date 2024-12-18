# coding: utf-8

"""
https://adventofcode.com/2024/day/18
"""

from __future__ import annotations

from collections import deque

from aoc2024 import Solver, Part


def solution(data: list[str], part: Part) -> int | str | None:
    h = w = 71
    cutoff = 1024

    # parse byte positions
    bytes = {complex(y, x) for x, y in (map(int, line.split(",")) for line in data[:cutoff])}
    next_bytes = deque([complex(y, x) for x, y in (map(int, line.split(",")) for line in data[cutoff:])])
    # add some fencing
    bytes |= {complex(i, -1) for i in range(-1, h + 1)}  # left
    bytes |= {complex(i, w) for i in range(-1, h + 1)}  # right
    bytes |= {complex(-1, j) for j in range(-1, w + 1)}  # top
    bytes |= {complex(h, j) for j in range(-1, w + 1)}  # bottom

    # points
    start = complex(0, 0)
    end = complex(h - 1, w - 1)
    directions = [1, -1, 1j, -1j]

    # walking function, returning the number of steps to reach the end, or None if not possible
    def walk() -> int | None:
        # bfs-like search, exploring all yet unseen next fields with the same number of steps at the same time
        steps = 0
        leaves: set[complex] = {start}
        seen: set[complex] = set()
        while leaves and end not in leaves:
            # given the current "leaves", advance to all next, unseen leaves
            new_leaves = set()
            for pos in leaves:
                for d in directions:
                    new_pos = pos + d
                    if new_pos not in seen and new_pos not in bytes:
                        new_leaves.add(new_pos)
                        seen.add(new_pos)
            leaves = new_leaves
            steps += 1
        # no solution possible if no more leaves were around at the end
        return steps if leaves else None

    # part a: just walk on the first batch of bytes
    if part == "a":
        return walk()

    # part b: iteratively add more bytes until no solution is possible (brute-force)
    while next_bytes:
        bytes.add(b := next_bytes.popleft())
        if walk() is None:
            return f"{int(b.imag)},{int(b.real)}"

    raise ValueError("no solution found :(")


if __name__ == "__main__":
    Solver(year=2024, day=18, truth_a=294, truth_b="31,22").solve(solution, part="x", submit=False)
