from __future__ import annotations
import random
from typing import Iterator


def make_rng(seed: int) -> random.Random:
    return random.Random(int(seed))


def spawn_rngs(seed: int, n: int) -> Iterator[random.Random]:
    base = random.Random(int(seed))
    for _ in range(n):
        yield random.Random(base.randrange(2**63))

