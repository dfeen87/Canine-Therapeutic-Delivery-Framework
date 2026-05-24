"""Minimal demo for phase-specific gating logic."""

from __future__ import annotations

import os
import sys

# Allow running this script directly from the examples/ folder.
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from delivery_models.phase_specific_delivery_matrix import calculate_peptide_stability


def main() -> None:
    """Run a couple of simple gating scenarios."""
    scenarios = [
        {
            "label": "Gastric phase (shield intact)",
            "environment_ph": 1.8,
            "pepsin_concentration": 0.9,
            "transit_time": 90.0,
        },
        {
            "label": "Duodenal phase (release)",
            "environment_ph": 6.8,
            "pepsin_concentration": 0.1,
            "transit_time": 45.0,
        },
    ]

    for scenario in scenarios:
        status = calculate_peptide_stability(
            environment_ph=scenario["environment_ph"],
            pepsin_concentration=scenario["pepsin_concentration"],
            transit_time=scenario["transit_time"],
        )
        print(f"{scenario['label']}: {status}")


if __name__ == "__main__":
    main()
