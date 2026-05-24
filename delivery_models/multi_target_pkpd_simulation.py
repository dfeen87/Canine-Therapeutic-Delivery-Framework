"""Multi-target PK/PD simulation for canine longevity therapeutics."""

from __future__ import annotations

import math
from typing import TypedDict


class MultiTargetResponse(TypedDict):
    """Structured PK/PD response output."""

    time_hr: float
    plasma_concentration_mg_L: float
    metabolic_modulation: float
    neuroinflammatory_suppression: float


def _validate_non_negative(name: str, value: float) -> None:
    if value < 0:
        raise ValueError(f"{name} must be non-negative (got {value}).")


def _validate_positive(name: str, value: float) -> None:
    if value <= 0:
        raise ValueError(f"{name} must be positive (got {value}).")


def pk_concentration(
    time_hr: float,
    dose_mg: float,
    volume_distribution_l: float,
    clearance_rate_l_hr: float,
) -> float:
    """One-compartment PK model with first-order elimination."""
    _validate_non_negative("time_hr", time_hr)
    _validate_positive("dose_mg", dose_mg)
    _validate_positive("volume_distribution_l", volume_distribution_l)
    _validate_non_negative("clearance_rate_l_hr", clearance_rate_l_hr)

    k_elim = clearance_rate_l_hr / volume_distribution_l
    return (dose_mg / volume_distribution_l) * math.exp(-k_elim * time_hr)


def pd_effect(concentration: float, ec50: float, hill_coefficient: float = 1.2) -> float:
    """Hill-type PD model for target engagement (fractional effect)."""
    _validate_non_negative("concentration", concentration)
    _validate_positive("ec50", ec50)
    _validate_positive("hill_coefficient", hill_coefficient)

    return (concentration**hill_coefficient) / (
        ec50**hill_coefficient + concentration**hill_coefficient
    )


def simulate_multi_target_response(
    time_hr: float,
    dose_mg: float,
    v_dist_l: float,
    clearance_l_hr: float,
    metabolic_ec50: float,
    neuro_ec50: float,
) -> MultiTargetResponse:
    """Integrate PK with metabolic and neuroinflammatory PD pathways."""
    conc = pk_concentration(time_hr, dose_mg, v_dist_l, clearance_l_hr)

    metabolic_effect = pd_effect(conc, metabolic_ec50)
    neuro_effect = pd_effect(conc, neuro_ec50)

    return {
        "time_hr": time_hr,
        "plasma_concentration_mg_L": round(conc, 4),
        "metabolic_modulation": round(metabolic_effect, 3),
        "neuroinflammatory_suppression": round(neuro_effect, 3),
    }


if __name__ == "__main__":
    results = [
        simulate_multi_target_response(
            time_hr=t,
            dose_mg=27,
            v_dist_l=9.0,
            clearance_l_hr=0.6,
            metabolic_ec50=0.8,
            neuro_ec50=1.2,
        )
        for t in range(0, 13, 2)
    ]

    for result in results:
        print(result)
