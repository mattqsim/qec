from __future__ import annotations

from typing import Dict, Sequence, Optional
import math

import matplotlib.pyplot as plt

from qec.src.qec.simulation.metrics import Estimate


def plot_depth_sweep(
    results: Dict[int, Dict[str, Estimate]],
    *,
    title: str = "Logical failure probability vs depth",
    logy: bool = False,
    show: bool = True,
    savepath: Optional[str] = None,
) -> None:
    depths = sorted(results.keys())

    def series(key: str):
        ys = [results[d][key].p for d in depths]
        ylo = [results[d][key].p - results[d][key].lo for d in depths]
        yhi = [results[d][key].hi - results[d][key].p for d in depths]
        return ys, [ylo, yhi]

    no_y, no_err = series("no_qec")
    q_y, q_err = series("qec")

    plt.figure()
    plt.errorbar(depths, no_y, yerr=no_err, marker="o", linestyle="-", label="no_qec")
    plt.errorbar(depths, q_y, yerr=q_err, marker="o", linestyle="-", label="qec")
    plt.xlabel("Depth (QEC cycles)")
    plt.ylabel("Logical failure probability")
    plt.title(title)
    plt.legend()

    if logy:
        plt.yscale("log")

    plt.tight_layout()

    if savepath is not None:
        plt.savefig(savepath, dpi=200)

    if show:
        plt.show()
    else:
        plt.close()


def plot_vs_n_at_fixed_depth(
    results_by_n: Dict[int, Dict[str, Estimate]],
    *,
    title: str,
    logy: bool = True,
    show: bool = True,
    savepath: Optional[str] = None,
) -> None:
    ns = sorted(results_by_n.keys())
    ys = [results_by_n[n]["qec"].p for n in ns]
    ylo = [results_by_n[n]["qec"].p - results_by_n[n]["qec"].lo for n in ns]
    yhi = [results_by_n[n]["qec"].hi - results_by_n[n]["qec"].p for n in ns]

    plt.figure()
    plt.errorbar(ns, ys, yerr=[ylo, yhi], marker="o", linestyle="-", label="qec")
    plt.xlabel("n (data qubits)")
    plt.ylabel("Logical failure probability (QEC)")
    plt.title(title)
    plt.legend()

    if logy:
        plt.yscale("log")

    plt.tight_layout()

    if savepath is not None:
        plt.savefig(savepath, dpi=200)

    if show:
        plt.show()
    else:
        plt.close()

