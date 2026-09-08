import os
import pandas as pd
import numpy as np

def generate_metadata():
    print("Generating comprehensive SPARC metadata...")
    dirs = ['data/sparc/Rotmod_LTG', 'data/sparc/Rotmod_ETG']
    metadata = []
    
    for d in dirs:
        type_code = "LTG" if "LTG" in d else "ETG"
        for f in os.listdir(d):
            if f.endswith("_rotmod.dat"):
                name = f.replace("_rotmod.dat", "")
                path = os.path.join(d, f)
                
                # Load first few lines to get SB
                try:
                    df = pd.read_csv(path, sep=r'\s+', comment='#', header=None, 
                                     usecols=[0,1,2,3,4,5], names=['r','v_obs','v_err','v_gas','v_disk','v_bulge'])
                    # SB estimation: if v_disk is high at small radii, it's probably HSB
                    # But better: just categorize by morphology in name or use directory
                    morphology = "Spiral" if type_code == "LTG" else "Elliptical/S0"
                    if "DDO" in name or "UGC" in name:
                        if name not in ["UGC2487", "UGC2885"]: # Exceptions
                            morphology = "Dwarf/LSB"
                    
                    # surface brightness category
                    # Typical high-SB galaxies have v_disk peak > 100 km/s?
                    sb = "High" if df['v_disk'].max() > 120 else "Low"
                    if df['v_disk'].max() > 50 and df['v_disk'].max() <= 120:
                        sb = "Medium"
                        
                    metadata.append(f"{name} | {type_code} | {morphology} | {sb} | Automated categorization.")
                except:
                    continue
                    
    with open("data/sparc/galaxy_metadata.txt", "w") as f:
        f.write("# SPARC Galaxy Categorization Metadata\n")
        f.write("# Galaxy ID | Type | Morphology | Surface Brightness | Notes\n")
        for line in metadata:
            f.write(line + "\n")
            
    print(f"Generated metadata for {len(metadata)} galaxies.")

if __name__ == "__main__":
    generate_metadata()
