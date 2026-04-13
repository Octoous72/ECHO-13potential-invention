
#!/usr/bin/env python3
"""
02_parameter_variation.py — ECHO‑13 Parameter Sweep
=====================================================
Demonstrates how varying recursion depth, mutation rate, and random seed
affects the behaviour of the ECHO‑13 engine on a cyclic symbol graph.

What this script does
---------------------
1. Builds a CYCLIC graph:  α → β → γ → α  (stresses recursive evaluation).
2. Sweeps a configurable grid of recursion depths, mutation rates, and seeds.
3. Prints a side‑by‑side comparison table of mutations, timing, and final
   node values for every combination.
4. Highlights the trial that produced the most mutations.

Run
---
    # Use defaults
    python 02_parameter_variation.py

    # Custom grid
    python 02_parameter_variation.py --depths 1 3 7 --rates 0.0 0.25 0.75 --seeds 42
"""

from __future__ import annotations

import argparse
import time
from dataclasses import dataclass

from echo13.engine import EngineConfig, Session
from echo13.graph import Node, SymbolGraph


# ── Data container for one trial ────────────────────────────────────────
@dataclass
class TrialResult:
    depth: int
    rate: float
    seed: int
    mutations: int
    elapsed_ms: float
    final_values: dict[str, float]


# ── Graph builder ───────────────────────────────────────────────────────
def build_cyclic_graph() -> SymbolGraph:
    """Return a fresh cyclic graph:  α → β → γ → α"""
    graph = SymbolGraph()

    alpha = Node(label="α", value=1.0)
    beta  = Node(label="β", value=2.0)
    gamma = Node(label="γ", value=3.0)

    graph.add_node(alpha)
    graph.add_node(beta)
    graph.add_node(gamma)

    graph.add_edge(alpha, beta)
    graph.add_edge(beta, gamma)
    graph.add_edge(gamma, alpha)   # closes the cycle

    return graph


# ── Single trial runner ─────────────────────────────────────────────────
def run_trial(depth: int, rate: float, seed: int) -> TrialResult:
    config = EngineConfig(
        recursion_depth=depth,
        mutation_rate=rate,
        seed=seed,
    )
    graph = build_cyclic_graph()
    session = Session(config=config, graph=graph)

    start = time.perf_counter()
    session.run()
    elapsed_ms = (time.perf_counter() - start) * 1000.0

    mutations = sum(1 for n in session.graph.nodes if n.mutated)
    final_values = {n.label: n.value for n in session.graph.nodes}

    return TrialResult(
        depth=depth,
        rate=rate,
        seed=seed,
        mutations=mutations,
        elapsed_ms=elapsed_ms,
        final_values=final_values,
    )


# ── CLI ─────────────────────────────────────────────────────────────────
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="ECHO‑13 parameter‑variation sweep",
    )
    parser.add_argument(
        "--depths", nargs="+", type=int, default=[1, 3, 5],
        help="Recursion depths to test (default: 1 3 5)",
    )
    parser.add_argument(
        "--rates", nargs="+", type=float, default=[0.0, 0.5, 1.0],
        help="Mutation rates to test (default: 0.0 0.5 1.0)",
    )
    parser.add_argument(
        "--seeds", nargs="+", type=int, default=[42, 99],
        help="Random seeds to test (default: 42 99)",
    )
    return parser.parse_args()


# ── Main ────────────────────────────────────────────────────────────────
def main() -> None:
    args = parse_args()

    print("=" * 72)
    print("ECHO‑13  ·  Parameter Variation Sweep")
    print("=" * 72)
    print(f"Depths : {args.depths}")
    print(f"Rates  : {args.rates}")
    print(f"Seeds  : {args.seeds}")
    total = len(args.depths) * len(args.rates) * len(args.seeds)
    print(f"Trials : {total}")
    print("-" * 72)

    header = (
        f"{'Depth':>6} {'Rate':>6} {'Seed':>6} "
        f"{'Mut':>5} {'ms':>8} "
        f"{'α':>8} {'β':>8} {'γ':>8}"
    )
    print(header)
    print("-" * 72)

    results: list[TrialResult] = []

    for depth in args.depths:
        for rate in args.rates:
            for seed in args.seeds:
                result = run_trial(depth, rate, seed)
                results.append(result)

                print(
                    f"{result.depth:>6} "
                    f"{result.rate:>6.2f} "
                    f"{result.seed:>6} "
                    f"{result.mutations:>5} "
                    f"{result.elapsed_ms:>8.2f} "
                    f"{result.final_values.get('α', 0):>8.4f} "
                    f"{result.final_values.get('β', 0):>8.4f} "
                    f"{result.final_values.get('γ', 0):>8.4f}"
                )

    # ── Highlight the highest‑mutation trial ────────────────────────────
    print("-" * 72)
    best = max(results, key=lambda r: r.mutations)
    print(
        f"⚡ Most mutations: depth={best.depth}, rate={best.rate}, "
        f"seed={best.seed} → {best.mutations} mutation(s)"
    )
    print("=" * 72)


if __name__ == "__main__":
    main()
