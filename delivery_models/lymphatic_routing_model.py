# Project: Lymphatic Routing Model (Canine Longevity)
# License: MIT
# Architect: Don Michael Feeney Jr.

def determine_absorption_route(lipid_content, particle_size_nm, bile_salt_level, api_lipophilicity):
    """
    Simulates the absorption pathway of an orally delivered therapeutic.
    Determines whether the API enters the portal circulation (liver-first)
    or the intestinal lymphatic system (liver-bypass).
    """
    
    # Thresholds for lymphatic uptake
    lipid_threshold = 0.3          # Minimum lipid fraction required for chylomicron formation
    size_threshold_nm = 50         # Nanoparticle size needed for lymphatic transport
    bile_salt_trigger = 1.2        # Minimum bile salt concentration for emulsification
    lipophilicity_trigger = 4.0    # LogP threshold for lipid-phase partitioning
    
    # Default route: portal vein (first-pass metabolism)
    route = "Portal Circulation"
    
    # Lymphatic routing logic
    if (lipid_content >= lipid_threshold and
        particle_size_nm >= size_threshold_nm and
        bile_salt_level >= bile_salt_trigger and
        api_lipophilicity >= lipophilicity_trigger):
        
        route = "Intestinal Lymphatic System"
        return "Routing Status: Lymphatic Uptake. First-Pass Metabolism Bypassed."
    
    else:
        return "Routing Status: Portal Absorption. Subject to First-Pass Metabolism."

# Simulation: High-Lipid Encapsulation for Lymphatic Routing
current_route = determine_absorption_route(
    lipid_content=0.45,
    particle_size_nm=80,
    bile_salt_level=1.5,
    api_lipophilicity=4.8
)
print(current_route)
