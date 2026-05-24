"""Lymphatic routing model for canine therapeutic absorption."""

from __future__ import annotations

from typing import Final

LIPID_THRESHOLD: Final[float] = 0.3
SIZE_THRESHOLD_NM: Final[float] = 50.0
BILE_SALT_TRIGGER: Final[float] = 1.2
LIPOPHILICITY_TRIGGER: Final[float] = 4.0


def _validate_fraction(name: str, value: float) -> None:
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must be between 0 and 1 (got {value}).")


def _validate_non_negative(name: str, value: float) -> None:
    if value < 0:
        raise ValueError(f"{name} must be non-negative (got {value}).")


def determine_absorption_route(
    lipid_content: float,
    particle_size_nm: float,
    bile_salt_level: float,
    api_lipophilicity: float,
) -> str:
    """
    Determine whether the API enters portal circulation or lymphatic uptake.
    """
    _validate_fraction("lipid_content", lipid_content)
    _validate_non_negative("particle_size_nm", particle_size_nm)
    _validate_non_negative("bile_salt_level", bile_salt_level)
    _validate_non_negative("api_lipophilicity", api_lipophilicity)

    if (
        lipid_content >= LIPID_THRESHOLD
        and particle_size_nm >= SIZE_THRESHOLD_NM
        and bile_salt_level >= BILE_SALT_TRIGGER
        and api_lipophilicity >= LIPOPHILICITY_TRIGGER
    ):
        return "Routing Status: Lymphatic Uptake. First-Pass Metabolism Bypassed."

    return "Routing Status: Portal Absorption. Subject to First-Pass Metabolism."


if __name__ == "__main__":
    current_route = determine_absorption_route(
        lipid_content=0.45,
        particle_size_nm=80,
        bile_salt_level=1.5,
        api_lipophilicity=4.8,
    )
    print(current_route)
