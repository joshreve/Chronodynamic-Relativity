import os
import sys
import json

# Project root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.utils.cache import ResultCache

def fast_track_cache():
    print("Generating fast-track global cache for lensing investigation...")
    cache = ResultCache(base_dir="results/global")
    
    # Using the previously observed global optimal parameters
    param_cache = {
        'V5 (Screened Yukawa)': {'n': 0.2385, 'alpha_m': 1.25e-10, 'rs_yuk': 185.0, 'alpha': 1.59, 'r_core': 1.0},
        'V4 (Horizon-Linked)': {'n': 0.2385, 'alpha_m': 1.25e-10, 'r_core': 1.0},
        'V3 (Softened Core)': {'n': 0.2385, 'alpha_m': 1.21e-10, 'alpha': 1.66, 'r_core': 1.0},
        'V2 (Linear Membrane)': {'n': 0.2385, 'alpha_m': 1.2e-10},
        'V1 (Simple Repulsion)': {'n': 0.2385, 'alpha': 5.0}
    }
    
    cache.save("unified_global_optimization", param_cache)
    print("Cache generated.")

if __name__ == "__main__":
    fast_track_cache()
