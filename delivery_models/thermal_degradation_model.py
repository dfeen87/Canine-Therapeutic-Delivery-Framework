# Project: Thermal Degradation Model (Canine Longevity)
# License: MIT
# Architect: Don Michael Feeney Jr.

def simulate_thermal_degradation(temperature_c, shear_force, exposure_time):
    """
    Models the degradation of a synthetic longevity API under extrusion-like conditions.
    Returns predicted molecular integrity based on thermal and mechanical stress.
    """
    
    # Thermal thresholds for complex synthetic APIs
    denaturation_temp = 55       # Many engineered peptides begin unfolding
    collapse_temp = 90           # Structural collapse accelerates
    annihilation_temp = 130      # Near-total molecular destruction
    
    # Shear force thresholds (arbitrary units for simulation)
    shear_threshold = 0.7        # High mechanical stress
    
    # Default integrity (100% = fully intact)
    integrity = 100.0
    
    # Thermal degradation logic
    if temperature_c >= annihilation_temp:
        integrity -= 95
        return "Status: Thermal Annihilation. API Destroyed (<5% Integrity)."
    
    elif temperature_c >= collapse_temp:
        integrity -= 70
        if shear_force >= shear_threshold:
            integrity -= 20
        return f"Status: Structural Collapse. Approx. {integrity}% Integrity Remaining."
    
    elif temperature_c >= denaturation_temp:
        integrity -= 40
        if shear_force >= shear_threshold:
            integrity -= 10
        return f"Status: Partial Denaturation. Approx. {integrity}% Integrity Remaining."
    
    else:
        return "Status: Thermally Stable. API Integrity Preserved."
    

# Simulation: Extrusion Conditions (Typical Kibble Manufacturing)
current_status = simulate_thermal_degradation(
    temperature_c=150, 
    shear_force=0.8, 
    exposure_time=45
)
print(current_status)
