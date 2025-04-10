
#!/usr/bin/env python3
# setup_project.py

import os

base_path = os.path.expanduser("~/wifi_ecology_project")

structure = {
    "": ["requirements.txt", ".gitignore", "README.md"],
    "scripts": ["collector.py"],
    "data": ["wifi_scans.csv"],
    "utils": ["vendor_lookup.py"],
    "visuals": ["explorer.py"]
}

files_content = {
    "requirements.txt": "gspread\noauth2client\npandas\nnumpy\nmatplotlib\nrich\n",
    ".gitignore": "__pycache__/\n*.pyc\n.env\nwifi_scans.csv\n*.log\n",
    "README.md": "# 📡 Wi-Fi Ecology Project\n\nReal-time local Wi-Fi environment sensing and 3D visualization using OpenGL.\n",
    "scripts/collector.py": "# Entry point for Wi-Fi scanning and CSV logging\n",
    "data/wifi_scans.csv": "timestamp,mac_address,ssid,freq,signal,vendor_name,guessed_name,first_seen,last_seen,seen_count,num_disconnects,avg_connection_duration,mobility_score,heat_score\n",
    "utils/vendor_lookup.py": "# Utility for MAC vendor lookups (stub OUI DB)\nOUI_VENDOR_MAP = {}\n",
    "visuals/explorer.py": "# Placeholder for OpenGL-based 3D visualization of Wi-Fi ecology\n"
}

def create_structure():
    for folder, files in structure.items():
        folder_path = os.path.join(base_path, folder)
        os.makedirs(folder_path, exist_ok=True)
        for file in files:
            path = os.path.join(folder_path, file)
            key = f"{folder}/{file}" if folder else file
            with open(path, "w") as f:
                f.write(files_content.get(key, ""))

if __name__ == "__main__":
    create_structure()
    print(f"✅ Wi-Fi Ecology Project setup created at {base_path}")
