# Project: Protein-Binding Probability Model (Canine Longevity)
# License: MIT
# Architect: Don Michael Feeney Jr.

def calculate_binding_probability(
    gastric_ph, 
    dietary_protein_g, 
    calcium_mg, 
    api_charge_state, 
    protective_matrix=False
):
    """
    Estimates the probability of non-specific protein or calcium binding 
    for an orally delivered API in the canine stomach.
    """
    
    # Baseline binding coefficients (arbitrary units for simulation)
    protein_binding_coeff = 0.02
    calcium_binding_coeff = 0.015
    
    # Acidic environment increases binding risk
    acidity_factor = max(0, (2.5 - gastric_ph)) * 0.1
    
    # Charge-state multiplier (cationic APIs bind more readily)
    if api_charge_state == "positive":
        charge_multiplier = 1.8
    elif api_charge_state == "neutral":
        charge_multiplier = 1.0
    else:  # negative
        charge_multiplier = 1.3
    
    # Calculate raw binding probability
    binding_probability = (
        dietary_protein_g * protein_binding_coeff +
        calcium_mg * calcium_binding_coeff
    ) * charge_multiplier * (1 + acidity_factor)
    
    # Apply protective matrix logic
    if protective_matrix:
        binding_probability *= 0.15  # 85% reduction via zwitterionic shielding
        return f"Binding Risk: {binding_probability:.2f} (Shielded). API Protected."
    
    return f"Binding Risk: {binding_probability:.2f} (Unshielded). High Probability of API Loss."

# Simulation: High-Protein Meal Without Protective Matrix
current_risk = calculate_binding_probability(
    gastric_ph=1.8,
    dietary_protein_g=35,
    calcium_mg=120,
    api_charge_state="positive",
    protective_matrix=False
)
print(current_risk)
