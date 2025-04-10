# collector.py - Wi-Fi Analyzer using nmcli + rich table (autofit + ellipsis)

import subprocess
import csv
import os
import time
from datetime import datetime, timezone
from utils.vendor_lookup import get_vendor
import pandas as pd
from rich.console import Console
from rich.table import Table
from rich import box

CSV_PATH = os.path.expanduser("~/wifi_ecology_project/data/wifi_scans.csv")
INTERFACE = "wlx347de44ff463"
SCAN_INTERVAL = 10  # seconds

HEADERS = [
    "timestamp", "mac_address", "ssid", "freq", "signal",
    "vendor_name", "guessed_name", "first_seen", "last_seen",
    "seen_count", "num_disconnects", "avg_connection_duration",
    "mobility_score", "heat_score"
]

device_memory = {}
console = Console()

def ensure_csv_exists():
    if not os.path.exists(CSV_PATH):
        with open(CSV_PATH, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(HEADERS)

def guess_device_name(ssid):
    if "iPhone" in ssid:
        return "Apple iPhone"
    elif "Galaxy" in ssid:
        return "Samsung Galaxy"
    elif "Pixel" in ssid:
        return "Google Pixel"
    elif "'s" in ssid:
        return ssid.split("'")[0] + "'s Device"
    return "Unknown Device"

def scan_wifi():
    try:
        result = subprocess.run(
            ["nmcli", "-t", "-f", "SSID,BSSID,FREQ,SIGNAL", "device", "wifi", "list", "ifname", INTERFACE],
            capture_output=True, text=True, check=True
        )
        return result.stdout.strip().split("\n")
    except subprocess.CalledProcessError:
        return []

def log_scan():
    timestamp = datetime.now(timezone.utc).isoformat()
    rows = []

    for line in scan_wifi():
        parts = line.rsplit(":", 3)
        if len(parts) != 4:
            continue
        ssid, bssid, freq, signal = parts
        ssid = ssid or "Hidden"
        mac = bssid.upper()
        freq = freq.strip()
        signal = signal.strip()
        guessed_name = guess_device_name(ssid)
        vendor_name = get_vendor(mac)

        now_epoch = time.time()
        first_seen = timestamp
        last_seen = timestamp
        seen_count = "1"
        num_disconnects = "0"
        avg_connection_duration = "0"
        mobility_score = "0"
        heat_score = "1"

        if mac in device_memory:
            mem = device_memory[mac]
            seen_count = str(int(mem["seen_count"]) + 1)
            first_seen = mem["first_seen"]
            avg_connection_duration = str(round((now_epoch - mem["first_seen_epoch"]) / int(seen_count), 2))
            heat_score = str(round(max(0, min(1, (1 / (1 + int(seen_count))))), 3))
            mem["seen_count"] = seen_count
            mem["last_seen"] = timestamp
        else:
            device_memory[mac] = {
                "first_seen": timestamp,
                "first_seen_epoch": now_epoch,
                "last_seen": timestamp,
                "seen_count": seen_count
            }

        rows.append([
            timestamp, mac, ssid, freq, signal,
            vendor_name, guessed_name,
            first_seen, last_seen, seen_count,
            num_disconnects, avg_connection_duration,
            mobility_score, heat_score
        ])

    with open(CSV_PATH, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    # 🖼️ Display clean table with autofit + ellipsis
    try:
        df = pd.read_csv(CSV_PATH)
        recent_df = df.tail(75)
        table = Table(show_header=True, header_style="bold cyan", box=box.SIMPLE_HEAVY)
        for col in recent_df.columns:
            table.add_column(col, max_width=20, overflow="ellipsis", no_wrap=True)
        for _, row in recent_df.iterrows():
            table.add_row(*[str(row[col]) if len(str(row[col])) <= 20 else str(row[col])[:17] + "..." for col in recent_df.columns])
        console.clear()
        console.print(table)
    except Exception as e:
        console.print(f"[red]Error displaying table:[/red] {e}")

if __name__ == "__main__":
    ensure_csv_exists()
    try:
        while True:
            log_scan()
            time.sleep(SCAN_INTERVAL)
    except KeyboardInterrupt:
        print("\nScan stopped.")
