# coding: utf-8

"""
https://adventofcode.com/2024/day/24
"""

from __future__ import annotations

import re
from operator import and_, or_, xor
from collections import deque, defaultdict
from dataclasses import dataclass

from aoc2024 import Solver, Part


@dataclass
class Gate:
    out: str
    inp1: str
    inp2: str
    op: str

    def __post_init__(self):
        self.func = {"AND": and_, "OR": or_, "XOR": xor}[self.op]

    def __hash__(self) -> int:
        return hash(self.out)

    def has_input(self, name: str) -> bool:
        return name == self.inp1 or name == self.inp2


def solution(data: list[str], part: Part) -> int | str | None:
    # parse into gate objects and values
    gates: dict[str, Gate] = {}
    values: dict[str, int] = {}
    gate_cre = re.compile(r"^(?P<inp1>.+) (?P<op>AND|OR|XOR) (?P<inp2>.+) -> (?P<out>.+)$")
    for line in data[::-1]:
        if (m := gate_cre.match(line)):
            gate = Gate(**m.groupdict())
            gates[gate.out] = gate
        else:
            inp_name, val = line.split(": ")
            values[inp_name] = int(val)
    n_outputs = sum(1 for key in gates if key.startswith("z"))

    # helper to recursively "pull" values from inputs and a state dict
    def pull_value(name: str, state: dict[str, int]) -> int:
        if name not in state:
            gate = gates[name]
            state[name] = gate.func(pull_value(gate.inp1, state), pull_value(gate.inp2, state))
        return state[name]

    # part a: process gates as is, pulling output values one by one
    if part == "a":
        state = values.copy()
        return sum(pull_value(f"z{i:02d}", state) << i for i in range(n_outputs))

    # part b main observation after a long dive into bit addition rules: when comparing actual and expected output bits,
    # wrong gates can be identified standalone (!) if they fulfill any of the four conditions:
    # 1. XOR gate in the graph other than the first or last layer (only x/y inputs and z outputs are allowed)
    # 2. XOR gate followed by an OR gate, and none of the inputs is the first x bit (x00)
    # 3. AND gate followed by a XOR gate, and none of the inputs is the first x bit (x00)
    # 4. AND/OR gate, produces an output other than the last one (z45)

    swap_gates = []
    gate_exists = lambda inp, op: any(gate.has_input(inp) and gate.op == op for gate in gates.values())
    for gate in gates.values():
        # check swap conditions
        swap = gate.op == "XOR" and gate.inp1 not in values and gate.inp2 not in values and not gate.out.startswith("z")
        swap |= gate.op == "XOR" and gate_exists(gate.out, "OR") and not gate.has_input("x00")
        swap |= gate.op == "AND" and gate_exists(gate.out, "XOR") and not gate.has_input("x00")
        swap |= gate.op != "XOR" and gate.out.startswith("z") and gate.out != "z45"
        if swap:
            swap_gates.append(gate.out)

    return ",".join(sorted(swap_gates))


if __name__ == "__main__":
    Solver(
        year=2024,
        day=24,
        truth_a=46463754151024,
        truth_b="cqk,fph,gds,jrs,wrk,z15,z21,z34",
    ).solve(solution, part="x", example=False)
