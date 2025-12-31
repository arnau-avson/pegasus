import subprocess
import sys
import time

scripts = [
    "app_watcher.py",
    "capture_screen.py",
    "touch_recorder.py"
]

processes = []

print("🚀 Iniciando monitorización completa")
print("📱 App watcher")
print("📸 Screen capture")
print("🎯 Touch recorder")
print("⏹️  Ctrl+C para detener todo\n")

try:
    for script in scripts:
        proc = subprocess.Popen(
            [sys.executable, script],
            stdout=None,
            stderr=None
        )
        processes.append(proc)
        time.sleep(0.5)  # pequeño delay para evitar colisiones

    # Mantener el main vivo
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("\n🛑 Deteniendo todos los procesos...")

    for proc in processes:
        proc.terminate()

    for proc in processes:
        proc.wait()

    print("✅ Todo detenido correctamente")
