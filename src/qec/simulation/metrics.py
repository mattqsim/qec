from __future__ import annotations

from dataclasses import dataclass
import math
import random
from typing import Dict, Optional, Sequence

from qec.src.qec.codes.repetition import RepetitionCode
from qec.src.qec.noise.channels import BitFlipChannel
from qec.src.qec.decoding.majority_vote import MajorityVoteDecoder
from qec.src.qec.simulation.runner import run_single_shot, RunnerConfig


def _z_value(alpha: float) -> float:
    lookup = {
        0.10: 1.6448536269514722,
        0.05: 1.959963984540054,
        0.01: 2.5758293035489004,
        0.001: 3.2905267314919255,
    }
    return lookup.get(float(alpha), 1.959963984540054)


def wilson_interval(failures: int, shots: int, alpha: float = 0.05) -> tuple[float, float]:
    if shots <= 0:
        raise ValueError("shots must be > 0")
    if failures < 0 or failures > shots:
        raise ValueError("failures must be in [0, shots]")

    z = _z_value(alpha)
    n = float(shots)
    p = failures / n
    z2 = z * z
    denom = 1.0 + z2 / n
    center = (p + z2 / (2.0 * n)) / denom
    rad = z * math.sqrt((p * (1.0 - p) / n) + (z2 / (4.0 * n * n))) / denom
    lo = max(0.0, center - rad)
    hi = min(1.0, center + rad)
    return lo, hi


@dataclass(frozen=True)
class Estimate:
    p: float
    lo: float
    hi: float
    failures: int
    shots: int


def estimate_with_ci(
    *,
    code: RepetitionCode,
    noise: BitFlipChannel,
    decoder: Optional[MajorityVoteDecoder],
    depth: int,
    shots: int,
    seed: int,
    alpha: float = 0.05,
) -> Estimate:
    rng = random.Random(seed)
    failures = 0
    for _ in range(shots):
        if run_single_shot(code=code, noise=noise, decoder=decoder, depth=int(depth), rng=rng):
            failures += 1
    p = failures / shots
    lo, hi = wilson_interval(failures, shots, alpha=alpha)
    return Estimate(p=p, lo=lo, hi=hi, failures=failures, shots=shots)


def depth_sweep_with_ci(
    *,
    cfg: RunnerConfig,
    depths: Sequence[int],
    alpha: float = 0.05,
) -> Dict[int, Dict[str, Estimate]]:
    code = RepetitionCode(cfg.n)
    noise = BitFlipChannel(cfg.p)
    decoder = MajorityVoteDecoder(n=cfg.n)

    out: Dict[int, Dict[str, Estimate]] = {}
    for d in depths:
        di = int(d)
        out[di] = {
            "no_qec": estimate_with_ci(
                code=code, noise=noise, decoder=None, depth=di, shots=cfg.shots, seed=cfg.seed, alpha=alpha
            ),
            "qec": estimate_with_ci(
                code=code, noise=noise, decoder=decoder, depth=di, shots=cfg.shots, seed=cfg.seed, alpha=alpha
            ),
        }
    return out

