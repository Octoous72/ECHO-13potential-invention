
"""
echo13.engine
=============
Core engine components: configuration, session management, and execution.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from echo13.graph import SymbolGraph


@dataclass
class EngineConfig:
    """Configuration for an ECHO-13 engine session."""

    recursion_depth: int = 1
    mutation_rate: float = 0.0
    seed: int = 42
    enable_tracing: bool = False

    def __post_init__(self) -> None:
        if self.recursion_depth < 1:
            raise ValueError("recursion_depth must be >= 1")
        if not (0.0 <= self.mutation_rate <= 1.0):
            raise ValueError("mutation_rate must be between 0.0 and 1.0")


class Session:
    """
    Manages graph execution across one or more recursive passes.

    Parameters
    ----------
    config : EngineConfig
        Engine configuration for this session.
    graph : SymbolGraph
        The symbol graph to evaluate.
    """

    def __init__(self, config: EngineConfig, graph: SymbolGraph) -> None:
        self.config = config
        self.graph = graph
        self._rng = random.Random(config.seed)
        self._trace: list[dict] = []

    def run(self, pass_id: int = 1) -> None:
        """
        Execute one recursive pass over the graph.

        Parameters
        ----------
        pass_id : int
            Identifier for this pass (used in trace output).
        """
        for depth in range(self.config.recursion_depth):
            for node in self.graph.nodes:
                parents = self.graph.get_parents(node)
                if parents:
                    incoming = sum(p.value for p in parents)
                    node.value = (node.value + incoming) / (len(parents) + 1)

                mutated = False
                if self._rng.random() < self.config.mutation_rate:
                    node.value *= 1.0 + (self._rng.random() - 0.5) * 0.2
                    node.mutated = True
                    mutated = True

                node.generation += 1

                if self.config.enable_tracing:
                    self._trace.append({
                        "pass": pass_id,
                        "depth": depth,
                        "kind": "evaluate",
                        "node": node.label,
                        "value": round(node.value, 6),
                        "mutated": mutated,
                    })

    def get_trace(self) -> list[dict]:
        """Return the accumulated trace events."""
        return list(self._trace)
