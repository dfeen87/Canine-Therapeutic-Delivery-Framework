# Project: Senior-Dog Physiological Variability Model (Canine Longevity)
# License: MIT
# Architect: Don Michael Feeney Jr.

def get_senior_dog_profile(age_years, weight_kg):
    """
    Generates an age-adjusted physiological profile for a senior dog.
    """
    # Baseline adult values
    baseline_gastric_ph = 1.8
    baseline_clearance_factor = 1.0
    baseline_inflammation_index = 1.0  # 1 = adult baseline
    baseline_body_fat_fraction = 0.20
    
    # Age scaling (simplified)
    age_factor = max(0, age_years - 7)  # senior threshold at ~7 years
    
    gastric_ph = baseline_gastric_ph + 0.05 * age_factor          # pH drifts upward
    clearance_factor = baseline_clearance_factor - 0.04 * age_factor  # hepatic clearance declines
    inflammation_index = baseline_inflammation_index + 0.15 * age_factor
    body_fat_fraction = baseline_body_fat_fraction + 0.02 * age_factor
    
    clearance_factor = max(0.4, clearance_factor)  # clamp to avoid zero/negative
    
    return {
        "age_years": age_years,
        "weight_kg": weight_kg,
        "gastric_ph": round(gastric_ph, 2),
        "clearance_factor": round(clearance_factor, 2),
        "inflammation_index": round(inflammation_index, 2),
        "body_fat_fraction": round(body_fat_fraction, 2)
    }

def adjust_dosing_for_senior(profile, base_mg_per_kg):
    """
    Adjusts mg/kg dosing based on reduced clearance and increased inflammation.
    """
    # Lower clearance → lower dose; higher inflammation → may require stronger effect
    clearance_adj = profile["clearance_factor"]
    inflammation_adj = profile["inflammation_index"]
    
    # Simple heuristic: scale dose by (inflammation / clearance)
    scaling = inflammation_adj / clearance_adj
    adjusted_mg_per_kg = base_mg_per_kg * min(scaling, 1.5)  # cap to avoid over-escalation
    
    return round(adjusted_mg_per_kg, 2)

# Simulation: 11-year-old, 18 kg senior spaniel
profile = get_senior_dog_profile(age_years=11, weight_kg=18.0)
adjusted_dose = adjust_dosing_for_senior(profile, base_mg_per_kg=1.5)

print("Senior Profile:", profile)
print("Adjusted mg/kg Dose:", adjusted_dose)
