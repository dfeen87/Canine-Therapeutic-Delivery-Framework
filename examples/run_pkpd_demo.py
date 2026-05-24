"""Minimal demo for the multi-target PK/PD simulation."""

from __future__ import annotations

import os
import sys

# Allow running this script directly from the examples/ folder.
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from delivery_models.multi_target_pkpd_simulation import simulate_multi_target_response


def main() -> None:
    """Simulate a few PK/PD time points and print the results."""
    for time_hr in (0, 2, 4, 6):
        response = simulate_multi_target_response(
            time_hr=time_hr,
            dose_mg=27.0,
            v_dist_l=9.0,
            clearance_l_hr=0.6,
            metabolic_ec50=0.8,
            neuro_ec50=1.2,
        )
        print(f"t={time_hr} hr -> {response}")


if __name__ == "__main__":
    main()
