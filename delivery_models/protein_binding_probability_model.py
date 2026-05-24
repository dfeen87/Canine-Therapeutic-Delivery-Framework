"""Protein- and calcium-binding probability model."""

from __future__ import annotations

from typing import Final, Literal, cast

ChargeState = Literal["positive", "neutral", "negative"]

PROTEIN_BINDING_COEFF: Final[float] = 0.02
CALCIUM_BINDING_COEFF: Final[float] = 0.015


def _validate_ph(value: float) -> None:
    if not 0.0 <= value <= 14.0:
        raise ValueError(f"gastric_ph must be between 0 and 14 (got {value}).")


def _validate_non_negative(name: str, value: float) -> None:
    if value < 0:
        raise ValueError(f"{name} must be non-negative (got {value}).")


def _validate_charge_state(api_charge_state: str) -> ChargeState:
    if api_charge_state not in ("positive", "neutral", "negative"):
        raise ValueError(
            "api_charge_state must be 'positive', 'neutral', or 'negative' "
            f"(got {api_charge_state})."
        )
    return cast(ChargeState, api_charge_state)


def calculate_binding_probability(
    gastric_ph: float,
    dietary_protein_g: float,
    calcium_mg: float,
    api_charge_state: ChargeState,
    protective_matrix: bool = False,
) -> str:
    """
    Estimate non-specific binding risk for an orally delivered API.
    """
    _validate_ph(gastric_ph)
    _validate_non_negative("dietary_protein_g", dietary_protein_g)
    _validate_non_negative("calcium_mg", calcium_mg)
    api_charge_state = _validate_charge_state(api_charge_state)

    acidity_factor = max(0.0, (2.5 - gastric_ph)) * 0.1

    if api_charge_state == "positive":
        charge_multiplier = 1.8
    elif api_charge_state == "neutral":
        charge_multiplier = 1.0
    else:
        charge_multiplier = 1.3

    binding_probability = (
        dietary_protein_g * PROTEIN_BINDING_COEFF
        + calcium_mg * CALCIUM_BINDING_COEFF
    ) * charge_multiplier * (1 + acidity_factor)

    if protective_matrix:
        binding_probability *= 0.15
        return (
            f"Binding Risk: {binding_probability:.2f} (Shielded). API Protected."
        )

    return (
        f"Binding Risk: {binding_probability:.2f} (Unshielded). "
        "High Probability of API Loss."
    )


if __name__ == "__main__":
    current_risk = calculate_binding_probability(
        gastric_ph=1.8,
        dietary_protein_g=35,
        calcium_mg=120,
        api_charge_state="positive",
        protective_matrix=False,
    )
    print(current_risk)
