# ------------------------------------------------------------
# ECHO‑13 Minimal Reference Implementation (Research Version)
# Deterministic, dependency‑free, single‑file engine
# ------------------------------------------------------------
import math
import random

# ------------------------------------------------------------
# Entity
# ------------------------------------------------------------
class Entity:
    def __init__(self, name, tempo, density, phase, position):
        self.name = name
        self.tempo = tempo
        self.density = density
        self.phase = phase
        self.position = position
        self.trace = [position]

    def update(self, direction, dt):
        x, y = self.position
        dx, dy = direction
        new_pos = (x + self.tempo * dx * dt, y + self.tempo * dy * dt)
        self.position = new_pos
        self.trace.append(new_pos)
        self.phase += 0.01 * dt


# ------------------------------------------------------------
# Relational Pair
# ------------------------------------------------------------
class Pair:
    def __init__(self, A, B):
        self.A = A
        self.B = B

    def distance(self):
        ax, ay = self.A.position
        bx, by = self.B.position
        return math.sqrt((ax - bx)**2 + (ay - by)**2)

    def harmonize(self):
        mean = (self.A.tempo + self.B.tempo) / 2
        self.A.tempo = (self.A.tempo + mean) / 2
        self.B.tempo = (self.B.tempo + mean) / 2


# ------------------------------------------------------------
# Braid
# ------------------------------------------------------------
class Braid:
    def __init__(self, pair):
        self.pair = pair
        self.crossings = 0
        self.width = 0

    def update(self):
        A = self.pair.A.trace
        B = self.pair.B.trace
        self.crossings = min(len(A), len(B)) // 12
        self.width = self.pair.distance()


# ------------------------------------------------------------
# Environment
# ------------------------------------------------------------
class Environment:
    def __init__(self):
        self.sediment = 0
        self.curvature = 0
        self.echo = 0

    def update(self, braid):
        self.echo += 0.001 * braid.width
        self.curvature += 0.0005 * braid.crossings
        self.sediment += 0.0001


# ------------------------------------------------------------
# Soft Overlap Compression
# ------------------------------------------------------------
def soft_overlap_compression(A, B, threshold=0.05):
    overlap = 0
    for p in A.trace:
        if p in B.trace:
            overlap += 1

    ratio = overlap / max(len(A.trace), len(B.trace))

    if ratio > threshold:
        k = 0.5
        A.density += k * math.log(1 + overlap)
        B.density += k * math.log(1 + overlap)


# ------------------------------------------------------------
# Unfolding Engine
# ------------------------------------------------------------
def run_echo13(steps=200, dt=0.1):
    random.seed(13)

    A = Entity("A", tempo=0.4, density=0.7, phase=0, position=(0, 0))
    B = Entity("B", tempo=0.38, density=0.8, phase=0, position=(0.2, 0))

    pair = Pair(A, B)
    braid = Braid(pair)
    env = Environment()

    for step in range(steps):
        direction_A = (1, 0)
        direction_B = (-1, 0)

        A.update(direction_A, dt)
        B.update(direction_B, dt)

        if pair.distance() < 1.0:
            pair.harmonize()

        braid.update()
        env.update(braid)
        soft_overlap_compression(A, B)

        print(f"Step {step}")
        print(f"  A pos={A.position} density={A.density:.3f}")
        print(f"  B pos={B.position} density={B.density:.3f}")
        print(f"  distance={pair.distance():.3f}")
        print(f"  crossings={braid.crossings}")
        print(f"  echo={env.echo:.4f}")
        print("")


# ------------------------------------------------------------
# Run the engine
# ------------------------------------------------------------
run_echo13()
