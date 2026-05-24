# Project: Micro-Encapsulation Stability Model (Canine Longevity)
# License: MIT
# Architect: Don Michael Feeney Jr.

def evaluate_encapsulation_stability(
    temperature_c,
    humidity_percent,
    mechanical_agitation,
    storage_days,
    matrix_type="lipid"
):
    """
    Predicts stability of a cold-processed micro-encapsulation matrix
    under real-world environmental conditions.
    """
    
    # Baseline stability scores (arbitrary units)
    stability_score = 100.0
    
    # Temperature thresholds
    if temperature_c > 45:
        stability_score -= 25
    elif temperature_c > 30:
        stability_score -= 10
    
    # Humidity thresholds
    if humidity_percent > 70:
        stability_score -= 20
    elif humidity_percent > 50:
        stability_score -= 8
    
    # Mechanical agitation (0 = none, 1 = high)
    if mechanical_agitation >= 0.8:
        stability_score -= 20
    elif mechanical_agitation >= 0.4:
        stability_score -= 10
    
    # Storage duration effects
    if storage_days > 180:
        stability_score -= 20
    elif storage_days > 90:
        stability_score -= 10
    
    # Matrix-type modifiers
    if matrix_type == "lipid":
        stability_score *= 1.05  # lipid matrices resist humidity + agitation
    elif matrix_type == "powder":
        stability_score *= 0.95  # powders slightly more humidity-sensitive
    
    # Clamp score
    stability_score = max(0, min(stability_score, 100))
    
    # Interpret results
    if stability_score >= 80:
        return f"Stability: {stability_score:.1f}. Matrix Fully Intact. API Protected."
    elif stability_score >= 50:
        return f"Stability: {stability_score:.1f}. Partial Degradation Risk."
    else:
        return f"Stability: {stability_score:.1f}. High Degradation Risk. Matrix Compromised."

# Simulation: 90-Day Storage, Warm Room, Moderate Agitation
current_status = evaluate_encapsulation_stability(
    temperature_c=32,
    humidity_percent=55,
    mechanical_agitation=0.3,
    storage_days=90,
    matrix_type="lipid"
)
print(current_status)
