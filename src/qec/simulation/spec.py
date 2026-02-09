from dataclasses import dataclass

@dataclass(frozen=True)
class ExperimentSpec:
    code: str
    n: int
    p: float
    depth: int
    shots: int
    seed: int
    decoder: str
