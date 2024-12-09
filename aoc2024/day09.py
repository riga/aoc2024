# coding: utf-8

"""
https://adventofcode.com/2024/day/9
"""

from __future__ import annotations

from collections import deque

from aoc2024 import Solver, Part


def solution(data: list[str], part: Part) -> int | None:
    # convert single line into stream of blocks and store file ids (assuming odd length)
    stream = deque(map(int, data[0]))
    file_ids = deque(range(len(stream) // 2 + 1))
    assert len(stream) % 2 == 1

    # helper to add to the checksum and advance the current index
    index_checksum = [0, 0]
    def add(fid: int, n: int) -> None:
        index_checksum[1] += fid * (2 * index_checksum[0] + n - 1) * n // 2
        index_checksum[0] += n
        # same as
        # for _ in range(n):
        #     index_checksum[1] += fid * index_checksum[0]
        #     index_checksum[0] += 1

    if part == "a":
        # switch between handling a file and free space during traversal
        is_file = True
        overflow: deque[int] = deque()
        while stream:
            if is_file:
                # just increment checksum
                fid, n = file_ids.popleft(), stream.popleft()
                add(fid, n)
            else:
                # fill overflow with files from back until space is filled
                space = stream.popleft()
                while len(overflow) < space:
                    overflow.extend(stream.pop() * [file_ids.pop()])
                    # stream has space at the end, so remove it
                    stream.pop()
                # advance checksum with overflow values
                for _ in range(space):
                    add(overflow.popleft(), 1)
            # toggle mode
            is_file = not is_file
        # handle remaining overflow
        for fid in overflow:
            add(fid, 1)

    else:  # "b"
        # switch between handling a file and free space during traversal
        is_file = True
        moved: set[int] = set()
        while stream:
            if is_file:
                fid, n = file_ids.popleft(), stream.popleft()
                # when already moved (during space handling), just move checksum pointer, otherwise add
                add(0 if fid in moved else fid, n)
                moved.add(fid)
            else:
                # to fill space, traverse backwards through stream and fill with matching files until filled
                space = stream.popleft()
                for i in range(len(file_ids) - 1, -1, -1):
                    # skip if already moved
                    fid = file_ids[i]
                    if fid in moved:
                        continue
                    # check if file fits into space
                    if stream[2 * i] <= space:
                        add(fid, stream[2 * i])
                        moved.add(fid)
                        # reduce space and potentially stop
                        space -= stream[2 * i]
                        if space <= 0:
                            break
                else:
                    # handling remaining space, just treat as zeros
                    add(0, space)
            # toggle mode
            is_file = not is_file

    return index_checksum[1]


if __name__ == "__main__":
    Solver(year=2024, day=9, truth_a=6432869891895, truth_b=6467290479134).solve(solution, part="x", submit=False)
