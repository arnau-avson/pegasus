# Pegasus Project

## Descripción
El proyecto Pegasus contiene herramientas para interactuar con dispositivos Android a través de ADB (Android Debug Bridge). Estas herramientas permiten monitorear aplicaciones activas, capturar pantallas y registrar toques en la pantalla.

## Estructura del Proyecto

- **app_watcher.py**: Monitorea la aplicación activa en un dispositivo Android conectado y muestra cambios en tiempo real.
- **capture_screen.py**: Captura pantallas del dispositivo Android conectado y las guarda en un directorio organizado por fecha y hora.
- **touch_recorder.py**: Registra los toques en la pantalla del dispositivo Android y los guarda en un archivo CSV con coordenadas y marcas de tiempo.
- **requirements.txt**: Lista de dependencias necesarias para ejecutar las herramientas.
- **toques_20251231_104309.csv**: Ejemplo de archivo generado por `touch_recorder.py` que contiene los toques registrados.

## Requisitos

- Python 3.6 o superior
- ADB (Android Debug Bridge) instalado y configurado en el PATH del sistema
- Dependencias adicionales (instalables con pip):
  ```
  pip install -r requirements.txt
  ```

## Uso

### 1. Monitorear aplicaciones activas
Ejecuta el script `app_watcher.py` para monitorear la aplicación activa en el dispositivo Android conectado:
```
python app_watcher.py
```

### 2. Capturar pantallas
Ejecuta el script `capture_screen.py` para capturar pantallas del dispositivo Android conectado:
```
python capture_screen.py
```

### 3. Registrar toques en la pantalla
Ejecuta el script `touch_recorder.py` para registrar los toques en la pantalla del dispositivo Android conectado:
```
python touch_recorder.py
```

## Notas
- Asegúrate de que la depuración USB esté habilitada en tu dispositivo Android.
- Verifica que el dispositivo esté correctamente conectado y reconocido por ADB.

## Licencia
Este proyecto está bajo la licencia MIT.