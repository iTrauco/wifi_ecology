# 📡 Wi-Fi Ecology Project 

This project passively scans and logs Wi-Fi device activity in your environment, building a real-time profile of your local wireless "ecosystem."

## 🔧 Features

- Continuous real-time scanning using your Wi-Fi adapter
- Intelligent device classification (new, ambient, recurring) 
- Logs SSID, MAC, frequency, signal, heat score, and more
- Outputs to CSV for analysis and visualization
- Vendor and device name guessing via MAC
- Future: 3D visualization powered by OpenGL

## 📁 Project Structure

```
wifi_ecology_project/
├── scripts/
│   └── collector.py        # Real-time Wi-Fi scanner and logger
├── data/
│   └── wifi_scans.csv      # Collected scan results
├── utils/
│   └── vendor_lookup.py    # MAC vendor lookup stub
├── visuals/  
│   └── explorer.py         # OpenGL-based visual interface (TBD)
├── requirements.txt
├── .gitignore
└── README.md
```

## 🚀 Getting Started

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the collector:
   ```
   python scripts/collector.py 
   ```

3. Visual exploration coming soon...

✅ Confirm when ready for the final baseline file (`requirements.txt`).
