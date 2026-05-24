"""Thermal degradation model for extrusion-like manufacturing stress."""

from __future__ import annotations

from typing import Final

DENATURATION_TEMP_C: Final[float] = 55.0
COLLAPSE_TEMP_C: Final[float] = 90.0
ANNIHILATION_TEMP_C: Final[float] = 130.0
SHEAR_THRESHOLD: Final[float] = 0.7


def _validate_non_negative(name: str, value: float) -> None:
    if value < 0:
        raise ValueError(f"{name} must be non-negative (got {value}).")


def simulate_thermal_degradation(
    temperature_c: float,
    shear_force: float,
    exposure_time: float,
) -> str:
    """
    Model degradation of a longevity API under thermal and mechanical stress.

    Exposure time is validated for scientific completeness but not yet applied
    in this simplified thermal logic.
    """
    _validate_non_negative("temperature_c", temperature_c)
    _validate_non_negative("shear_force", shear_force)
    _validate_non_negative("exposure_time", exposure_time)

    integrity = 100.0

    if temperature_c >= ANNIHILATION_TEMP_C:
        integrity -= 95
        return "Status: Thermal Annihilation. API Destroyed (<5% Integrity)."

    if temperature_c >= COLLAPSE_TEMP_C:
        integrity -= 70
        if shear_force >= SHEAR_THRESHOLD:
            integrity -= 20
        return f"Status: Structural Collapse. Approx. {integrity}% Integrity Remaining."

    if temperature_c >= DENATURATION_TEMP_C:
        integrity -= 40
        if shear_force >= SHEAR_THRESHOLD:
            integrity -= 10
        return f"Status: Partial Denaturation. Approx. {integrity}% Integrity Remaining."

    return "Status: Thermally Stable. API Integrity Preserved."


if __name__ == "__main__":
    current_status = simulate_thermal_degradation(
        temperature_c=150,
        shear_force=0.8,
        exposure_time=45,
    )
    print(current_status)
