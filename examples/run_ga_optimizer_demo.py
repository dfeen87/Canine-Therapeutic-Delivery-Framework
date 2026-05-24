"""Minimal demo for the delivery-matrix genetic algorithm optimizer."""

from __future__ import annotations

import os
import random
import sys

# Allow running this script directly from the examples/ folder.
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from delivery_models.delivery_matrix_optimization import optimize_delivery_matrix


def main() -> None:
    """Run a short optimization and print the best design."""
    random.seed(7)
    best_fitness, best_matrix = optimize_delivery_matrix(
        population_size=8,
        generations=5,
        elite_fraction=0.25,
        log_progress=False,
    )

    print(f"Best fitness: {best_fitness:.3f}")
    print("Best delivery matrix:", best_matrix)


if __name__ == "__main__":
    main()
