"""Delivery-matrix optimization using a genetic algorithm."""

from __future__ import annotations

import random
from typing import Final, TypedDict


class DeliveryMatrix(TypedDict):
    """Typed representation of a delivery-matrix design."""

    lipid_content: float
    particle_size_nm: float
    bile_salt_affinity: float
    shield_strength: float


LIPID_RANGE: Final[tuple[float, float]] = (0.2, 0.8)
PARTICLE_SIZE_RANGE_NM: Final[tuple[float, float]] = (30.0, 150.0)
BILE_SALT_AFFINITY_RANGE: Final[tuple[float, float]] = (0.5, 1.8)
SHIELD_STRENGTH_RANGE: Final[tuple[float, float]] = (0.4, 1.0)

MUTATION_LIPID_RANGE: Final[tuple[float, float]] = (0.1, 0.9)
MUTATION_PARTICLE_RANGE_NM: Final[tuple[float, float]] = (20.0, 200.0)
MUTATION_BILE_RANGE: Final[tuple[float, float]] = (0.3, 2.0)
MUTATION_SHIELD_RANGE: Final[tuple[float, float]] = (0.2, 1.0)


def _validate_range(name: str, value: float, lower: float, upper: float) -> None:
    if not lower <= value <= upper:
        raise ValueError(f"{name} must be between {lower} and {upper} (got {value}).")


def _validate_rate(rate: float) -> None:
    _validate_range("rate", rate, 0.0, 1.0)


def _validate_positive_int(name: str, value: int) -> None:
    if value < 1:
        raise ValueError(f"{name} must be at least 1 (got {value}).")


def _clamp(value: float, lower: float, upper: float) -> float:
    return max(lower, min(value, upper))


def random_matrix() -> DeliveryMatrix:
    """Generate a random delivery-matrix candidate."""
    return {
        "lipid_content": round(random.uniform(*LIPID_RANGE), 3),
        "particle_size_nm": round(random.uniform(*PARTICLE_SIZE_RANGE_NM), 1),
        "bile_salt_affinity": round(random.uniform(*BILE_SALT_AFFINITY_RANGE), 3),
        "shield_strength": round(random.uniform(*SHIELD_STRENGTH_RANGE), 3),
    }


def evaluate_fitness(matrix: DeliveryMatrix) -> float:
    """
    Score a delivery matrix for routing, protection, stability, and binding risk.
    """
    lipid = matrix["lipid_content"]
    size_nm = matrix["particle_size_nm"]
    bile_aff = matrix["bile_salt_affinity"]
    shield = matrix["shield_strength"]

    _validate_range("lipid_content", lipid, *MUTATION_LIPID_RANGE)
    _validate_range("particle_size_nm", size_nm, *MUTATION_PARTICLE_RANGE_NM)
    _validate_range("bile_salt_affinity", bile_aff, *MUTATION_BILE_RANGE)
    _validate_range("shield_strength", shield, *MUTATION_SHIELD_RANGE)

    lymphatic_score = 0.0
    if lipid >= 0.3 and size_nm >= 50 and bile_aff >= 1.2:
        lymphatic_score = 1.0
    else:
        lymphatic_score = (lipid * 0.6) + (bile_aff * 0.4)

    protection_score = shield
    stability_score = 0.5 + (lipid * 0.3) + (shield * 0.2)

    binding_risk = max(0.1, 1.2 - (shield + lipid))
    binding_score = 1.0 / binding_risk

    return (
        0.3 * lymphatic_score
        + 0.3 * protection_score
        + 0.2 * stability_score
        + 0.2 * binding_score
    )


def mutate(matrix: DeliveryMatrix, rate: float = 0.2) -> DeliveryMatrix:
    """Apply bounded mutations to a delivery-matrix design."""
    _validate_rate(rate)
    new = matrix.copy()

    if random.random() < rate:
        new["lipid_content"] = round(
            _clamp(new["lipid_content"] + random.uniform(-0.1, 0.1), *MUTATION_LIPID_RANGE),
            3,
        )
    if random.random() < rate:
        new["particle_size_nm"] = round(
            _clamp(
                new["particle_size_nm"] + random.uniform(-15, 15),
                *MUTATION_PARTICLE_RANGE_NM,
            ),
            1,
        )
    if random.random() < rate:
        new["bile_salt_affinity"] = round(
            _clamp(
                new["bile_salt_affinity"] + random.uniform(-0.2, 0.2),
                *MUTATION_BILE_RANGE,
            ),
            3,
        )
    if random.random() < rate:
        new["shield_strength"] = round(
            _clamp(
                new["shield_strength"] + random.uniform(-0.1, 0.1),
                *MUTATION_SHIELD_RANGE,
            ),
            3,
        )
    return new


def crossover(parent1: DeliveryMatrix, parent2: DeliveryMatrix) -> DeliveryMatrix:
    """Blend two parent designs into a child matrix."""
    return {
        key: parent1[key] if random.random() < 0.5 else parent2[key]
        for key in parent1.keys()
    }


def optimize_delivery_matrix(
    population_size: int = 20,
    generations: int = 30,
    elite_fraction: float = 0.2,
    log_progress: bool = True,
) -> tuple[float, DeliveryMatrix]:
    """Run the genetic algorithm and return the best scoring matrix."""
    _validate_positive_int("population_size", population_size)
    _validate_positive_int("generations", generations)
    if population_size < 2:
        raise ValueError("population_size must be at least 2 for crossover.")
    if not 0.0 < elite_fraction <= 1.0:
        raise ValueError("elite_fraction must be between 0 and 1.")

    population = [random_matrix() for _ in range(population_size)]

    for gen in range(generations):
        scored = [(evaluate_fitness(m), m) for m in population]
        scored.sort(reverse=True, key=lambda item: item[0])

        elites_count = min(population_size, max(2, int(population_size * elite_fraction)))
        elites = [m for _, m in scored[:elites_count]]

        if log_progress:
            best_fitness, best_matrix = scored[0]
            print(
                f"Generation {gen}: Best Fitness = {best_fitness:.3f}, "
                f"Design = {best_matrix}"
            )

        next_pop = elites.copy()
        while len(next_pop) < population_size:
            parent1, parent2 = random.sample(elites, 2)
            child = crossover(parent1, parent2)
            next_pop.append(mutate(child))

        population = next_pop

    final_scored = [(evaluate_fitness(m), m) for m in population]
    final_scored.sort(reverse=True, key=lambda item: item[0])
    return final_scored[0]


if __name__ == "__main__":
    best = optimize_delivery_matrix()
    print("\nOptimized Delivery Matrix:", best)
