import subprocess
import datetime
import csv
from pathlib import Path
from PIL import Image, ImageDraw
import io
import threading

def check_adb_connection():
    result = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
    devices = [line for line in result.stdout.split('\n') if '\tdevice' in line]
    return len(devices) > 0

def get_screen_resolution():
    """Obtiene la resolución de la pantalla del dispositivo"""
    result = subprocess.run(['adb', 'shell', 'wm', 'size'], capture_output=True, text=True)
    size_line = result.stdout.strip()
    if 'Physical size:' in size_line:
        size = size_line.split(': ')[1]
        width, height = map(int, size.split('x'))
        return width, height
    return None, None

def get_touch_event_max_values():
    """Obtiene los valores máximos del evento táctil"""
    result = subprocess.run(['adb', 'shell', 'getevent', '-p'], capture_output=True, text=True)
    max_x, max_y = None, None
    
    lines = result.stdout.split('\n')
    
    for line in lines:
        if 'ABS_MT_POSITION_X' in line or '0035' in line:
            if 'max' in line:
                try:
                    parts = line.split('max')
                    if len(parts) > 1:
                        max_val = parts[1].split(',')[0].strip()
                        max_x = int(max_val)
                except:
                    pass
        
        if 'ABS_MT_POSITION_Y' in line or '0036' in line:
            if 'max' in line:
                try:
                    parts = line.split('max')
                    if len(parts) > 1:
                        max_val = parts[1].split(',')[0].strip()
                        max_y = int(max_val)
                except:
                    pass
    
    if not max_x or not max_y:
        result = subprocess.run(['adb', 'shell', 'getevent', '-lp', '/dev/input/event2'], 
                               capture_output=True, text=True)
        
        for line in result.stdout.split('\n'):
            if '0035' in line:
                try:
                    max_x = int(line.split('max')[1].split(',')[0].strip(), 16)
                except:
                    pass
            if '0036' in line:
                try:
                    max_y = int(line.split('max')[1].split(',')[0].strip(), 16)
                except:
                    pass
    
    return max_x, max_y

def capture_screenshot_bytes():
    """Captura la pantalla y devuelve los bytes directamente"""
    try:
        result = subprocess.run(['adb', 'exec-out', 'screencap', '-p'], 
                               capture_output=True, 
                               timeout=2)
        if result.returncode == 0:
            return result.stdout
        return None
    except:
        return None

def save_screenshot_with_point(screenshot_bytes, x, y, save_path):
    """Guarda la captura con el punto dibujado"""
    try:
        # Carga la imagen desde memoria
        image = Image.open(io.BytesIO(screenshot_bytes))
        
        # Dibuja el punto rojo
        draw = ImageDraw.Draw(image)
        radius = 8
        draw.ellipse((x-radius, y-radius, x+radius, y+radius), 
                     fill="red", outline="red")
        
        # Guarda la imagen
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
        filename = save_path / f"screenshot_{timestamp}.png"
        image.save(filename)
        
        return filename
    except Exception as e:
        print(f"   ✗ Error al guardar: {e}")
        return None

def record_touch_coordinates(save_path, csv_file, screen_width, screen_height, max_x, max_y):
    """Registra las coordenadas de los toques"""
    EVENT_DEVICE = "/dev/input/event2"
    
    print(f"\n🎯 Configuración:")
    print(f"   Pantalla: {screen_width}x{screen_height}")
    if max_x and max_y:
        print(f"   Touch range: {max_x}x{max_y}")
        print(f"   Factor escala: X={screen_width/max_x:.4f}, Y={screen_height/max_y:.4f}")
    
    print(f"\n👆 Toca la pantalla del dispositivo... (Ctrl+C para detener)\n")
    
    proc = subprocess.Popen(
        ["adb", "shell", "getevent", "-lt", EVENT_DEVICE],
        stdout=subprocess.PIPE, 
        text=True,
        bufsize=1
    )
    
    x, y = None, None
    screenshot_bytes = None
    touch_started = False
    
    try:
        for line in proc.stdout:
            line = line.strip()
            
            # Cuando detectamos DOWN, capturamos la pantalla INMEDIATAMENTE
            if "BTN_TOUCH" in line and "DOWN" in line:
                touch_started = True
                x, y = None, None
                # Captura inmediata en el momento del toque
                print("📸 Capturando...", end=" ", flush=True)
                screenshot_bytes = capture_screenshot_bytes()
            
            # Capturamos las coordenadas
            if "ABS_MT_POSITION_X" in line and touch_started:
                try:
                    x = int(line.split()[-1], 16)
                except ValueError:
                    continue
            
            elif "ABS_MT_POSITION_Y" in line and touch_started:
                try:
                    y = int(line.split()[-1], 16)
                except ValueError:
                    continue
            
            # Cuando se levanta el dedo, procesamos
            if "BTN_TOUCH" in line and "UP" in line and touch_started:
                if x is not None and y is not None and screenshot_bytes is not None:
                    # Escala las coordenadas
                    if max_x and max_y:
                        scaled_x = int((x / max_x) * screen_width)
                        scaled_y = int((y / max_y) * screen_height)
                    else:
                        scaled_x = x
                        scaled_y = y
                    
                    print(f"👆 ({scaled_x}, {scaled_y}) - Guardando...", end=" ", flush=True)
                    
                    # Guarda con el punto dibujado
                    screenshot_path = save_screenshot_with_point(screenshot_bytes, scaled_x, scaled_y, save_path)
                    
                    if screenshot_path:
                        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                        with open(csv_file, 'a', newline='') as f:
                            writer = csv.writer(f)
                            writer.writerow([timestamp, scaled_x, scaled_y, screenshot_path.name])
                        print("✓")
                    else:
                        print("✗")
                elif screenshot_bytes is None:
                    print("✗ No se capturó pantalla")
                else:
                    print("✗ Coordenadas incompletas")
                
                x, y = None, None
                screenshot_bytes = None
                touch_started = False
                    
    except KeyboardInterrupt:
        print("\n\n⏹️  Detenido")
    finally:
        proc.terminate()

def main():
    print("="*60)
    print("  CAPTURA INSTANTÁNEA DE TOQUES")
    print("="*60)
    
    if not check_adb_connection():
        print("\n✗ No hay conexión ADB")
        return

    print("\n✓ Conexión ADB establecida")
    
    screen_width, screen_height = get_screen_resolution()
    max_x, max_y = get_touch_event_max_values()
    
    if not screen_width or not screen_height:
        print("✗ No se pudo obtener la resolución de pantalla")
        return
    
    if not max_x or not max_y:
        print("⚠️  No se detectaron valores máximos del touchscreen")
        print("   Se usarán coordenadas raw\n")
    
    save_path = Path.cwd() / "screenshots"
    save_path.mkdir(exist_ok=True)
    
    csv_file = save_path / "touch_coordinates.csv"
    if not csv_file.exists():
        with open(csv_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Timestamp', 'X', 'Y', 'Screenshot'])
    
    record_touch_coordinates(save_path, csv_file, screen_width, screen_height, max_x, max_y)
    
    print(f"\n✓ Capturas guardadas en: {save_path}")

if __name__ == "__main__":
    main()