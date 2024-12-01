# coding: utf8

from __future__ import annotations

import os
import inspect
from typing import Callable, Literal

# set the aoc session when missing
if not os.getenv("AOC_SESSION", ""):
    this_dir = os.path.dirname(os.path.abspath(__file__))
    session_file = os.path.join(os.path.dirname(this_dir), ".aoc_session")
    if os.path.exists(session_file):
        with open(session_file) as f:
            os.environ["AOC_SESSION"] = f.read().strip()

import aocd


Part = Literal["a", "b", "x"]


class Solver:
    """
    Puzzle solver class, helping with repeated tasks like input fetching and solution submission.
    Requires the ``AOC_SESSION`` env var to be set. Use as:

    .. code-block:: python

        def solution(data: list[str], part: Part) -> int | None:
            # ...
            return None

        Solver(year=..., day=...).solve(solution, part="a")
    """

    def __init__(
        self,
        *,
        year: int,
        day: int,
        truth_a: int | None = None,
        truth_b: int | None = None,
    ) -> None:
        super().__init__()

        # attributes
        self.year = year
        self.day = day
        self.truth_a = truth_a
        self.truth_b = truth_b

        # deferred aocd puzzle handle
        self._puzzle: aocd.models.Puzzle | None = None

    @property
    def puzzle(self) -> aocd.models.Puzzle:
        if self._puzzle is None:
            self._puzzle = aocd.get_puzzle(year=self.year, day=self.day)
        return self._puzzle

    @property
    def has_puzzle(self) -> bool:
        return self._puzzle is not None

    @property
    def has_session(self) -> bool:
        return bool(os.getenv("AOC_SESSION", ""))

    def solve(
        self,
        func: Callable[[list[str], Part], int | None],
        /,
        *,
        part: Part,
        submit: bool = True,
        example: bool = False,
        example_index: int = 0,
        strip: bool = True,
    ) -> None:
        assert part in ("a", "b", "x")

        # solve both parts when "x" is given
        if part == "x":
            self.solve(func, part="a", submit=submit, example=example, example_index=example_index)
            print("-" * 50)
            self.solve(func, part="b", submit=submit, example=example, example_index=example_index)
            return

        # puzzle identifier
        puzzle_id = f"{self.year}_{self.day:02d}_{part}"
        if example:
            puzzle_id += f"_example{example_index or ''}"

        # fetch data from local file, fallback to aocd
        data_dir = os.path.dirname(inspect.getfile(func))
        data_name = f"example{example_index or ''}.txt" if example else "data.txt"
        data_path = os.path.join(data_dir, data_name)
        if os.path.exists(data_path):
            data_raw = open(data_path).read()
        else:
            data_raw = (self.puzzle.examples[0] if example else self.puzzle).input_data
            with open(data_path, "w") as f:
                f.write(data_raw)

        # split into lines
        data = data_raw.splitlines()
        if strip:
            data = [line for line in (line.strip() for line in data) if line]

        # run the solution function
        result = func(data, part)

        # handle the result
        if result is None:
            print(f"{puzzle_id}: no solution provided")
            return
        print(f"{puzzle_id}: {result}")
        if not example and (truth := getattr(self, f"truth_{part}")) is not None:
            print(f"{'✅' if result == truth else '❌'} truth : {truth}")

        # check if submission is an option
        if example and submit:
            submit = False
        if submit:
            if not self.has_puzzle and not self.has_session:
                print("❌ submission requires AOC_SESSION")
                submit = False
            elif self.puzzle.answered(part):
                print("✅ puzzle already answered")
                submit = False

        # get interactive confirmation
        if submit:
            inp = ""
            try:
                while inp not in ("y", "n"):
                    inp = input("submit? (y/n): ").lower()
            except KeyboardInterrupt:
                print("aborted")
                return
            submit = inp == "y"

        # actual submission
        if submit:
            setattr(self.puzzle, f"answer_{part}", result)
