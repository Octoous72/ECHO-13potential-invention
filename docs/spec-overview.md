ECHO‑13 Specification Overview

ECHO‑13 defines a continuous unfolding computational model built from five interacting components: entities, traces, relational dynamics, braid geometry, and environmental feedback. This overview summarizes the core structures and update rules that govern the system.

1. Entities
Entities are the fundamental units of the system. Each entity has:
- tempo — rate of motion  
- density — internal mass/weight that can increase through SOR  
- phase — slow‑changing internal oscillator  
- position — 2D spatial coordinates  
- trace — complete history of positions  

Entities update deterministically each step based on direction, tempo, and time increment.

2. Traces
Traces are append‑only histories of entity motion.  
They are never deleted or compressed destructively.

Traces enable:
- braid formation  
- overlap detection  
- environmental echo accumulation  
- long‑term memory of system evolution  

3. Relational Dynamics
Pairs of entities form a relational unit.  
The key quantity is distance, which influences:

- synchrony  
- tempo harmonization  
- braid width  
- environmental response  

When entities are within a threshold, they partially synchronize their tempos.

4. Braid Geometry
Braids emerge from the intertwined traces of entity pairs.

A braid has:
- crossings — count of trace intersections  
- width — spatial separation of the pair  

Braid geometry influences environmental curvature and echo.

5. Soft Overlap Compression (SOR)
SOR increases density when traces overlap significantly.

Properties:
- non‑destructive  
- logarithmic growth  
- preserves all history  
- increases internal weight without erasing structure  

SOR is a key mechanism for memory accumulation.

6. Environment
The environment responds to braid activity and entity motion.

It tracks:
- echo — accumulated influence of braid width  
- curvature — response to crossings  
- sediment — slow global accumulation  

The environment does not control entities but reflects their unfolding.

---

System Evolution
Each step of the engine performs:

1. Entity motion  
2. Trace extension  
3. Relational evaluation  
4. Tempo harmonization  
5. Braid update  
6. Environmental update  
7. Soft Overlap Compression  

This produces a deterministic, interpretable unfolding process.

---
