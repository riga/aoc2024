# coding: utf-8

"""
https://adventofcode.com/2024/day/17
"""

from __future__ import annotations

from collections import deque

from aoc2024 import Solver, Part


def solution(data: list[str], part: Part) -> int | str | None:
    # parse data into registers and program instructions
    a, b, c = (int(line.rsplit(" ", 1)[-1]) for line in data[:3])
    prog = list(int(i) for i in data[3].rsplit(" ")[-1].split(","))

    # helper to run the program once
    def run(a: int, b: int, c: int, verbose: bool = False) -> list[int]:
        # helper to get combo operand
        combo = lambda i: i if i <= 3 else [a, b, c][i - 4]
        # helpers for logging things (part b)
        log = print if verbose else (lambda *args: None)
        combo_str = lambda i: str(i) if i <= 3 else "abc"[i - 4]
        # process instructions
        out: list[int] = []
        ptr = 0
        while ptr < len(prog) - 1:
            opcode, operand = prog[ptr], prog[ptr + 1]
            ptr += 2
            if opcode == 0:  # adv
                a = int(a / (1 << combo(operand)))
                log(f"a = a // 1<<{combo_str(operand)}")
            elif opcode == 1:  # bxl
                b ^= operand
                log(f"b = b ^ {operand}")
            elif opcode == 2:  # bst
                b = combo(operand) % 8
                log(f"b = {combo_str(operand)} % 8")
            elif opcode == 3:  # jnz
                if a != 0:
                    ptr = operand
                    log(f"ptr = {operand}")
            elif opcode == 4:  # bxc
                b ^= c
                log("b = b ^ c")
            elif opcode == 5:  # out
                out.append(combo(operand) % 8)
                log(f"out -> {combo_str(operand)} % 8  ({out[-1]})")
            elif opcode == 6:  # bdv
                b = int(a / (1 << combo(operand)))
                log(f"b = a // 1<<{combo_str(operand)}")
            else:  # cdv
                c = int(a / (1 << combo(operand)))
                log(f"c = a // 1<<{combo_str(operand)}")
        return out

    # part a: just run with given input
    if part == "a":
        return ",".join(map(str, run(a, b, c)))

    # part b: running the program verbosely shows that the instructions repeat in a pattern
    # run(prog, 1000, b, c, verbose=True)
    # ->
    #   b = a % 8
    #   b = b ^ 1
    #   c = a // 1<<b
    #   a = a // 1<<3
    #   b = b ^ 4
    #   b = b ^ c
    #   out -> b % 8
    #   ptr = 0
    # this can be inlined to
    #   set a
    #   out -> ((((a % 8) ^ 1) ^ 4) ^ (a // (1 << ((a % 8) ^ 1)))) % 8
    #   a = a // 1<<3  # assumption: this is generic for all inputs
    #   ptr 0
    # so one could check from the back which a value matches the end of the program and then work towards the front
    # the update rule for a is a // 8 and is lossy, but to invert it, we can try all eight possible previous values :)
    # also, use the run() helper above instead of the inlined form since the latter might not generalize to all inputs
    q = deque([(len(prog) - 1, 0)])
    while q:
        offset, prev_a = q.popleft()
        # try all eight possible values
        for i in range(8):
            a = prev_a * 8 + i
            # of the end matches, proceed or stop
            if run(a, b, c) == prog[offset:]:
                # the whole sequence matches
                if offset == 0:
                    return a
                # make one step to the front
                q.append((offset - 1, a))

    raise ValueError("no solution found :(")


if __name__ == "__main__":
    Solver(year=2024, day=17, truth_a="4,0,4,7,1,2,7,1,6", truth_b=202322348616234).solve(solution, part="x", submit=False)  # noqa
