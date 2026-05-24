# Project: Delivery-Matrix Optimization (Genetic Algorithm)
# License: MIT
# Architect: Don Michael Feeney Jr.

import random

# --- Design Space Encoding ---
# Each "matrix" is a candidate design with:
# - lipid_content (0–1)
# - particle_size_nm (20–200)
# - bile_salt_affinity (0–2)
# - shield_strength (0–1)  # peptide/zwitterionic protection

def random_matrix():
    return {
        "lipid_content": round(random.uniform(0.2, 0.8), 3),
        "particle_size_nm": round(random.uniform(30, 150), 1),
        "bile_salt_affinity": round(random.uniform(0.5, 1.8), 3),
        "shield_strength": round(random.uniform(0.4, 1.0), 3)
    }

# --- Fitness Function ---
def evaluate_fitness(matrix):
    """
    Scores a delivery matrix based on:
    - Lymphatic routing likelihood
    - Gastric protection
    - Stability proxy
    - Reduced protein binding risk
    """
    lipid = matrix["lipid_content"]
    size_nm = matrix["particle_size_nm"]
    bile_aff = matrix["bile_salt_affinity"]
    shield = matrix["shield_strength"]
    
    # Lymphatic routing score (Appendix B logic inspired)
    lymphatic_score = 0
    if lipid >= 0.3 and size_nm >= 50 and bile_aff >= 1.2:
        lymphatic_score = 1.0
    else:
        lymphatic_score = (lipid * 0.6) + (bile_aff * 0.4)
    
    # Gastric protection (Appendix A + D inspired)
    protection_score = shield  # stronger shield → better protection
    
    # Stability proxy (Appendix G inspired)
    stability_score = 0.5 + (lipid * 0.3) + (shield * 0.2)
    
    # Protein binding risk (inverse; higher shield & lipid → lower risk)
    binding_risk = max(0.1, 1.2 - (shield + lipid))
    binding_score = 1.0 / binding_risk  # higher is better
    
    # Aggregate fitness
    fitness = (
        0.3 * lymphatic_score +
        0.3 * protection_score +
        0.2 * stability_score +
        0.2 * binding_score
    )
    return fitness

# --- Genetic Algorithm Core ---
def mutate(matrix, rate=0.2):
    new = matrix.copy()
    if random.random() < rate:
        new["lipid_content"] = round(min(0.9, max(0.1, new["lipid_content"] + random.uniform(-0.1, 0.1))), 3)
    if random.random() < rate:
        new["particle_size_nm"] = round(min(200, max(20, new["particle_size_nm"] + random.uniform(-15, 15))), 1)
    if random.random() < rate:
        new["bile_salt_affinity"] = round(min(2.0, max(0.3, new["bile_salt_affinity"] + random.uniform(-0.2, 0.2))), 3)
    if random.random() < rate:
        new["shield_strength"] = round(min(1.0, max(0.2, new["shield_strength"] + random.uniform(-0.1, 0.1))), 3)
    return new

def crossover(parent1, parent2):
    child = {}
    for key in parent1.keys():
        child[key] = parent1[key] if random.random() < 0.5 else parent2[key]
    return child

def optimize_delivery_matrix(
    population_size=20,
    generations=30,
    elite_fraction=0.2
):
    # Initialize population
    population = [random_matrix() for _ in range(population_size)]
    
    for gen in range(generations):
        scored = [(evaluate_fitness(m), m) for m in population]
        scored.sort(reverse=True, key=lambda x: x[0])
        
        elites_count = max(1, int(population_size * elite_fraction))
        elites = [m for _, m in scored[:elites_count]]
        
        # Print best of generation (optional)
        best_fitness, best_matrix = scored[0]
        print(f"Generation {gen}: Best Fitness = {best_fitness:.3f}, Design = {best_matrix}")
        
        # Create next generation
        next_pop = elites.copy()
        while len(next_pop) < population_size:
            parent1, parent2 = random.sample(elites, 2)
            child = crossover(parent1, parent2)
            child = mutate(child)
            next_pop.append(child)
        
        population = next_pop
    
    # Final best
    final_scored = [(evaluate_fitness(m), m) for m in population]
    final_scored.sort(reverse=True, key=lambda x: x[0])
    return final_scored[0]

# Run Optimization
best = optimize_delivery_matrix()
print("\nOptimized Delivery Matrix:", best)
