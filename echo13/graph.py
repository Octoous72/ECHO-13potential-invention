"""
echo13.graph
============
Symbol graph data structures: nodes, edges, and the graph container.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Node:
    """A single symbol node in the graph."""

    label: str
    value: float = 0.0
    generation: int = 0
    mutated: bool = False

    def __hash__(self) -> int:
        return hash(self.label)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Node):
            return NotImplemented
        return self.label == other.label


class SymbolGraph:
    """
    A directed graph of symbol nodes connected by edges.

    Nodes are evaluated in insertion order. Edges define data flow
    from source to target (source -> target means source feeds into target).
    """

    def __init__(self) -> None:
        self._nodes: list[Node] = []
        self._edges: list[tuple[Node, Node]] = []

    @property
    def nodes(self) -> list[Node]:
        """Return all nodes in insertion order."""
        return list(self._nodes)

    def add_node(self, node: Node) -> None:
        """Add a node to the graph."""
        if any(n.label == node.label for n in self._nodes):
            raise ValueError(f"Node '{node.label}' already exists in the graph")
        self._nodes.append(node)

    @property
    def edges(self) -> list[tuple[Node, Node]]:
        """Return all edges as (source, target) tuples."""
        return list(self._edges)

    def add_edge(self, source: Node, target: Node) -> None:
        """Add a directed edge from source to target."""
        if source not in self._nodes:
            raise ValueError(f"Source node '{source.label}' not in graph")
        if target not in self._nodes:
            raise ValueError(f"Target node '{target.label}' not in graph")
        self._edges.append((source, target))

    def get_parents(self, node: Node) -> list[Node]:
        """Return all nodes that have an edge pointing TO this node."""
        return [src for src, tgt in self._edges if tgt == node]

    def get_children(self, node: Node) -> list[Node]:
        """Return all nodes that this node has an edge pointing TO."""
        return [tgt for src, tgt in self._edges if src == node]
