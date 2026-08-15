"""Demonstration script for Canine Food Additive & Palatability Regulation Analysis."""

from __future__ import annotations

import json
import sys
from pathlib import Path

# Ensure root directory is on path
sys.path.insert(0, str(Path(__file__).parent.parent))

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


def run_demo() -> None:
    print("=" * 80)
    print("CANINE PALATABILITY & DOPAMINE REGULATION ANALYSIS DEMO")
    print("=" * 80)

    # 1. Construct a sample formulation with high palatant & dual-phase coating load
    formulation_high_risk = FoodFormulation(
        formulation_id="FORM_PREMIUM_BEEF_01",
        name="Ultra-Palatable Gourmet Beef Kibble",
        palatants=[
            Additive(
                name="Tallow Fat Spray",
                palatant_type="animal_fat",
                concentration_pct=6.5,
                source="beef",
            ),
            Additive(
                name="Hydrolyzed Beef Liver Digest",
                palatant_type="hydrolyzed_protein",
                concentration_pct=4.0,
                source="bovine",
            ),
            Additive(
                name="Autolyzed Yeast Extract",
                palatant_type="yeast_extract",
                concentration_pct=2.5,
                source="yeast",
            ),
            Additive(
                name="Maillard Reaction Flavor Booster",
                palatant_type="maillard_compound",
                concentration_pct=1.5,
                source="reaction_flavor",
            ),
        ],
        processing=ProcessingParams(
            extrusion_temp_c=138.0,
            moisture_pct=8.5,
            fat_spray_timing="dual_stage",
            maillard_intensity=8.5,
        ),
        coating=CoatingArchitecture(
            coating_type="dual_phase",
            release_delay_sec=3.0,
            burst_factor=0.75,
        ),
        volatile_profile=VolatileProfile(
            volatile_aromatics=80.0,
            sulfur_compounds=65.0,
            amino_acid_derivatives=70.0,
            voc_cluster_intensity=85.0,
        ),
        texture=TextureParams(
            hardness_n=35.0,
            friability_pct=10.0,
            chew_phase_breakdown_sec=4.0,
        ),
        nutrient_base=NutrientBase(
            carb_type="white_potato",
            glycemic_index=75.0,
            protein_source="dehydrated_beef",
            fat_type="beef_tallow",
        ),
    )

    # 2. Construct a balanced formulation
    formulation_balanced = FoodFormulation(
        formulation_id="FORM_BALANCED_LONGEVITY_02",
        name="Longevity-Calm Therapeutic Formula",
        palatants=[
            Additive(
                name="Chicken Fat",
                palatant_type="animal_fat",
                concentration_pct=2.0,
                source="chicken",
            ),
            Additive(
                name="Enzymatic Plant Hydrolysate",
                palatant_type="plant_hydrolysate",
                concentration_pct=1.5,
                source="pea_protein",
            ),
        ],
        processing=ProcessingParams(
            extrusion_temp_c=108.0,
            moisture_pct=10.0,
            fat_spray_timing="post_extrusion_coat",
            maillard_intensity=3.5,
        ),
        coating=CoatingArchitecture(
            coating_type="single_phase",
            release_delay_sec=0.0,
            burst_factor=0.20,
        ),
        volatile_profile=VolatileProfile(
            volatile_aromatics=25.0,
            sulfur_compounds=12.0,
            amino_acid_derivatives=20.0,
            voc_cluster_intensity=22.0,
        ),
        texture=TextureParams(
            hardness_n=52.0,
            friability_pct=4.5,
            chew_phase_breakdown_sec=11.0,
        ),
        nutrient_base=NutrientBase(
            carb_type="sweet_potato",
            glycemic_index=45.0,
            protein_source="fresh_salmon",
            fat_type="salmon_oil",
        ),
    )

    model = PalatabilityRegulationModel()

    for formulation in [formulation_high_risk, formulation_balanced]:
        print(f"\nAnalyzing Formulation: {formulation.name} (ID: {formulation.formulation_id})")
        print("-" * 70)
        result = model.analyze_formulation(formulation)

        print(f"Total Palatant Load:           {result['additive_profile']['total_palatant_load_pct']}%")
        print(f"Dopamine Risk Score:           {result['dopamine_risk_score']} / 100 ({result['risk_classification']} Risk)")
        print(f"Cognitive Ease Index:          {result['cognitive_ease_index']} (Range: 0.00 - 1.00)")
        print(f"Chew Behavior Compatibility:   {result['chew_behavior_score']} / 100")
        print(f"Cognitive Comfort Exceeded:    {result['cognitive_comfort_exceeded']}")
        print(f"Compulsive Intake Risk:        {result['compulsive_intake_risk']} / 100")
        print("\nFormulation Recommendations:")
        for idx, rec in enumerate(result["recommendations"], 1):
            print(f"  {idx}. {rec}")
        print("\nFull Analysis JSON Output:")
        print(json.dumps(result, indent=2))
        print("=" * 80)


if __name__ == "__main__":
    run_demo()
