from src.utils.data_loaders import DataLoader
import os

def bootstrap_real_data():
    print("Bootstrapping Real World Data...")
    
    # Pantheon+ (Easy to download directly)
    pantheon_path = "data/pantheon_plus/Pantheon+SH0ES.dat"
    try:
        sn_data = DataLoader.load_pantheon_plus_real(pantheon_path)
        print(f"Successfully loaded {len(sn_data)} Supernovae from Pantheon+ dataset.")
    except Exception as e:
        print(f"Failed to download/load Pantheon+: {e}")

    # SPARC Metadata (Distance, Luminosity, etc.)
    print("- Fetching SPARC Metadata...")
    import requests
    sparc_dir = "data/sparc"
    os.makedirs(sparc_dir, exist_ok=True)
    
    tables = {
        "Table1.mrt": "http://astroweb.cwru.edu/SPARC/Table1.mrt",
        "Table2.mrt": "http://astroweb.cwru.edu/SPARC/Table2.mrt"
    }
    
    for name, url in tables.items():
        path = os.path.join(sparc_dir, name)
        if not os.path.exists(path):
            print(f"  * Downloading {name} from {url}...")
            try:
                r = requests.get(url)
                if r.status_code == 200:
                    with open(path, "wb") as f:
                        f.write(r.content)
                    print(f"    [Done]")
                else:
                    print(f"    [Failed: {r.status_code}]")
            except Exception as e:
                print(f"    [Error: {e}]")

if __name__ == "__main__":
    bootstrap_real_data()
