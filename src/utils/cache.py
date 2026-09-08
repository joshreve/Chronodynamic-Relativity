import json
import os
import numpy as np

class ResultCache:
    """
    Utilities for saving and loading optimized model parameters and benchmark results.
    """
    def __init__(self, base_dir="results"):
        self.base_dir = base_dir
        os.makedirs(base_dir, exist_ok=True)

    def _convert_numpy(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return obj

    def save(self, name, data):
        """Save results to a JSON file."""
        path = os.path.join(self.base_dir, f"{name}.json")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        # Ensure numpy types are serializable
        clean_data = self._process_numpy(data)
        with open(path, "w") as f:
            json.dump(clean_data, f, indent=4)
        print(f"  [Cached] Results saved to {path}")

    def load(self, name):
        """Load results from a JSON file if it exists."""
        path = os.path.join(self.base_dir, f"{name}.json")
        if os.path.exists(path):
            with open(path, "r") as f:
                return json.load(f)
        return None

    def _process_numpy(self, data):
        if isinstance(data, dict):
            return {k: self._process_numpy(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self._process_numpy(v) for v in data]
        else:
            return self._convert_numpy(data)
