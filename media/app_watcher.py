import subprocess
import time
import datetime
import re
import csv

def get_foreground_app():
    try:
        result = subprocess.run(
            ["adb", "shell", "dumpsys", "window"],
            capture_output=True,
            text=True,
            timeout=3
        )

        for line in result.stdout.splitlines():
            if "mCurrentFocus" in line or "mFocusedApp" in line:
                match = re.search(r'([a-zA-Z0-9_.]+\/[a-zA-Z0-9_.\$]+)', line)
                if match:
                    return match.group(1)

        return None

    except Exception:
        return None


# 📄 CSV
timestamp_file = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
csv_file = f"apps_activas_{timestamp_file}.csv"

with open(csv_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Nº", "Hora", "App"])

print("📱 Monitor de aplicación activa")
print(f"💾 Guardando en: {csv_file}")
print("⏹️  Ctrl+C para detener\n")

last_app = None
counter = 0

try:
    while True:
        current_app = get_foreground_app()

        if current_app and current_app != last_app:
            counter += 1
            timestamp = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]

            print(f"[{timestamp}] 🔍 App activa: {current_app}")

            with open(csv_file, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([counter, timestamp, current_app])

            last_app = current_app

        time.sleep(0.5)

except KeyboardInterrupt:
    print(f"\n✅ Monitor detenido")
    print(f"📊 Total de cambios registrados: {counter}")
    print(f"💾 Archivo: {csv_file}")
