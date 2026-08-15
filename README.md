# **Canine‑Therapeutic‑Delivery‑Framework (v2.0.0)**

A research‑grade computational framework for modeling next‑generation delivery systems for canine longevity therapeutics and food palatability regulation.

This suite integrates **phase‑specific gating**, **lymphatic routing**, **thermal‑stress modeling**, **protein‑binding risk**, **PK/PD simulation**, **senior‑dog physiological variability**, **mg/kg dosing engines**, a **genetic‑algorithm delivery‑matrix optimizer**, and a **palatability & dopamine regulation analysis module**—all under the MIT License.

Built for translational teams advancing **veterinary pharmacology**, **drug‑delivery engineering**, **pet food chemistry**, and **canine healthspan science**.

---

## **v2.0.0 Release Notes: Palatability & Dopamine Regulation Module**

Version **2.0.0** introduces a scientific analysis module for **Canine Food Additive & Palatability Regulation** (`delivery_models.palatability_regulation_model`). This module evaluates food formulations for chemical additives, processing parameters, and release kinetics that influence dopamine-reward pathways and eating behavior.

### Key Capabilities:
* **Additive Profiling**: Quantifies palatant loads across animal fats, hydrolyzed proteins, yeast extracts, Maillard compounds, and plant/insect hydrolysates.
* **Chemosensoric VOC Profiling**: Aligns GC-MS/O compound classes (volatile aromatics, sulfur compounds, amino-acid derivatives, VOC clusters) with canine olfaction thresholds.
* **Coating Kinetics**: Evaluates single-phase vs. dual-phase coating architectures and release dynamics.
* **Dopamine-Palatability Risk Score (0–100)**: Assesses risk of hyper-arousal, reward over-stimulation, and compulsive eating (classified as *Low*, *Moderate*, or *High* risk).
* **Cognitive Ease Index (0.00–1.00)**: Models whether the food profile promotes calm, non-compulsive eating behavior.
* **Chew-Behavior Compatibility Score (0–100)**: Evaluates kibble hardness, friability, moisture, and chew-phase duration.
* **Formulation Balancing Recommendations**: Automatically generates targeted formulation adjustments when cognitive comfort or safety thresholds are breached.

### Quick Example:
```python
from delivery_models import (
    Additive, CoatingArchitecture, FoodFormulation,
    NutrientBase, PalatabilityRegulationModel,
    ProcessingParams, TextureParams, VolatileProfile,
)

formulation = FoodFormulation(
    formulation_id="FORM_LONGEVITY_01",
    name="Calm Longevity Kibble",
    palatants=[Additive(name="Chicken Fat", palatant_type="animal_fat", concentration_pct=2.0)],
    processing=ProcessingParams(extrusion_temp_c=108.0, moisture_pct=10.0, maillard_intensity=3.5),
    coating=CoatingArchitecture(coating_type="single_phase"),
    volatile_profile=VolatileProfile(volatile_aromatics=25.0, sulfur_compounds=12.0),
    texture=TextureParams(hardness_n=52.0, friability_pct=4.5, chew_phase_breakdown_sec=11.0),
    nutrient_base=NutrientBase(glycemic_index=45.0),
)

model = PalatabilityRegulationModel()
result = model.analyze_formulation(formulation)
print(result)
```

For a full demonstration, run:
```bash
python3 examples/palatability_demo.py
```

---

Public Overview:  

A narrative, non‑technical summary of this framework is available as a LinkedIn article:
From Lab to Bowl: Solving the Pharmacokinetic Hurdle in Canine Healthspan Expansion — [LinkedIn Article](https://www.linkedin.com/pulse/from-lab-bowl-solving-pharmacokinetic-hurdle-canine-feeney-jr-pyile/)

---

Acknowledgments: 
> This framework is built on the shoulders of the researchers and biotech innovators actively pioneering the science of canine longevity—thank you for leading the charge in helping our companions live healthier, longer lives. Additionally, a special thanks to the tools that helped accelerate this architecture: conceptual synthesis and structural refinement were supported by Google Gemini, while Microsoft Copilot provided code generation and syntax formatting for the Python pipelines.
