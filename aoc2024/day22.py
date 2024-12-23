# coding: utf-8

"""
https://adventofcode.com/2024/day/22
"""

from __future__ import annotations

from collections import deque

from aoc2024 import Solver, Part


def solution(data: list[str], part: Part) -> int | str | None:
    # initial secret per buyer
    initial_secrets: list[int] = list(map(int, data))

    # helper to simulate the sequence of random secrets
    def simulate_secrets(secret: int) -> list[int]:
        secrets = [secret]
        for _ in range(2000):
            secret = secrets[-1]
            secret = ((secret * 64) ^ secret) % 16777216
            secret = ((secret // 32) ^ secret) % 16777216
            secret = ((secret * 2048) ^ secret) % 16777216
            secrets.append(secret)
        return secrets

    # simulate all secrets
    buyers_secrets: list[list[int]] = list(map(simulate_secrets, initial_secrets))

    # part a: return the sum of the 2000th secret per buyer
    if part == "a":
        return sum(s[-1] for s in buyers_secrets)

    # part b: per buyer, create a dictionary of the four last price changes mapped to the current price; then
    # loop over all unique price change sequences (brute-force) and check which one yields the highest sum

    # helper to create the price changes -> price mapping
    def get_sequence_prices(secrets: list[int]) -> dict[tuple[int, ...], int]:
        prices = {}
        # rolling window of price changes
        window: deque[int] = deque()
        prev = secrets[0] % 10
        for secret in secrets[1:]:
            price = secret % 10
            window.append(price - prev)
            prev = price
            # add to window
            if len(window) == 4:
                seq = tuple(window)
                # only keep first price change as the monkey starts from the front as well
                if seq not in prices:
                    prices[seq] = price
                window.popleft()
        return prices

    # get all price change sequences and brute-force the best one
    prices = list(map(get_sequence_prices, map(simulate_secrets, map(int, data))))
    max_sum_price = -1
    for seq in set.union(*(set(p.keys()) for p in prices)):
        sum_price = sum(p[seq] for p in prices if seq in p)
        if sum_price > max_sum_price:
            max_sum_price = sum_price

    return max_sum_price


if __name__ == "__main__":
    Solver(year=2024, day=22, truth_a=19854248602, truth_b=2223).solve(solution, part="x", submit=False)
