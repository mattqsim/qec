from __future__ import annotations
from dataclasses import dataclass
import random
from typing import List


@dataclass(frozen=True)
class BitFlipChannel: 
    p: float 

    def __post_init__(self) -> None: 
        if not (0.0 <= self.p <= 1.0): 
            raise ValueError("p must be in [0, 1]")
    
    def apply(self, x_errors: List[int], rng: random.Random) -> List[int]: 
        out = x_errors[:]
        for i in range(len(out)): 
            if rng.random() < self.p: 
                out[i] ^= 1

        return out 
        

            