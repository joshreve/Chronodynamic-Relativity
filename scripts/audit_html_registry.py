import os
import re
import datetime

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
OUTPUT_MD_DEV = os.path.join(PROJECT_ROOT, "development", "docs", "HTML_DOCUMENTATION_REGISTRY.md")
OUTPUT_MD_OFF = os.path.join(PROJECT_ROOT, "official", "docs", "HTML_DOCUMENTATION_REGISTRY.md")
OUTPUT_MD_PUB = os.path.abspath(os.path.join(PROJECT_ROOT, "../Chronodynamic-Relativity/docs/HTML_DOCUMENTATION_REGISTRY.md"))

# Exclusion patterns for vendor or temporary build directories
IGNORE_DIRS = {'.venv', 'node_modules', 'MUSIC2', 'ramses', 'build', '.git', '__pycache__', 'dist'}

def scan_html_files():
    html_records = []
    
    for root, dirs, files in os.walk(PROJECT_ROOT):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS and not d.startswith('.')]
        
        for f in files:
            if f.endswith('.html'):
                full_path = os.path.join(root, f)
                rel_path = os.path.relpath(full_path, PROJECT_ROOT).replace('\\', '/')
                
                stat = os.stat(full_path)
                mtime = datetime.datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
                size_kb = stat.st_size / 1024.0
                
                title = ""
                description = ""
                try:
                    with open(full_path, 'r', encoding='utf-8', errors='ignore') as fp:
                        content = fp.read(4096)
                        t_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
                        if t_match:
                            title = t_match.group(1).strip()
                            
                        d_match = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', content, re.IGNORECASE)
                        if d_match:
                            description = d_match.group(1).strip()
                        elif not description:
                            h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.IGNORECASE | re.DOTALL)
                            if h1_match:
                                description = re.sub(r'<[^>]+>', '', h1_match.group(1)).strip()
                except Exception as e:
                    title = f"Error reading: {e}"
                
                if not title:
                    title = f.replace('.html', '').replace('_', ' ').title()
                    
                category, status, purpose = classify_file(rel_path, title, description)
                
                html_records.append({
                    'rel_path': rel_path,
                    'filename': f,
                    'title': title,
                    'purpose': purpose,
                    'category': category,
                    'status': status,
                    'mtime': mtime,
                    'size_kb': size_kb
                })
                
    return html_records

def classify_file(rel_path, title, desc):
    # 1. Official Analyses Suite (Canonical Public Release)
    if rel_path.startswith("official/docs/analyses/") or rel_path.startswith("docs/analyses/"):
        if "cosmic_expansion" in rel_path:
            return "Official Analysis: Cosmic Expansion & SNe Ia", "Active Public Release", f"Pillar I canonical analysis: {title}"
        elif "galactic_rotation" in rel_path:
            return "Official Analysis: Galactic Kinematics & SPARC", "Active Public Release", f"Pillar II canonical analysis: {title}"
        elif "strong_lensing" in rel_path:
            return "Official Analysis: Strong Lensing & Bullet Cluster", "Active Public Release", f"Pillar III canonical analysis: {title}"
        elif "early_universe" in rel_path:
            return "Official Analysis: Early Universe, CMB & DESI BAO", "Active Public Release", f"Pillar IV canonical analysis: {title}"
        elif "theory" in rel_path:
            return "Official Analysis: Theoretical Foundations & QFT", "Active Public Release", f"Theoretical foundations: {title}"
        else:
            return "Official Analysis: Master Portals & Dashboards", "Active Public Release", f"Primary portal dashboard: {title}"
            
    # 2. Development & In-Progress Research Investigations
    if "development/docs/investigations" in rel_path or "docs/investigations" in rel_path:
        if any(k in rel_path for k in ['class_cr', 'boltzmann', 'cmb_perturbation']):
            return "Development: Paper II Boltzmann Investigations", "Dev Repository Only (Paper II)", f"In-progress Boltzmann solver test: {title}"
        else:
            return "Development: Research Investigations & Sweeps", "Dev Repository Only", f"Diagnostic investigation: {title}"
            
    # 3. Simulations Suite
    if "simulations" in rel_path:
        return "Development: 3D Simulation Sandboxes", "Dev Repository Only", f"3D simulation sandbox visualizer: {title}"
        
    return "Miscellaneous Documentation", "Dev Repository Only", desc or title

def generate_markdown_registry(records):
    records.sort(key=lambda r: (r['category'], r['status'], r['rel_path']))
    
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    md = []
    md.append("# Chronodynamic Relativity: HTML Documentation Registry & Purpose Tracker\n")
    md.append(f"> **Auto-Generated on:** `{now_str}`  ")
    md.append(f"> **Total Tracked HTML Documents:** `{len(records)}`  ")
    md.append("> **Auditing Tool:** `scripts/audit_html_registry.py`\n")
    md.append("---\n")
    md.append("## 1. Release Classification Summary\n")
    
    status_counts = {}
    cat_counts = {}
    for r in records:
        status_counts[r['status']] = status_counts.get(r['status'], 0) + 1
        cat_counts[r['category']] = cat_counts.get(r['category'], 0) + 1
        
    md.append("| Release Status | Count | Description |")
    md.append("| :--- | :---: | :--- |")
    md.append(f"| **Active Public Release** | {status_counts.get('Active Public Release', 0)} | Canonical production pages and recategorized public-ready analyses published to `Chronodynamic-Relativity`. |")
    md.append(f"| **Dev Repository Only (Paper II)** | {status_counts.get('Dev Repository Only (Paper II)', 0)} | In-progress CLASS-CR Boltzmann solvers and high-$\\ell$ polarization suites reserved for companion papers. |")
    md.append(f"| **Dev Repository Only** | {status_counts.get('Dev Repository Only', 0)} | Intermediate research scripts, exploratory parameter sweeps, and 3D simulation sandboxes. |\n")
    md.append("---\n")
    
    md.append("## 2. Complete HTML Document Catalog\n")
    
    current_cat = None
    for r in records:
        if r['category'] != current_cat:
            current_cat = r['category']
            md.append(f"\n### {current_cat}\n")
            md.append("| HTML Document / Path | Last Modified | Size | Release Status | Purpose / Topic |")
            md.append("| :--- | :---: | :---: | :---: | :--- |")
            
        filename_display = f"`{r['filename']}`"
        size_str = f"{r['size_kb']:.1f} KB" if r['size_kb'] < 1024 else f"{r['size_kb']/1024:.2f} MB"
        status_badge = f"`{r['status']}`"
        
        md.append(f"| **{filename_display}**<br><sub>`{r['rel_path']}`</sub> | `{r['mtime']}` | {size_str} | {status_badge} | {r['purpose']} |")
        
    md.append("\n---\n")
    md.append("## 3. Maintenance Instructions\n")
    md.append("To refresh this registry after modifying HTML files or running new simulations:\n")
    md.append("```bash\n& \".venv/Scripts/python.exe\" scripts/audit_html_registry.py\n```\n")
    
    content = "\n".join(md)
    if os.path.exists(os.path.join(PROJECT_ROOT, "official")):
        out_paths = [OUTPUT_MD_DEV, OUTPUT_MD_OFF]
        if os.path.exists(os.path.dirname(OUTPUT_MD_PUB)):
            out_paths.append(OUTPUT_MD_PUB)
    else:
        out_paths = [os.path.join(PROJECT_ROOT, "docs", "HTML_DOCUMENTATION_REGISTRY.md")]

    for out_path in out_paths:
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Registry generated successfully at: {out_path} ({len(records)} files tracked)")

if __name__ == "__main__":
    records = scan_html_files()
    generate_markdown_registry(records)
