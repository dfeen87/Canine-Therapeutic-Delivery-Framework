"""Physiological variability model for senior dogs."""

from __future__ import annotations

from typing import TypedDict


class SeniorDogProfile(TypedDict):
    """Structured physiological profile for a senior dog."""

    age_years: float
    weight_kg: float
    gastric_ph: float
    clearance_factor: float
    inflammation_index: float
    body_fat_fraction: float


def _validate_non_negative(name: str, value: float) -> None:
    if value < 0:
        raise ValueError(f"{name} must be non-negative (got {value}).")


def _validate_positive(name: str, value: float) -> None:
    if value <= 0:
        raise ValueError(f"{name} must be positive (got {value}).")


def get_senior_dog_profile(age_years: float, weight_kg: float) -> SeniorDogProfile:
    """Generate an age-adjusted physiological profile for a senior dog."""
    _validate_non_negative("age_years", age_years)
    _validate_positive("weight_kg", weight_kg)

    baseline_gastric_ph = 1.8
    baseline_clearance_factor = 1.0
    baseline_inflammation_index = 1.0
    baseline_body_fat_fraction = 0.20

    age_factor = max(0.0, age_years - 7)

    gastric_ph = baseline_gastric_ph + 0.05 * age_factor
    clearance_factor = baseline_clearance_factor - 0.04 * age_factor
    inflammation_index = baseline_inflammation_index + 0.15 * age_factor
    body_fat_fraction = baseline_body_fat_fraction + 0.02 * age_factor

    clearance_factor = max(0.4, clearance_factor)

    return {
        "age_years": age_years,
        "weight_kg": weight_kg,
        "gastric_ph": round(gastric_ph, 2),
        "clearance_factor": round(clearance_factor, 2),
        "inflammation_index": round(inflammation_index, 2),
        "body_fat_fraction": round(body_fat_fraction, 2),
    }


def adjust_dosing_for_senior(profile: SeniorDogProfile, base_mg_per_kg: float) -> float:
    """Adjust mg/kg dosing for reduced clearance and elevated inflammation."""
    _validate_positive("base_mg_per_kg", base_mg_per_kg)

    clearance_adj = profile["clearance_factor"]
    inflammation_adj = profile["inflammation_index"]

    scaling = inflammation_adj / clearance_adj
    adjusted_mg_per_kg = base_mg_per_kg * min(scaling, 1.5)

    return round(adjusted_mg_per_kg, 2)


if __name__ == "__main__":
    profile = get_senior_dog_profile(age_years=11, weight_kg=18.0)
    adjusted_dose = adjust_dosing_for_senior(profile, base_mg_per_kg=1.5)

    print("Senior Profile:", profile)
    print("Adjusted mg/kg Dose:", adjusted_dose)
