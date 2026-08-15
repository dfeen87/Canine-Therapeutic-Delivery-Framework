"""Unit tests for PalatabilityRegulationModel and FoodFormulation data structures."""

import pytest
from delivery_models.palatability_regulation_model import (
    Additive,
    CoatingArchitecture,
    FoodFormulation,
    NutrientBase,
    PalatabilityRegulationModel,
    ProcessingParams,
    TextureParams,
    VolatileProfile,
)


def test_additive_validation():
    add = Additive(name="Liver Digest", palatant_type="hydrolyzed_protein", concentration_pct=3.5)
    assert add.concentration_pct == 3.5

    with pytest.raises(ValueError):
        Additive(name="Invalid Concentration", palatant_type="animal_fat", concentration_pct=-1.0)

    with pytest.raises(ValueError):
        Additive(name="Invalid Concentration", palatant_type="animal_fat", concentration_pct=105.0)


def test_processing_params_validation():
    proc = ProcessingParams(extrusion_temp_c=120.0, moisture_pct=10.0, maillard_intensity=6.0)
    assert proc.extrusion_temp_c == 120.0

    with pytest.raises(ValueError):
        ProcessingParams(extrusion_temp_c=-10.0, moisture_pct=10.0)

    with pytest.raises(ValueError):
        ProcessingParams(extrusion_temp_c=120.0, moisture_pct=110.0)

    with pytest.raises(ValueError):
        ProcessingParams(extrusion_temp_c=120.0, moisture_pct=10.0, maillard_intensity=15.0)


def test_additive_profiling():
    model = PalatabilityRegulationModel()
    additives = [
        Additive(name="Chicken Fat", palatant_type="animal_fat", concentration_pct=4.0),
        Additive(name="Yeast Extract", palatant_type="yeast_extract", concentration_pct=2.0),
        Additive(name="Hydrolyzed Liver", palatant_type="hydrolyzed_protein", concentration_pct=3.0),
    ]

    profile = model.profile_additives(additives)
    assert profile["total_palatant_load_pct"] == 9.0
    assert profile["additive_count"] == 3
    assert profile["class_breakdown_pct"]["animal_fat"] == 4.0
    assert profile["class_breakdown_pct"]["yeast_extract"] == 2.0
    assert profile["class_breakdown_pct"]["hydrolyzed_protein"] == 3.0


def test_low_risk_formulation():
    model = PalatabilityRegulationModel()
    formulation = FoodFormulation(
        formulation_id="FORM_LOW_01",
        name="Balanced Senior Maintenance",
        palatants=[
            Additive(name="Chicken Fat", palatant_type="animal_fat", concentration_pct=1.5),
        ],
        processing=ProcessingParams(extrusion_temp_c=105.0, moisture_pct=10.0, maillard_intensity=3.0),
        coating=CoatingArchitecture(coating_type="single_phase", burst_factor=0.1),
        volatile_profile=VolatileProfile(
            volatile_aromatics=15.0,
            sulfur_compounds=5.0,
            amino_acid_derivatives=10.0,
            voc_cluster_intensity=15.0,
        ),
        texture=TextureParams(hardness_n=55.0, friability_pct=4.0, chew_phase_breakdown_sec=10.0),
        nutrient_base=NutrientBase(glycemic_index=40.0),
    )

    result = model.analyze_formulation(formulation)

    assert result["risk_classification"] == "Low"
    assert result["dopamine_risk_score"] <= 30.0
    assert result["cognitive_ease_index"] >= 0.70
    assert result["chew_behavior_score"] >= 80.0
    assert not result["cognitive_comfort_exceeded"]


def test_high_risk_formulation_and_recommendations():
    model = PalatabilityRegulationModel()
    formulation = FoodFormulation(
        formulation_id="FORM_HIGH_01",
        name="Hyper-Palatable Extreme Kibble",
        palatants=[
            Additive(name="Tallow", palatant_type="animal_fat", concentration_pct=8.0),
            Additive(name="Hydrolyzed Liver Digest", palatant_type="hydrolyzed_protein", concentration_pct=5.0),
            Additive(name="Autolyzed Yeast", palatant_type="yeast_extract", concentration_pct=3.0),
        ],
        processing=ProcessingParams(
            extrusion_temp_c=145.0,
            moisture_pct=6.0,
            fat_spray_timing="dual_stage",
            maillard_intensity=9.0,
        ),
        coating=CoatingArchitecture(coating_type="dual_phase", release_delay_sec=5.0, burst_factor=0.8),
        volatile_profile=VolatileProfile(
            volatile_aromatics=85.0,
            sulfur_compounds=70.0,
            amino_acid_derivatives=80.0,
            voc_cluster_intensity=90.0,
        ),
        texture=TextureParams(hardness_n=20.0, friability_pct=15.0, chew_phase_breakdown_sec=2.0),
        nutrient_base=NutrientBase(glycemic_index=85.0),
    )

    result = model.analyze_formulation(formulation)

    assert result["risk_classification"] == "High"
    assert result["dopamine_risk_score"] > 65.0
    assert result["cognitive_comfort_exceeded"] is True
    assert result["cognitive_ease_index"] < 0.50
    assert len(result["recommendations"]) >= 3
    assert any("Reduce overall palatant load" in rec for rec in result["recommendations"])
    assert any("exceeds canine cognitive-comfort threshold" in rec for rec in result["recommendations"])
    assert any("Dual-phase release" in rec for rec in result["recommendations"])


def test_boundary_and_edge_cases():
    model = PalatabilityRegulationModel()
    empty_formulation = FoodFormulation(
        formulation_id="FORM_EMPTY_01",
        name="Bland Minimalist Formula",
        palatants=[],
        processing=ProcessingParams(extrusion_temp_c=100.0, moisture_pct=10.0, maillard_intensity=0.0),
        coating=CoatingArchitecture(coating_type="single_phase", burst_factor=0.0),
        volatile_profile=VolatileProfile(
            volatile_aromatics=0.0,
            sulfur_compounds=0.0,
            amino_acid_derivatives=0.0,
            voc_cluster_intensity=0.0,
        ),
    )

    result = model.analyze_formulation(empty_formulation)

    assert result["additive_profile"]["total_palatant_load_pct"] == 0.0
    assert result["dopamine_risk_score"] < 10.0
    assert result["risk_classification"] == "Low"
