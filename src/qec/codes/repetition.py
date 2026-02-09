from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable, List, Tuple

Check = Tuple[int, int] 
@dataclass(frozen=True)
class RepetitionCode: 

    n: int

    def __post_init__(self) -> None: 
        if self.n < 3: 
            raise ValueError("RepetitionCode requires n >= 3")

# Layout
    @property
    def n_data(self) -> int: 
        return self.n

    @property
    def checks(self) -> List[Check]:
        return [(i, i + 1) for i in range(self.n - 1)]

    @property
    def distance(self) -> int:
        return self.n

    @property
    def stabilizers(self) -> List[Tuple[str, Check]]:
        return [("ZZ", chk) for chk in self.checks]
    
    @property
    def logical_x(self) -> Tuple[str, Tuple[int, ...]]:
        return ("X" * self.n, tuple(range(self.n)))

    @property
    def logical_z(self) -> Tuple[str, Tuple[int, ...]]:
        return ("Z", (0,))
    
    
    def measure_syndrome_from_x_errors(self, x_errors: Iterable[int | bool]) -> List[int]: 
        xs = [1 if bool(b) else 0 for b in x_errors]
        if len(xs) != self.n: 
            raise ValueError(f"x_errors must have length {self.n}, got {len(xs)}")

        syn: List[int] = []
        for i, j in self.checks: 
            syn.append((xs[i] ^ xs[j]) & 1) 
        return syn 

    def expected_syndrome_for_single_x(self, k: int) -> List[int]:
        if not (0 <= k < self.n):
            raise ValueError("k out of range")
        x = [0] * self.n
        x[k] = 1
        return self.measure_syndrome_from_x_errors(x)

    def validate(self) -> None:
        if len(self.checks) != self.n - 1:
            raise AssertionError("checks length mismatch")
        if len(self.stabilizers) != self.n - 1:
            raise AssertionError("stabilizers length mismatch")
            
    


