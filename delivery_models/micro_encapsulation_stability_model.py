"""Micro-encapsulation stability model for storage conditions."""

from __future__ import annotations

from typing import Literal, cast

MatrixType = Literal["lipid", "powder"]


def _validate_non_negative(name: str, value: float) -> None:
    if value < 0:
        raise ValueError(f"{name} must be non-negative (got {value}).")


def _validate_percentage(name: str, value: float) -> None:
    if not 0.0 <= value <= 100.0:
        raise ValueError(f"{name} must be between 0 and 100 (got {value}).")


def _validate_fraction(name: str, value: float) -> None:
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must be between 0 and 1 (got {value}).")


def _validate_matrix_type(matrix_type: str) -> MatrixType:
    if matrix_type not in ("lipid", "powder"):
        raise ValueError("matrix_type must be 'lipid' or 'powder'.")
    return cast(MatrixType, matrix_type)


def evaluate_encapsulation_stability(
    temperature_c: float,
    humidity_percent: float,
    mechanical_agitation: float,
    storage_days: float,
    matrix_type: MatrixType = "lipid",
) -> str:
    """Predict encapsulation stability under environmental conditions."""
    _validate_non_negative("temperature_c", temperature_c)
    _validate_percentage("humidity_percent", humidity_percent)
    _validate_fraction("mechanical_agitation", mechanical_agitation)
    _validate_non_negative("storage_days", storage_days)
    matrix_type = _validate_matrix_type(matrix_type)

    stability_score = 100.0

    if temperature_c > 45:
        stability_score -= 25
    elif temperature_c > 30:
        stability_score -= 10

    if humidity_percent > 70:
        stability_score -= 20
    elif humidity_percent > 50:
        stability_score -= 8

    if mechanical_agitation >= 0.8:
        stability_score -= 20
    elif mechanical_agitation >= 0.4:
        stability_score -= 10

    if storage_days > 180:
        stability_score -= 20
    elif storage_days > 90:
        stability_score -= 10

    if matrix_type == "lipid":
        stability_score *= 1.05
    else:
        stability_score *= 0.95

    stability_score = max(0.0, min(stability_score, 100.0))

    if stability_score >= 80:
        return f"Stability: {stability_score:.1f}. Matrix Fully Intact. API Protected."
    if stability_score >= 50:
        return f"Stability: {stability_score:.1f}. Partial Degradation Risk."
    return f"Stability: {stability_score:.1f}. High Degradation Risk. Matrix Compromised."


if __name__ == "__main__":
    current_status = evaluate_encapsulation_stability(
        temperature_c=32,
        humidity_percent=55,
        mechanical_agitation=0.3,
        storage_days=90,
        matrix_type="lipid",
    )
    print(current_status)
