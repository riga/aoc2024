# coding: utf-8

"""
https://adventofcode.com/2024/day/21
"""

from __future__ import annotations

from collections import Counter

from aoc2024 import Solver, Part


Pos = tuple[int, int]


def solution(data: list[str], part: Part) -> int | str | None:
    # i-j coordinates of number and direction pad (0,0 at top left, i to bottom, j to right)
    num_coords = {n: divmod(k, 3) for k, n in enumerate("789456123 0A")}
    dir_coords = {d: divmod(k, 3) for k, d in enumerate(" ^A<v>")}

    # helper to get direction characters given a position difference (e.g. (-2, 1) -> "^^>")
    # with the option to reverse it (e.g. in case the normal moves would cross a gap)
    # since all sequences always start at "A", there is a best order of moves: left -> down -> up -> right
    def get_move_sequence(diff_i: int, diff_j: int, *, reverse: bool) -> str:
        # compose at most two characters, repeated several times
        moves = "<" * -diff_j + "v" * diff_i + "^" * -diff_i + ">" * diff_j
        return moves[::-1] if reverse else moves

    # helper to count unique relative moves over a pad
    def get_move_counts(coords: dict[str, Pos], sequence: str, *, count: int) -> Counter[tuple[Pos, bool]]:
        # advance through the sequence of positions and remember how often each
        # unique, relative difference between coordinates occurs, and whether it crosses a gap
        pos_i, pos_j = coords["A"]
        counts: Counter[tuple[Pos, bool]] = Counter()
        for s in sequence:
            next_i, next_j = coords[s]
            # check if the path crosses a gap, and remember the relative move
            crosses_gap = coords[" "] in ((next_i, pos_j), (pos_i, next_j))
            counts[((next_i - pos_i, next_j - pos_j), crosses_gap)] += count
            pos_i, pos_j = next_i, next_j
        return counts

    # main function receiving a number code and expanding it several times into directional moves
    def expand_moves(code: str, n_dir_robots: int) -> int:
        # num code to directional moves
        counts = get_move_counts(num_coords, code, count=1)

        # expand the sequential directional moves, plus one for the final, manual one
        for _ in range(n_dir_robots + 1):
            # sum up counts to meake each single difference move of the previous iteration
            next_counts: Counter[tuple[Pos, bool]] = Counter()
            for (pos, crosses_gap), count in counts.items():
                # determine move sequence to achieve the relative position difference
                move_code = get_move_sequence(*pos, reverse=crosses_gap)
                # add counts, passing how often each difference occured (since we only care for the move lengths)
                next_counts += get_move_counts(dir_coords, move_code + "A", count=count)
            counts = next_counts

        # return the sum of counts
        return counts.total()

    # sum of complexity per move, with different number of robots on directional pads per part
    return sum(
        int(code[:-1]) * expand_moves(code, n_dir_robots=2 if part == "a" else 25)
        for code in data
    )


if __name__ == "__main__":
    Solver(year=2024, day=21, truth_a=202648, truth_b=248919739734728).solve(solution, part="x", submit=False)
