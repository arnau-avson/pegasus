import subprocess
import time
import datetime
import re

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
                # Buscar algo tipo com.whatsapp/.Main
                match = re.search(r'([a-zA-Z0-9_.]+\/[a-zA-Z0-9_.\$]+)', line)
                if match:
                    return match.group(1)

        return None

    except Exception:
        return None


print("📱 Monitor de aplicación activa")
print("⏹️  Ctrl+C para detener\n")

last_app = None

try:
    while True:
        current_app = get_foreground_app()

        if current_app and current_app != last_app:
            timestamp = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
            print(f"[{timestamp}] 🔍 App activa: {current_app}")
            last_app = current_app

        time.sleep(0.5)

except KeyboardInterrupt:
    print("\n✅ Monitor detenido")
