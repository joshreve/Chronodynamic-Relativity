import os
import sys
import numpy as np
import pandas as pd
from scipy.optimize import minimize

# Project root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.models import ACTIVE_MODEL_NAME, LatestChronodynamicModel
from src.evaluations.benchmark_suite import BenchmarkSuite
from src.evaluations.fitter import ModelFitter
from src.utils.data_loaders import DataLoader
from src.utils.cache import ResultCache

def get_galaxy_metadata():
    metadata = {}
    path = "data/sparc/galaxy_metadata.txt"
    if not os.path.exists(path):
        print("Warning: Metadata file not found. Running generator...")
        from src.utils.generate_sparc_metadata import generate_metadata
        generate_metadata()
        
    with open(path, 'r') as f:
        for line in f:
            if line.startswith('#') or not line.strip(): continue
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 4:
                metadata[parts[0]] = {
                    'type': parts[1],
                    'morphology': parts[2],
                    'sb': parts[3]
                }
    return metadata

class EnhancedFitter(ModelFitter):
    """
    Overwrites fit_unified to use the 3D Geometric model.
    """
    def fit_unified_3d(self, model_class, sn_data, sparc_data_list, metadata, initial_params, weights=[0.5, 0.5]):
        param_names = list(initial_params.keys())
        scales = np.array([abs(initial_params[name]) if initial_params[name] != 0 else 1.0 for name in param_names])
        initial_scaled = np.array([initial_params[name] / scales[i] for i, name in enumerate(param_names)])
        
        w_exp, w_rot = weights
        
        def objective(scaled_values):
            values = scaled_values * scales
            params = dict(zip(param_names, values))
            
            try:
                model = model_class(parameters=params)
                res_sn = self.suite.evaluate_supernova(model, sn_data)
                chi2_exp = res_sn['red_chi2']
                
                rot_chi2_list = []
                for name, data, z in sparc_data_list:
                    meta = metadata.get(name)
                    # USE THE NEW 3D MODEL
                    res_rot = self.suite.evaluate_rotation_curve_3d(model, data, z=z, metadata=meta)
                    rot_chi2_list.append(res_rot['red_chi2'])
                
                chi2_rot = np.mean(rot_chi2_list)
                return w_exp * chi2_exp + w_rot * chi2_rot
            except Exception:
                return 1e20
                
        print("  * Optimizing Global Parameters (Expansion + 3D Rotation)...")
        res = minimize(objective, initial_scaled, method='Nelder-Mead', tol=1e-3,
                       callback=lambda x: print(".", end="", flush=True))
        print("\n    [Optimization Complete]")
        optimized_params = dict(zip(param_names, res.x * scales))
        return optimized_params, res.fun

def run_global_optimization():
    print("Initializing Global Optimization for Chronodynamic Relativity v8.0...")
    suite = BenchmarkSuite()
    fitter = EnhancedFitter()
    cache = ResultCache(base_dir="results/global")
    
    # 1. Load Data
    pantheon_path = "data/pantheon_plus/Pantheon+SH0ES.dat"
    sn_data = DataLoader.load_pantheon_plus_real(pantheon_path)
    metadata = get_galaxy_metadata()
    
    sparc_dir = "data/sparc"
    opt_data = []
    print("- Loading SPARC galaxies...")
    for root, _, files in os.walk(sparc_dir):
        for f in files:
            if f.endswith('_rotmod.dat'):
                name = f.replace('_rotmod.dat', '')
                d = DataLoader.load_sparc_galaxy(os.path.join(root, f))
                if d is not None:
                    z = (70.0 * d.attrs.get('dist', 0)) / 3e5
                    opt_data.append((name, d, z))
    
    print(f"  * Total galaxies for fit: {len(opt_data)}")

    # 2. Perform Fit
    # We re-optimize n and alpha_m
    init = {'n': 0.2385, 'alpha_m': 1.2e-10}
    
    # We give high weight to rotation since it has more data points and is more affected by 3D changes
    best_params, final_cost = fitter.fit_unified_3d(LatestChronodynamicModel, sn_data, opt_data, metadata, init, weights=[0.2, 0.8])
    
    print("\n--- Optimized Parameters (Chronodynamic Relativity v8.0 3D) ---")
    for k, v in best_params.items():
        print(f"  {k}: {v:.6e}")
    print(f"  Final Combined Cost: {final_cost:.4f}")

    # 3. Update Cache
    param_cache = cache.load("unified_global_optimization") or {}
    param_cache[ACTIVE_MODEL_NAME] = best_params
    cache.save("unified_global_optimization", param_cache)
    print("\nGlobal optimization cache updated successfully.")

if __name__ == "__main__":
    run_global_optimization()
