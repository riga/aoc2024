# coding: utf-8

"""
https://adventofcode.com/2024/day/15
"""

from __future__ import annotations

from aoc2024 import Solver, Part, Point, Dim, Direction


def solution(data: list[str], part: Part) -> int | None:
    # grid scaling depending on the puzzle
    scale = (1, 1 if part == "a" else 2)

    # dimensions of objects
    robot_dim = Dim(1, 1)  # does not scale
    box_dim = wall_dim = Dim(1, 1) * scale

    # parse input
    walls: set[Point] = set()
    boxes: set[Point] = set()
    robot: Point = Point()
    moves: list[Direction] = []
    move_map = dict((c, Direction(v)) for c, v in zip("^v<>", (-1, 1, -1j, 1j)))
    for i, line in enumerate(data):
        if "#" in line:
            # find all box positions
            for j, char in enumerate(line):
                if char == "O":
                    boxes.add(Point(i, j) * scale)
                if char == "#":
                    walls.add(Point(i, j) * scale)
            # find robot position
            if not robot and (p := line.find("@")) >= 0:
                robot = Point(i, p) * scale
        else:
            # add moves
            moves.extend(move_map[char] for char in line)

    # helper to find top-left coordinates of objects that collide with a specific seed object given their dimensions
    def find_collisions(objects: set[Point], object_dim: Dim, seed: Point, seed_dim: Dim) -> set[Point]:
        start = seed - object_dim + (1, 1)  # minimum overlap
        stop = seed + seed_dim
        return {
            q
            for i in range(start.i, stop.i)
            for j in range(start.j, stop.j)
            if (q := Point(i, j)) in objects
        }

    # helper to find new positions of objects after a seed position with some dimension was potentially moved
    # returns None if any (!) collision with a wall was detected
    def get_new_positions(seed: Point, m: Direction, dim: Dim) -> list[Point] | None:
        # get the new position and check if it collides with walls
        q = seed + m
        if find_collisions(walls, wall_dim, q, dim):
            return None
        # build new positions, always putting the updated seed first
        pos = [q]
        # check colliding boxes, removing the seed object to avoid self-collisions
        for b in find_collisions(boxes, box_dim, q, dim) - {seed}:
            # stop if any box cannot be moved, otherwise add
            if (b_pos := get_new_positions(b, m, box_dim)) is None:
                return None
            pos.extend(b_pos)
        return pos

    # perform moves
    for m in moves:
        # find positions of new objects if moving all of them is possible
        if (positions := get_new_positions(robot, m, robot_dim)):
            # position 0 is the robot
            robot = positions[0]
            # all others are moved boxes, so first remove original ones
            boxes -= {b - m for b in positions[1:]}
            boxes |= set(positions[1:])

    # result
    return sum(b.i * 100 + b.j for b in boxes)


if __name__ == "__main__":
    Solver(year=2024, day=15, truth_a=1438161, truth_b=1437981).solve(solution, part="x", submit=False)
