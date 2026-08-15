"""Scientific Analysis Module: Canine Food Additive & Palatability Regulation.

Provides chemosensoric profiling, dopamine-linked palatability risk modeling,
cognitive ease index computation, chew-behavior compatibility scoring,
and formulation balancing recommendations for canine nutrition.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Final, Literal, TypedDict


# Validation constants and thresholds
DOPAMINE_RISK_LOW_MAX: Final[float] = 30.0
DOPAMINE_RISK_MODERATE_MAX: Final[float] = 65.0
COGNITIVE_COMFORT_AROMA_THRESHOLD: Final[float] = 75.0  # Max comfortable aroma intensity score
MIN_COGNITIVE_EASE_THRESHOLD: Final[float] = 0.50

VALID_PALATANT_TYPES: Final[set[str]] = {
    "animal_fat",
    "hydrolyzed_protein",
    "yeast_extract",
    "maillard_compound",
    "plant_hydrolysate",
    "insect_hydrolysate",
    "synthetic_aromatic",
}


def _validate_range(name: str, value: float, lower: float, upper: float) -> None:
    if not lower <= value <= upper:
        raise ValueError(f"{name} must be between {lower} and {upper} (got {value}).")


def _validate_non_negative(name: str, value: float) -> None:
    if value < 0.0:
        raise ValueError(f"{name} must be non-negative (got {value}).")


def _clamp(value: float, lower: float, upper: float) -> float:
    return max(lower, min(value, upper))


@dataclass
class Additive:
    """Represents a chemical additive or palatant in the food formulation."""

    name: str
    palatant_type: str  # Must be one of VALID_PALATANT_TYPES or similar
    concentration_pct: float  # Percentage by weight (0.0 - 100.0)
    source: str = "synthetic"

    def __post_init__(self) -> None:
        _validate_range("concentration_pct", self.concentration_pct, 0.0, 100.0)


@dataclass
class ProcessingParams:
    """Thermal and mechanical processing parameters during kibble/food production."""

    extrusion_temp_c: float  # Processing temperature in Celsius
    moisture_pct: float  # Moisture content percentage (0.0 - 100.0)
    fat_spray_timing: Literal["pre_extrusion", "post_extrusion_coat", "dual_stage"] = "post_extrusion_coat"
    maillard_intensity: float = 5.0  # 0.0 (none) to 10.0 (extreme)

    def __post_init__(self) -> None:
        _validate_non_negative("extrusion_temp_c", self.extrusion_temp_c)
        _validate_range("moisture_pct", self.moisture_pct, 0.0, 100.0)
        _validate_range("maillard_intensity", self.maillard_intensity, 0.0, 10.0)


@dataclass
class CoatingArchitecture:
    """Coating kinetics and phase release properties."""

    coating_type: Literal["single_phase", "dual_phase"] = "single_phase"
    release_delay_sec: float = 0.0  # Delay before secondary aroma release
    burst_factor: float = 0.2  # Immediate aromatic burst ratio (0.0 - 1.0)

    def __post_init__(self) -> None:
        _validate_non_negative("release_delay_sec", self.release_delay_sec)
        _validate_range("burst_factor", self.burst_factor, 0.0, 1.0)


@dataclass
class VolatileProfile:
    """GC-MS/O aligned volatile aromatic compound intensity clusters (0.0 - 100.0)."""

    volatile_aromatics: float = 20.0
    sulfur_compounds: float = 10.0
    amino_acid_derivatives: float = 15.0
    voc_cluster_intensity: float = 25.0

    def __post_init__(self) -> None:
        _validate_range("volatile_aromatics", self.volatile_aromatics, 0.0, 100.0)
        _validate_range("sulfur_compounds", self.sulfur_compounds, 0.0, 100.0)
        _validate_range("amino_acid_derivatives", self.amino_acid_derivatives, 0.0, 100.0)
        _validate_range("voc_cluster_intensity", self.voc_cluster_intensity, 0.0, 100.0)


@dataclass
class TextureParams:
    """Physical kibble texture and chew kinetics."""

    hardness_n: float = 50.0  # Force required to fracture in Newtons
    friability_pct: float = 5.0  # Percentage friability (0 - 100)
    chew_phase_breakdown_sec: float = 8.0  # Time required for mastication before swallow

    def __post_init__(self) -> None:
        _validate_non_negative("hardness_n", self.hardness_n)
        _validate_range("friability_pct", self.friability_pct, 0.0, 100.0)
        _validate_non_negative("chew_phase_breakdown_sec", self.chew_phase_breakdown_sec)


@dataclass
class NutrientBase:
    """Macronutrient base profile."""

    carb_type: str = "sweet_potato"
    glycemic_index: float = 50.0  # 0 to 100 scale
    protein_source: str = "dehydrated_chicken"
    fat_type: str = "chicken_fat"

    def __post_init__(self) -> None:
        _validate_range("glycemic_index", self.glycemic_index, 0.0, 100.0)


@dataclass
class FoodFormulation:
    """Complete canine food formulation specification."""

    formulation_id: str
    name: str
    palatants: list[Additive] = field(default_factory=list)
    processing: ProcessingParams = field(default_factory=ProcessingParams)
    coating: CoatingArchitecture = field(default_factory=CoatingArchitecture)
    volatile_profile: VolatileProfile = field(default_factory=VolatileProfile)
    texture: TextureParams = field(default_factory=TextureParams)
    nutrient_base: NutrientBase = field(default_factory=NutrientBase)


class PalatabilityAnalysisResult(TypedDict):
    """Structured result dictionary for formulation palatability analysis."""

    formulation_id: str
    formulation_name: str
    additive_profile: dict[str, Any]
    dopamine_risk_score: float
    risk_classification: Literal["Low", "Moderate", "High"]
    cognitive_ease_index: float
    chew_behavior_score: float
    cognitive_comfort_exceeded: bool
    compulsive_intake_risk: float
    recommendations: list[str]


class PalatabilityRegulationModel:
    """
    Scientific analysis engine for canine food additive, palatability,
    dopamine-linked reward dynamics, and cognitive ease evaluation.
    """

    @staticmethod
    def profile_additives(palatants: list[Additive]) -> dict[str, Any]:
        """Quantify and classify palatants present in the formulation."""
        class_breakdown: dict[str, float] = {}
        total_palatant_load = 0.0

        for add in palatants:
            p_type = add.palatant_type.lower()
            class_breakdown[p_type] = class_breakdown.get(p_type, 0.0) + add.concentration_pct
            total_palatant_load += add.concentration_pct

        return {
            "total_palatant_load_pct": round(total_palatant_load, 3),
            "additive_count": len(palatants),
            "class_breakdown_pct": {k: round(v, 3) for k, v in class_breakdown.items()},
        }

    @staticmethod
    def compute_aromatic_release_intensity(
        volatile_profile: VolatileProfile,
        coating: CoatingArchitecture,
        processing: ProcessingParams,
    ) -> float:
        """
        Compute total perceived aromatic intensity factoring GC-MS/O VOCs,
        burst kinetics, and fat spray timing.
        """
        raw_voc_sum = (
            volatile_profile.volatile_aromatics * 0.35
            + volatile_profile.sulfur_compounds * 0.25
            + volatile_profile.amino_acid_derivatives * 0.20
            + volatile_profile.voc_cluster_intensity * 0.20
        )

        # Dual-phase release creates initial spike + secondary surge
        coating_multiplier = 1.35 if coating.coating_type == "dual_phase" else 1.00
        burst_impact = 1.00 + (coating.burst_factor * 0.30)

        # Post-extrusion fat spray releases volatile aromatics much faster than pre-extrusion mixing
        spray_multiplier = (
            1.25 if processing.fat_spray_timing == "post_extrusion_coat"
            else (1.30 if processing.fat_spray_timing == "dual_stage" else 1.00)
        )

        aromatic_intensity = raw_voc_sum * coating_multiplier * burst_impact * spray_multiplier
        return round(_clamp(aromatic_intensity, 0.0, 100.0), 2)

    @staticmethod
    def compute_dopamine_risk_score(
        palatant_profile: dict[str, Any],
        aromatic_intensity: float,
        coating: CoatingArchitecture,
        processing: ProcessingParams,
    ) -> float:
        """
        Compute Dopamine-Palatability Risk Score (0 - 100).
        Evaluates risk of over-stimulation of dopamine reward pathways and compulsive eating.
        """
        total_load = palatant_profile["total_palatant_load_pct"]
        # Standard kibble baseline palatant load threshold ~ 5%
        load_factor = _clamp(total_load / 8.0, 0.0, 1.0) * 35.0

        aroma_factor = (aromatic_intensity / 100.0) * 30.0

        maillard_factor = (processing.maillard_intensity / 10.0) * 15.0

        phase_factor = 20.0 if coating.coating_type == "dual_phase" else 5.0
        if coating.burst_factor > 0.5:
            phase_factor += 5.0

        dopamine_score = load_factor + aroma_factor + maillard_factor + phase_factor
        return round(_clamp(dopamine_score, 0.0, 100.0), 2)

    @staticmethod
    def compute_cognitive_ease_index(
        aromatic_intensity: float,
        texture: TextureParams,
        nutrient_base: NutrientBase,
        processing: ProcessingParams,
    ) -> float:
        """
        Compute Cognitive Ease Index (0.00 - 1.00).
        Models whether the food promotes calm, non-compulsive eating behavior versus hyper-arousal.
        """
        # Excessive volatile intensity reduces cognitive ease
        aroma_penalty = max(0.0, (aromatic_intensity - 40.0) / 60.0) * 0.35

        # Rapid chew phase or extremely soft/friable kibble promotes bolting food
        chew_time_benefit = _clamp(texture.chew_phase_breakdown_sec / 15.0, 0.0, 1.0) * 0.25

        # High glycemic index causes rapid glucose/dopamine spike
        glycemic_penalty = (nutrient_base.glycemic_index / 100.0) * 0.20

        # Excessive Maillard intensity increases arousal
        maillard_penalty = (processing.maillard_intensity / 10.0) * 0.20

        base_ease = 0.90 - aroma_penalty - glycemic_penalty - maillard_penalty + chew_time_benefit
        return round(_clamp(base_ease, 0.0, 1.0), 3)

    @staticmethod
    def compute_chew_behavior_score(
        texture: TextureParams,
        processing: ProcessingParams,
        aromatic_intensity: float,
    ) -> float:
        """
        Compute Chew-Behavior Compatibility Score (0 - 100).
        Evaluates physical kibble texture and chew kinetics for optimal dental/oral engagement.
        """
        # Hardness optimal range ~ 40-70 N
        if 40.0 <= texture.hardness_n <= 70.0:
            hardness_score = 35.0
        else:
            diff = min(abs(texture.hardness_n - 40.0), abs(texture.hardness_n - 70.0))
            hardness_score = max(0.0, 35.0 - (diff * 0.5))

        # Friability: ideally low to moderate (2% - 8%)
        if 2.0 <= texture.friability_pct <= 8.0:
            friability_score = 25.0
        else:
            friability_score = max(0.0, 25.0 - abs(texture.friability_pct - 5.0) * 2.0)

        # Moisture: ideal kibble moisture ~ 8% - 12%
        if 8.0 <= processing.moisture_pct <= 12.0:
            moisture_score = 20.0
        else:
            moisture_score = max(0.0, 20.0 - abs(processing.moisture_pct - 10.0) * 1.5)

        # Chew phase duration score (ideal > 6 seconds)
        chew_score = _clamp(texture.chew_phase_breakdown_sec / 10.0, 0.0, 1.0) * 20.0

        total_chew_score = hardness_score + friability_score + moisture_score + chew_score
        return round(_clamp(total_chew_score, 0.0, 100.0), 2)

    def analyze_formulation(self, formulation: FoodFormulation) -> PalatabilityAnalysisResult:
        """
        Main entry point: Analyzes a complete FoodFormulation and generates
        palatability risks, cognitive ease, chew score, and balancing recommendations.
        """
        additive_profile = self.profile_additives(formulation.palatants)

        aromatic_intensity = self.compute_aromatic_release_intensity(
            formulation.volatile_profile,
            formulation.coating,
            formulation.processing,
        )

        dopamine_risk_score = self.compute_dopamine_risk_score(
            additive_profile,
            aromatic_intensity,
            formulation.coating,
            formulation.processing,
        )

        if dopamine_risk_score <= DOPAMINE_RISK_LOW_MAX:
            risk_classification: Literal["Low", "Moderate", "High"] = "Low"
        elif dopamine_risk_score <= DOPAMINE_RISK_MODERATE_MAX:
            risk_classification = "Moderate"
        else:
            risk_classification = "High"

        cognitive_ease_index = self.compute_cognitive_ease_index(
            aromatic_intensity,
            formulation.texture,
            formulation.nutrient_base,
            formulation.processing,
        )

        chew_behavior_score = self.compute_chew_behavior_score(
            formulation.texture,
            formulation.processing,
            aromatic_intensity,
        )

        cognitive_comfort_exceeded = aromatic_intensity > COGNITIVE_COMFORT_AROMA_THRESHOLD
        compulsive_intake_risk = round(_clamp((dopamine_risk_score * 0.7) + ((1.0 - cognitive_ease_index) * 30.0), 0.0, 100.0), 2)

        # Recommendation Engine
        recommendations: list[str] = []

        if dopamine_risk_score > DOPAMINE_RISK_MODERATE_MAX:
            recommendations.append(
                f"High Dopamine Risk Score ({dopamine_risk_score}/100): Reduce overall palatant load "
                f"(currently {additive_profile['total_palatant_load_pct']}%) by at least 20-30%."
            )

        if cognitive_comfort_exceeded:
            recommendations.append(
                f"Aromatic release intensity ({aromatic_intensity}) exceeds canine cognitive-comfort threshold ({COGNITIVE_COMFORT_AROMA_THRESHOLD}). "
                "Attenuate high-intensity VOC clusters or sulfur compounds."
            )

        if formulation.coating.coating_type == "dual_phase" and dopamine_risk_score > DOPAMINE_RISK_LOW_MAX:
            recommendations.append(
                "Dual-phase release creates an intense aromatic burst. Consider switching to a single-phase "
                "controlled release architecture to promote calm intake."
            )

        if formulation.processing.maillard_intensity > 6.0:
            recommendations.append(
                f"Elevated Maillard intensity ({formulation.processing.maillard_intensity}/10.0): Lower thermal extrusion "
                f"temperature (currently {formulation.processing.extrusion_temp_c}°C) or adjust reducing sugar content."
            )

        if formulation.processing.fat_spray_timing == "dual_stage" and aromatic_intensity > 60.0:
            recommendations.append(
                "Dual-stage fat spraying amplifies volatile flash-off. Transition to single post-extrusion or pre-extrusion fat mixing."
            )

        if cognitive_ease_index < MIN_COGNITIVE_EASE_THRESHOLD:
            recommendations.append(
                f"Cognitive Ease Index ({cognitive_ease_index}) is below safe target ({MIN_COGNITIVE_EASE_THRESHOLD}). "
                "Increase kibble chew phase duration or lower glycemic index carbohydrates."
            )

        if formulation.texture.chew_phase_breakdown_sec < 5.0:
            recommendations.append(
                f"Short chew breakdown time ({formulation.texture.chew_phase_breakdown_sec}s): Increase kibble size/hardness "
                "to encourage thorough mastication and prevent binge eating."
            )

        if not recommendations:
            recommendations.append("Formulation is well-balanced within safe palatability and cognitive ease parameters.")

        return {
            "formulation_id": formulation.formulation_id,
            "formulation_name": formulation.name,
            "additive_profile": additive_profile,
            "dopamine_risk_score": dopamine_risk_score,
            "risk_classification": risk_classification,
            "cognitive_ease_index": cognitive_ease_index,
            "chew_behavior_score": chew_behavior_score,
            "cognitive_comfort_exceeded": cognitive_comfort_exceeded,
            "compulsive_intake_risk": compulsive_intake_risk,
            "recommendations": recommendations,
        }
