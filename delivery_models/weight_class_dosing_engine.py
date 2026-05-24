# Project: Weight-Class Dosing Engine (Canine Longevity)
# License: MIT
# Architect: Don Michael Feeney Jr.

def calculate_dose_mg(dog_weight_kg, target_mg_per_kg):
    """
    Calculates total dose (mg) based on dog weight and target mg/kg.
    """
    return dog_weight_kg * target_mg_per_kg

def calculate_volume_per_actuation_ml(
    total_dose_mg,
    api_concentration_mg_per_ml,
    max_acts_per_feeding
):
    """
    Converts total mg dose into volumetric actuations for a calibrated pump system.
    """
    total_volume_ml = total_dose_mg / api_concentration_mg_per_ml
    volume_per_actuation = total_volume_ml / max_acts_per_feeding
    return total_volume_ml, volume_per_actuation

def generate_dosing_schedule(
    dog_weight_kg,
    target_mg_per_kg,
    api_concentration_mg_per_ml,
    feedings_per_day=2,
    max_acts_per_feeding=3
):
    """
    Generates a structured dosing schedule for a given dog weight.
    Outputs total daily dose, volume, and per-feeding actuation pattern.
    """
    total_dose_mg = calculate_dose_mg(dog_weight_kg, target_mg_per_kg)
    total_volume_ml, volume_per_actuation = calculate_volume_per_actuation_ml(
        total_dose_mg,
        api_concentration_mg_per_ml,
        max_acts_per_feeding
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
        "acts_per_feeding": max_acts_per_feeding
    }

# Simulation: 18 kg (≈40 lb) Spaniel on 1.5 mg/kg Target Dose
schedule = generate_dosing_schedule(
    dog_weight_kg=18.0,
    target_mg_per_kg=1.5,
    api_concentration_mg_per_ml=10.0,
    feedings_per_day=2,
    max_acts_per_feeding=3
)

print("Dosing Schedule:", schedule)
