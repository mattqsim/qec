from __future__ import annotations

from dataclasses import dataclass
import random
from typing import Dict, List, Optional, Sequence

from qec.src.qec.codes.repetition import RepetitionCode
from qec.src.qec.noise.channels import BitFlipChannel
from qec.src.qec.decoding.majority_vote import MajorityVoteDecoder


def xor_bits(a: List[int], b: List[int]) -> List[int]:
    return [(ai ^ bi) & 1 for ai, bi in zip(a, b)]


def apply_mask(x: List[int], m: List[int]) -> List[int]:
    return [(xi ^ mi) & 1 for xi, mi in zip(x, m)]


def infer_data_flips_from_delta(delta: List[int], n: int, rng: random.Random) -> List[int]:
    d = delta[:]
    flips = [0] * n
    i = 0
    while i < len(d):
        if d[i] == 0:
            i += 1
            continue
        if i < len(d) - 1 and d[i + 1] == 1:
            flips[i + 1] ^= 1
            d[i] = 0
            d[i + 1] = 0
            i += 2
            continue
        if i == 0:
            flips[0] ^= 1
            d[i] = 0
            i += 1
            continue
        if i == len(d) - 1:
            flips[n - 1] ^= 1
            d[i] = 0
            i += 1
            continue
        if rng.random() < 0.5:
            flips[i] ^= 1
        else:
            flips[i + 1] ^= 1
        d[i] = 0
        i += 1
    return flips


@dataclass(frozen=True)
class RunnerConfig:
    n: int
    p: float
    shots: int
    seed: int = 0


def run_single_shot(
    *,
    code: RepetitionCode,
    noise: BitFlipChannel,
    decoder: Optional[MajorityVoteDecoder],
    depth: int,
    rng: random.Random,
) -> bool:
    x_phys = [0] * code.n_data
    x_frame = [0] * code.n_data
    syn_prev = [0] * (code.n_data - 1)

    for _ in range(depth):
        x_phys = noise.apply(x_phys, rng)
        if decoder is not None:
            x_eff = apply_mask(x_phys, x_frame)
            syn_now = code.measure_syndrome_from_x_errors(x_eff)
            delta = xor_bits(syn_prev, syn_now)
            flips = infer_data_flips_from_delta(delta, code.n_data, rng)
            x_frame = apply_mask(x_frame, flips)
            x_eff2 = apply_mask(x_phys, x_frame)
            syn_prev = code.measure_syndrome_from_x_errors(x_eff2)

    x_final = apply_mask(x_phys, x_frame) if decoder is not None else x_phys
    final_dec = MajorityVoteDecoder(n=code.n)
    return final_dec.decode(x_final)


def estimate_logical_failure_probability(
    *,
    code: RepetitionCode,
    noise: BitFlipChannel,
    decoder: Optional[MajorityVoteDecoder],
    depth: int,
    shots: int,
    seed: int,
) -> float:
    rng = random.Random(seed)
    failures = 0
    for _ in range(shots):
        if run_single_shot(code=code, noise=noise, decoder=decoder, depth=depth, rng=rng):
            failures += 1
    return failures / shots


def run_depth_sweep(
    *,
    cfg: RunnerConfig,
    depths: Sequence[int],
) -> Dict[int, Dict[str, float]]:
    code = RepetitionCode(cfg.n)
    noise = BitFlipChannel(cfg.p)
    decoder = MajorityVoteDecoder(n=cfg.n)
    results: Dict[int, Dict[str, float]] = {}
    for d in depths:
        di = int(d)
        p_no = estimate_logical_failure_probability(
            code=code,
            noise=noise,
            decoder=None,
            depth=di,
            shots=cfg.shots,
            seed=cfg.seed,
        )
        p_qec = estimate_logical_failure_probability(
            code=code,
            noise=noise,
            decoder=decoder,
            depth=di,
            shots=cfg.shots,
            seed=cfg.seed,
        )
        results[di] = {"no_qec": p_no, "qec": p_qec}
    return results
