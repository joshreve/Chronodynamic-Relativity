import numpy as np
from scipy.optimize import minimize
from src.evaluations.benchmark_suite import BenchmarkSuite

class ModelFitter:
    """
    Utility to optimize model parameters against observational datasets.
    """
    def __init__(self):
        self.suite = BenchmarkSuite()

    def fit_gravity(self, custom_model_class, custom_accel_func, galaxy_data, initial_params):
        """
        Find best-fit parameters for a custom gravity model using a galaxy rotation curve.
        """
        param_names = list(initial_params.keys())
        scales = np.array([abs(initial_params[name]) if initial_params[name] != 0 else 1.0 for name in param_names])
        initial_scaled = np.array([initial_params[name] / scales[i] for i, name in enumerate(param_names)])

        def objective(scaled_values):
            values = scaled_values * scales
            params = dict(zip(param_names, values))
            model = custom_model_class(custom_accel_func=custom_accel_func, parameters=params)
            try:
                # Disable optimize_ups to fit purely the custom parameters
                results = self.suite.evaluate_rotation_curve(model, galaxy_data, optimize_ups=False)
                return results['red_chi2']
            except Exception as e:
                import traceback
                traceback.print_exc()
                return 1e20

        res = minimize(objective, initial_scaled, method='Nelder-Mead', tol=1e-6)
        optimized_values = res.x * scales
        optimized_params = dict(zip(param_names, optimized_values))

        return optimized_params, res.fun

    def fit_cosmology(self, custom_model_class, custom_h_func, sn_data, initial_params):
        """
        Find best-fit parameters for a CustomCosmology model using Supernova data.
        """
        param_names = list(initial_params.keys())
        # Scale factors to normalize parameters around 1.0 for the optimizer
        scales = np.array([abs(initial_params[name]) if initial_params[name] != 0 else 1.0 for name in param_names])
        initial_scaled = np.array([initial_params[name] / scales[i] for i, name in enumerate(param_names)])
        
        def objective(scaled_values):
            values = scaled_values * scales
            params = dict(zip(param_names, values))
            model = custom_model_class(custom_h_func=custom_h_func, parameters=params)
            try:
                results = self.suite.evaluate_supernova(model, sn_data)
                return results['red_chi2'] * len(sn_data)
            except Exception:
                return 1e20
                
        res = minimize(objective, initial_scaled, method='Nelder-Mead', tol=1e-6)
        optimized_values = res.x * scales
        optimized_params = dict(zip(param_names, optimized_values))
        
        return optimized_params, res.fun

    def fit_unified(self, model_class, sn_data, sparc_data_list, initial_params, weights=[0.5, 0.5]):
        """
        Simultaneously optimize against Supernova (Expansion) and Galaxy (Rotation) data.
        sparc_data_list: List of (galaxy_df, z) tuples.
        weights: [weight_expansion, weight_rotation]
        """
        param_names = list(initial_params.keys())
        scales = np.array([abs(initial_params[name]) if initial_params[name] != 0 else 1.0 for name in param_names])
        initial_scaled = np.array([initial_params[name] / scales[i] for i, name in enumerate(param_names)])
        
        w_exp, w_rot = weights
        
        def objective(scaled_values):
            values = scaled_values * scales
            params = dict(zip(param_names, values))
            
            try:
                # 1. Instantiate model with current params
                model = model_class(parameters=params)
                
                # 2. Expansion Cost (Reduced Chi2)
                res_sn = self.suite.evaluate_supernova(model, sn_data)
                chi2_exp = res_sn['red_chi2']
                
                # 3. Rotation Cost (Mean Reduced Chi2 across full sample)
                rot_chi2_list = []
                for data, z in sparc_data_list:
                    res_rot = self.suite.evaluate_rotation_curve(model, data, z=z)
                    rot_chi2_list.append(res_rot['red_chi2'])
                
                chi2_rot = np.mean(rot_chi2_list)
                
                # Weighted cost function
                return w_exp * chi2_exp + w_rot * chi2_rot
                
            except Exception:
                return 1e20
                
        res = minimize(objective, initial_scaled, method='Nelder-Mead', tol=1e-3,
                       callback=lambda x: print(".", end="", flush=True))
        print("\n    [Optimization Complete]")
        optimized_params = dict(zip(param_names, res.x * scales))
        
        return optimized_params, res.fun
