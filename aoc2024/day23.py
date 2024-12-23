# coding: utf-8

"""
https://adventofcode.com/2024/day/23
"""

from __future__ import annotations

from collections import defaultdict
from typing import Generator

from aoc2024 import Solver, Part


# helper returning all unique, sorted combinations of values
def sorted_combinations(values: list[str] | set[str], n: int) -> Generator[tuple[str, ...], None, None]:
    def combs(values: list[str], n: int):
        if n == 1:
            # yield innermost values as 1-tuples
            for va in values:
                yield (va,)
        else:
            # iterate over leading values, skipping the last n - 1, then yield sub combinations
            for i in range(len(values) - (n - 1)):
                for vals in combs(values[i + 1:], n - 1):
                    yield (values[i],) + vals

    # perform input checks and sorting once, start recursion
    assert 0 < n <= len(values)
    yield from combs(sorted(values), n)


def solution(data: list[str], part: Part) -> int | str | None:
    # create lookup table with all connections
    # for part b: make bi-directional and add self-connections
    connections = defaultdict(set)
    for line in data:
        a, b = sorted(line.split("-"))
        connections[a].add(b)
        if part == "b":
            connections[b] |= {a, b}
            connections[a].add(a)

    # part a: find triplets, making use of the fact that keys and all value permutations will be sorted
    if part == "a":
        triplets = set()
        for a, bs in connections.items():
            # find connected pairs within b's
            if len(bs) < 2:
                continue
            for b, c in sorted_combinations(bs, 2):
                # check if connected and any of the three starts with "t"
                if c in connections.get(b, ()) and "t" in (a[0], b[0], c[0]):
                    triplets.add(tuple(sorted((a, b, c))))
        return len(triplets)

    # part b: fully-connected subnetworks are defined by their overlap of connections (needs self-connections),
    # so for each possible size (starting at the maximum), loop through connections, build distinct combinations
    # of keys of the required size, and check if their overlap is the sequence of keys itself
    for n in range(max(len(cons) for cons in connections.values()), 1, -1):
        for cons in connections.values():
            for keys in sorted_combinations(list(cons), n):
                if set(keys) == set.intersection(*(connections[key] for key in keys)):
                    return ",".join(keys)

    raise RuntimeError("no solution found :(")


if __name__ == "__main__":
    Solver(
        year=2024,
        day=23,
        truth_a=1163,
        truth_b="bm,bo,ee,fo,gt,hv,jv,kd,md,mu,nm,wx,xh",
    ).solve(solution, part="x", submit=False)
