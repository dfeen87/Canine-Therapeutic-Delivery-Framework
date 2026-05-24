"""Weight-class dosing engine for canine therapeutics."""

from __future__ import annotations

from typing import TypedDict


class DosingSchedule(TypedDict):
    """Structured dosing schedule output."""

    dog_weight_kg: float
    total_daily_dose_mg: float
    total_daily_volume_ml: float
    dose_per_feeding_mg: float
    volume_per_feeding_ml: float
    volume_per_actuation_ml: float
    acts_per_feeding: int


def _validate_positive(name: str, value: float) -> None:
    if value <= 0:
        raise ValueError(f"{name} must be positive (got {value}).")


def _validate_positive_int(name: str, value: int) -> None:
    if value <= 0:
        raise ValueError(f"{name} must be a positive integer (got {value}).")


def calculate_dose_mg(dog_weight_kg: float, target_mg_per_kg: float) -> float:
    """Calculate total dose in mg based on weight and target mg/kg."""
    _validate_positive("dog_weight_kg", dog_weight_kg)
    _validate_positive("target_mg_per_kg", target_mg_per_kg)
    return dog_weight_kg * target_mg_per_kg


def calculate_volume_per_actuation_ml(
    total_dose_mg: float,
    api_concentration_mg_per_ml: float,
    max_acts_per_feeding: int,
) -> tuple[float, float]:
    """Convert total dose into volume and per-actuation delivery."""
    _validate_positive("total_dose_mg", total_dose_mg)
    _validate_positive("api_concentration_mg_per_ml", api_concentration_mg_per_ml)
    _validate_positive_int("max_acts_per_feeding", max_acts_per_feeding)

    total_volume_ml = total_dose_mg / api_concentration_mg_per_ml
    volume_per_actuation = total_volume_ml / max_acts_per_feeding
    return total_volume_ml, volume_per_actuation


def generate_dosing_schedule(
    dog_weight_kg: float,
    target_mg_per_kg: float,
    api_concentration_mg_per_ml: float,
    feedings_per_day: int = 2,
    max_acts_per_feeding: int = 3,
) -> DosingSchedule:
    """Generate a structured dosing schedule for a given dog weight."""
    _validate_positive_int("feedings_per_day", feedings_per_day)
    _validate_positive_int("max_acts_per_feeding", max_acts_per_feeding)

    total_dose_mg = calculate_dose_mg(dog_weight_kg, target_mg_per_kg)
    total_volume_ml, volume_per_actuation = calculate_volume_per_actuation_ml(
        total_dose_mg,
        api_concentration_mg_per_ml,
        max_acts_per_feeding,
    )

    dose_per_feeding_mg = total_dose_mg / feedings_per_day
    volume_per_feeding_ml = total_volume_ml / feedings_per_day

    return {
        "dog_weight_kg": dog_weight_kg,
        "total_daily_dose_mg": round(total_dose_mg, 2),
        "total_daily_volume_ml": round(total_volume_ml, 2),
        "dose_per_feeding_mg": round(dose_per_feeding_mg, 2),
        "volume_per_feeding_ml": round(volume_per_feeding_ml, 2),
        "volume_per_actuation_ml": round(volume_per_actuation, 3),
        "acts_per_feeding": max_acts_per_feeding,
    }


if __name__ == "__main__":
    schedule = generate_dosing_schedule(
        dog_weight_kg=18.0,
        target_mg_per_kg=1.5,
        api_concentration_mg_per_ml=10.0,
        feedings_per_day=2,
        max_acts_per_feeding=3,
    )

    print("Dosing Schedule:", schedule)
