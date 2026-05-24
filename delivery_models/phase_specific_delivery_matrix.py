"""Phase-specific delivery matrix model for GI transit."""

from __future__ import annotations

from typing import Final

GASTRIC_PH_THRESHOLD: Final[float] = 2.0
DUODENAL_PH_TRIGGER: Final[float] = 6.5


def _validate_ph(value: float) -> None:
    if not 0.0 <= value <= 14.0:
        raise ValueError(f"environment_ph must be between 0 and 14 (got {value}).")


def _validate_non_negative(name: str, value: float) -> None:
    if value < 0:
        raise ValueError(f"{name} must be non-negative (got {value}).")


def calculate_peptide_stability(
    environment_ph: float,
    pepsin_concentration: float,
    transit_time: float,
) -> str:
    """
    Simulate peptide shield integrity across gastric and duodenal phases.

    Transit time is validated for scientific completeness but not used in the
    simplified gating logic.
    """
    _validate_ph(environment_ph)
    _validate_non_negative("pepsin_concentration", pepsin_concentration)
    _validate_non_negative("transit_time", transit_time)

    if environment_ph <= GASTRIC_PH_THRESHOLD and pepsin_concentration > 0:
        return "Transit Status: Gastric Phase. Shield Intact. API Protected."

    if environment_ph >= DUODENAL_PH_TRIGGER:
        return "Transit Status: Duodenal Phase. Shield Uncoiled. API Released for Absorption."

    return "Transit Status: Intermediate Phase. Matrix Stabilized."


if __name__ == "__main__":
    current_status = calculate_peptide_stability(
        environment_ph=6.8,
        pepsin_concentration=0.1,
        transit_time=120,
    )
    print(current_status)
