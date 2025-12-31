import subprocess
import csv
import datetime
import re
import requests

EVENT_DEVICE = "/dev/input/event2"  # CAMBIA ESTO

timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
csv_file = f"toques_{timestamp}.csv"
API_URL = "http://localhost:8000/api/all"

print("🎯 Grabando toques reales (pantalla)")
print("👉 Toca la PANTALLA (no el teclado)")
print("⏹️ Ctrl+C para terminar\n")

with open(csv_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Nº", "Hora", "X", "Y"])

count = 0
x = y = None

try:
    proc = subprocess.Popen(
        ["adb", "shell", "getevent", "-lt", EVENT_DEVICE],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
        bufsize=1
    )

    for line in proc.stdout:
        if "ABS_MT_POSITION_X" in line:
            x = int(line.split()[-1], 16)
        elif "ABS_MT_POSITION_Y" in line:
            y = int(line.split()[-1], 16)

        if x is not None and y is not None:
            count += 1
            time = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]

            # Send touch data to API
            data = {
                "type": "touch",
                "timestamp": time,
                "x": x,
                "y": y
            }
            try:
                requests.post(API_URL, json=data)
            except requests.exceptions.RequestException as e:
                print(f"Error sending touch data to API: {e}")

            with open(csv_file, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([count, time, x, y])

            print(f"[{count}] 📍 X={x} Y={y}")
            x = y = None

except KeyboardInterrupt:
    print(f"\n✅ Capturados {count} toques reales")
    print(f"💾 Guardado en: {csv_file}")
