# ECHO‑13 — Examples

Runnable demonstrations of the ECHO‑13 recursive symbolic engine.

## Prerequisites

| Requirement | Version |
|---|---|
| Python | 3.10 + |
| ECHO‑13 engine | installed in editable mode (`pip install -e .` from repo root) |

## File Index

| File | Purpose |
|---|---|
| `01_basic_run.py` | Minimal linear graph — one recursive pass, printed results |
| `02_parameter_variation.py` | Sweep recursion depth, mutation rate, and seed across a cyclic graph |
| `03_trace_inspection.py` | Enable tracing, inspect timeline, mutation summary, and per‑pass stats |

## Quick Start

```bash
# From the repo root
cd examples

# 1 — Basic run (no flags needed)
python 01_basic_run.py

# 2 — Parameter variation (defaults or custom grid)
python 02_parameter_variation.py
python 02_parameter_variation.py --depths 1 3 7 --rates 0.0 0.25 0.75 --seeds 42

# 3 — Trace inspection (defaults or custom pass count / JSON export)
python 03_trace_inspection.py
python 03_trace_inspection.py --passes 5 --json
