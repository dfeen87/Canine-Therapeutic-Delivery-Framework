# Project: Multi-Target PK/PD Simulation (Canine Longevity)
# License: MIT
# Architect: Don Michael Feeney Jr.

import math

def pk_concentration(time_hr, dose_mg, volume_distribution_l, clearance_rate_l_hr):
    """
    One-compartment PK model with first-order elimination.
    Returns plasma concentration (mg/L) at a given time.
    """
    k_elim = clearance_rate_l_hr / volume_distribution_l
    concentration = (dose_mg / volume_distribution_l) * math.exp(-k_elim * time_hr)
    return concentration

def pd_effect(concentration, ec50, hill_coefficient=1.2):
    """
    Hill-type PD model for target engagement.
    Returns fractional effect (0 to 1).
    """
    effect = (concentration ** hill_coefficient) / (
        ec50 ** hill_coefficient + concentration ** hill_coefficient
    )
    return effect

def simulate_multi_target_response(
    time_hr,
    dose_mg,
    v_dist_l,
    clearance_l_hr,
    metabolic_ec50,
    neuro_ec50
):
    """
    Integrates PK with two PD pathways:
    - Metabolic modulation
    - Neuroinflammatory suppression
    """
    
    # PK: plasma concentration at time t
    conc = pk_concentration(time_hr, dose_mg, v_dist_l, clearance_l_hr)
    
    # PD: target-specific effects
    metabolic_effect = pd_effect(conc, metabolic_ec50)
    neuro_effect = pd_effect(conc, neuro_ec50)
    
    return {
        "time_hr": time_hr,
        "plasma_concentration_mg_L": round(conc, 4),
        "metabolic_modulation": round(metabolic_effect, 3),
        "neuroinflammatory_suppression": round(neuro_effect, 3)
    }

# Simulation: 40 lb Spaniel, 1.5 mg/kg dose, 12-hour window
results = [
    simulate_multi_target_response(
        time_hr=t,
        dose_mg=27,            # 18 kg * 1.5 mg/kg
        v_dist_l=9.0,
        clearance_l_hr=0.6,
        metabolic_ec50=0.8,
        neuro_ec50=1.2
    )
    for t in range(0, 13, 2)
]

for r in results:
    print(r)
