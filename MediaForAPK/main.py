import os
import subprocess
import sys
import time

# Scripts to be executed
scripts = [
    "app_watcher.py",
    "capture_screen.py",
    "touch_recorder.py"
]

processes = []

def start_processes():
    print("🚀 Starting monitoring processes")
    print("📱 App watcher")
    print("📸 Screen capture")
    print("🎯 Touch recorder")
    print("⏹️  Ctrl+C to stop everything\n")

    try:
        for script in scripts:
            proc = subprocess.Popen(
                [sys.executable, script],
                stdout=None,
                stderr=None
            )
            processes.append(proc)
            time.sleep(0.5)  # Small delay to avoid collisions

        # Keep the main script alive
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n🛑 Stopping all processes...")

        for proc in processes:
            proc.terminate()

        for proc in processes:
            proc.wait()

        print("✅ All processes stopped successfully")

if __name__ == "__main__":
    start_processes()
