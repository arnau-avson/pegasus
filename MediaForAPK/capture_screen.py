import os
import time
import subprocess
import datetime
from pathlib import Path
import sys
import requests

def check_adb_connection():
    try:
        result = subprocess.run(['adb', 'devices'], capture_output=True, text=True, timeout=10)  # Aumentado de 5 a 10 segundos
        devices = [line for line in result.stdout.split('\n') if '\tdevice' in line]
        
        if not devices:
            print("❌ No se encontraron dispositivos Android conectados.")
            print("\nSolución de problemas:")
            print("1. Asegúrate de tener habilitada la 'Depuración USB' en tu dispositivo")
            print("2. Verifica que el cable USB esté funcionando correctamente")
            print("3. Reinstala los drivers USB de tu dispositivo si es necesario")
            return False
        
        print(f"✅ Dispositivo conectado: {len(devices)} encontrado(s)")
        for device in devices:
            print(f"   - {device.split('\t')[0]}")
        return True
        
    except FileNotFoundError:
        print("❌ ADB no está instalado o no está en el PATH")
        print("\nPara instalar ADB:")
        print("1. Windows: Descarga Android SDK Platform Tools")
        print("2. macOS: 'brew install android-platform-tools'")
        print("3. Linux: 'sudo apt-get install android-tools-adb'")
        return False
    except subprocess.TimeoutExpired:
        print("❌ Tiempo de espera agotado al buscar dispositivos")
        return False

def create_screenshot_directory():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    folder_name = f"screenshots_{timestamp}"
    
    screenshots_dir = Path.cwd() / folder_name
    screenshots_dir.mkdir(exist_ok=True)
    
    print(f"📁 Las capturas se guardarán en: {screenshots_dir}")
    return screenshots_dir

API_URL = "http://localhost:8000/upload"

def take_screenshot(device_id, save_path, counter):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = save_path / f"screenshot_{counter:04d}_{timestamp}.png"
    
    try:
        if device_id:
            cmd = ['adb', '-s', device_id, 'shell', 'screencap', '-p', '/sdcard/screenshot.png']
            pull_cmd = ['adb', '-s', device_id, 'pull', '/sdcard/screenshot.png', str(filename)]
        else:
            cmd = ['adb', 'shell', 'screencap', '-p', '/sdcard/screenshot.png']
            pull_cmd = ['adb', 'pull', '/sdcard/screenshot.png', str(filename)]
        
        subprocess.run(cmd, capture_output=True, timeout=10)
        subprocess.run(pull_cmd, capture_output=True, timeout=10)
        
        if filename.exists():
            print(f"📸 Captura {counter} guardada: {filename.name}")
            
            # Send screenshot data to API
            with open(filename, "rb") as image_file:
                try:
                    requests.post(API_URL, files={"image": image_file}, data={"type": "screenshot", "timestamp": timestamp})
                except requests.exceptions.RequestException as e:
                    print(f"Error sending screenshot to API: {e}")
            
            return True
        else:
            print(f"❌ Error al guardar captura {counter}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"❌ Tiempo de espera agotado al tomar captura {counter}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado al tomar captura {counter}: {str(e)}")
        return False

def get_device_id():
    try:
        result = subprocess.run(['adb', 'devices'], capture_output=True, text=True, timeout=5)
        for line in result.stdout.split('\n'):
            if '\tdevice' in line:
                return line.split('\t')[0]
    except:
        pass
    return None

def main():
    print("=" * 50)
    print("CAPTURADOR DE PANTALLA PARA DISPOSITIVOS MÓVILES")
    print("=" * 50)
    
    if not check_adb_connection():
        input("\nPresiona Enter para salir...")
        sys.exit(1)
    
    screenshots_dir = create_screenshot_directory()
    
    device_id = get_device_id()
    
    try:
        interval = 2  # segundos
        print(f"\n⏰ Intervalo de captura: {interval} segundos")
        print("⚠️  Asegúrate de que la pantalla del dispositivo esté encendida")
        print("\nPresiona Ctrl+C para detener la captura\n")
        
        counter = 1
        start_time = time.time()
        
        while True:
            take_screenshot(device_id, screenshots_dir, counter)
            
            time.sleep(interval)
            counter += 1
            
    except KeyboardInterrupt:
        elapsed_time = time.time() - start_time
        print(f"\n\n✅ Captura detenida por el usuario")
        print(f"📊 Total de capturas tomadas: {counter-1}")
        print(f"⏱️  Tiempo total: {elapsed_time:.1f} segundos")
        print(f"📁 Capturas guardadas en: {screenshots_dir}")
        
        if sys.platform == "win32":
            os.startfile(screenshots_dir)
        elif sys.platform == "darwin":
            subprocess.run(["open", screenshots_dir])
        else:
            subprocess.run(["xdg-open", screenshots_dir])
            
    except Exception as e:
        print(f"\n❌ Error inesperado: {str(e)}")

if __name__ == "__main__":
    main()