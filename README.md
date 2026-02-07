## qec v1 - Depth-Limited Benefits of Quantum Error Correction 

# Overview 

This repository contains a minimal, controlled implementation of quantum error correction (qec) designed to investigate a single research question: 

**When does quantum error correction stop improving logical fidelity as circuit depth increases under fixed noise and code parameters?** 

Rather than full fault-tolerant architecture, this v1 implementation restricts scope to isolate depth-dependent effects under reproducible and direct assumptions 

The codebase is structured to support simulation based experiments using stabilizer codes, Pauli noise models and classical decoding. 

## v1 Design Philosophy 
- **Minimal but complete**: only components required to answer the question are included 
- **Explicit assumptions**: all simplifications are documented and intentional 
- **Reproducible experiment**: fixed seeds, deterministic sweeps and saved results 
- **Research-first**: clarity taking preference over realism/performance 

This version is intended to be a research artefact not production ready QEC framework. 

## v1 Scope (Frozen) 

**Included** 
- One qec code: repetition code (bit-flip) 
- One primary noise model: bit-flip Pauli noise 
- One decoder: majority-vote
- One metric: logical failure probability 
- Repeated syndrome-extraction cycles 
- Tracking of the logical Pauli frame 
- Circuit-depth sweeps with and without qec 

**Explicitly Excluded But Future Work**
- Surface code beyond small distances 
- Advanced decoders (MWPM, neural, hardware-aware)
- Correlated noise, leakage, drift
- Hardware timing and latency 
- Magic-state distillation or logical gate synthesis 

## Core Modules in v1 

Despite the current file structure, only some files will be considered for v1: 

**src/qec/codes/repetition.py**
Defines repetition code: 
- physical qubit layout
- stabilizer generators
- logical operators 
- syndrome extraction for each correction cycle 

**src/qec/noise/channels.py**
Implements Pauli noise channels: 
- bit-flip noise applied after gates or per cycle 
- optional depolarising noise (for checks) 

**src/qec/decoding/majority_vote.py**
Implements a majority-vote decoder: 
- takes measured syndromes 
- infers the most likely correction 
- updates the logical Pauli frame

**src/qec/simulation/runner.py**
Orchestrates QEC experiments: 
- prepares logical states
- applies noise and correction cycles
- interleaves logical operations
- tracks logical failure events 

**src/qec/simulation/metrics.py**
Defines evaluation metrics: 
- logical failure probability 
- confidence intervals over repeated shots 

**src/qec/utils/seeding.py** 
For deterministic seeding: 
- ensures reproducibility across runs 
- allows fair comparison between qec enabled and unprotected circuits 

**src/qec/analysis/plots.py** 
Generates publication-quality figures: 
- logical failure vs circuit depth 
- qec vs no qec comparison 

## v1 Experiment 
**1. Fix**:
- repetition-code size 
- physical error rate 
- correction frequency
**2. Vary**: 
- logical circuit depth
**3. Compare**: 
- no error correction 
- error correction applied every cycle 
**4. Measure**: 
- logical failure probability as a function of depth 

This experiment is designed to show:
- initial benefit of qec at small depths 
- saturation or degradation at larger depths 
- dependence on noise strength and correction cadence 

## Intended Use
This repository is intended to support: 
- a focused research report/ preprint
- PhD or research-assistant applications 
- exploratory studies of qec limitations under finite resources

Not intended as a general-purpose quantum simulator. 

## Status 
- v1:  minimal implementation for depth-dependent studies 
- Further versions may expand scope only if justified by results 









