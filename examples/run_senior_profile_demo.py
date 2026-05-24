"""Minimal demo for the senior-dog physiological variability model."""

from __future__ import annotations

import os
import sys

# Allow running this script directly from the examples/ folder.
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from delivery_models.physiological_variability_model import (
    adjust_dosing_for_senior,
    get_senior_dog_profile,
)


def main() -> None:
    """Generate a profile and show the adjusted mg/kg dose."""
    profile = get_senior_dog_profile(age_years=11.0, weight_kg=18.0)
    adjusted_mg_per_kg = adjust_dosing_for_senior(profile, base_mg_per_kg=1.5)

    print("Senior profile:", profile)
    print("Adjusted mg/kg dose:", adjusted_mg_per_kg)


if __name__ == "__main__":
    main()
