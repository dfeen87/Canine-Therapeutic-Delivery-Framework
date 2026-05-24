"""End-to-end delivery pipeline simulation for canine therapeutics."""

from __future__ import annotations

from typing import Final

GASTRIC_PH_THRESHOLD: Final[float] = 2.0
DUODENAL_PH_TRIGGER: Final[float] = 6.5

LYMPHATIC_LIPID_THRESHOLD: Final[float] = 0.3
LYMPHATIC_SIZE_THRESHOLD_NM: Final[float] = 50.0
LYMPHATIC_BILE_SALT_THRESHOLD: Final[float] = 1.2
LYMPHATIC_LIPOPHILICITY_THRESHOLD: Final[float] = 4.0

THERMAL_DENATURATION_TEMP_C: Final[float] = 55.0
THERMAL_COLLAPSE_TEMP_C: Final[float] = 90.0
THERMAL_ANNIHILATION_TEMP_C: Final[float] = 130.0


def _validate_ph(name: str, value: float) -> None:
    if not 0.0 <= value <= 14.0:
        raise ValueError(f"{name} must be between 0 and 14 (got {value}).")


def _validate_non_negative(name: str, value: float) -> None:
    if value < 0:
        raise ValueError(f"{name} must be non-negative (got {value}).")


def _validate_fraction(name: str, value: float) -> None:
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must be between 0 and 1 (got {value}).")


def gastric_phase(
    environment_ph: float,
    pepsin_concentration: float,
    protective_matrix: bool,
) -> str:
    """Simulate gastric survival using Appendix A + D logic."""
    _validate_ph("environment_ph", environment_ph)
    _validate_non_negative("pepsin_concentration", pepsin_concentration)

    if environment_ph <= GASTRIC_PH_THRESHOLD and pepsin_concentration > 0:
        if protective_matrix:
            return "Gastric Phase: Shield Intact. API Protected."
        return "Gastric Phase: API Degraded or Protein-Bound."
    return "Gastric Phase: Transitional State."


def duodenal_phase(environment_ph: float) -> str:
    """Simulate duodenal gating using Appendix A logic."""
    _validate_ph("environment_ph", environment_ph)
    if environment_ph >= DUODENAL_PH_TRIGGER:
        return "Duodenal Phase: Shield Uncoiled. API Released."
    return "Duodenal Phase: Not Yet Released."


def lymphatic_routing(
    lipid_content: float,
    particle_size_nm: float,
    bile_salt_level: float,
    api_lipophilicity: float,
) -> str:
    """Simulate lymphatic vs. portal routing using Appendix B logic."""
    _validate_fraction("lipid_content", lipid_content)
    _validate_non_negative("particle_size_nm", particle_size_nm)
    _validate_non_negative("bile_salt_level", bile_salt_level)
    _validate_non_negative("api_lipophilicity", api_lipophilicity)

    if (
        lipid_content >= LYMPHATIC_LIPID_THRESHOLD
        and particle_size_nm >= LYMPHATIC_SIZE_THRESHOLD_NM
        and bile_salt_level >= LYMPHATIC_BILE_SALT_THRESHOLD
        and api_lipophilicity >= LYMPHATIC_LIPOPHILICITY_THRESHOLD
    ):
        return "Routing: Lymphatic Uptake. First-Pass Metabolism Bypassed."
    return "Routing: Portal Circulation. Subject to First-Pass Metabolism."


def thermal_integrity(temperature_c: float, shear_force: float) -> str:
    """Simulate extrusion-induced degradation using Appendix C logic."""
    _validate_non_negative("temperature_c", temperature_c)
    _validate_non_negative("shear_force", shear_force)

    if temperature_c >= THERMAL_ANNIHILATION_TEMP_C:
        return "Thermal Status: API Destroyed."
    if temperature_c >= THERMAL_COLLAPSE_TEMP_C:
        return "Thermal Status: Severe Structural Collapse."
    if temperature_c >= THERMAL_DENATURATION_TEMP_C:
        return "Thermal Status: Partial Denaturation."
    return "Thermal Status: Stable."


def full_delivery_pipeline() -> str:
    """Integrate all delivery stages into a single simulation."""
    manufacturing = thermal_integrity(temperature_c=25, shear_force=0.1)

    gastric = gastric_phase(
        environment_ph=1.8,
        pepsin_concentration=0.9,
        protective_matrix=True,
    )

    duodenum = duodenal_phase(environment_ph=6.8)

    routing = lymphatic_routing(
        lipid_content=0.45,
        particle_size_nm=80,
        bile_salt_level=1.5,
        api_lipophilicity=4.8,
    )

    return f"{manufacturing}\n{gastric}\n{duodenum}\n{routing}"


if __name__ == "__main__":
    print(full_delivery_pipeline())
