from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence


@dataclass
class MajorityVoteDecoder: 
    n: int

    def decode(self, x_errors: Sequence[int]) -> bool: 
        """
        Return True if a logical X error is found via majority vote
        """
        ones = sum(1 for b in x_errors if int(b) != 0) 
        return ones > self.n // 2