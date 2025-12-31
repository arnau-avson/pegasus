# Guía para Actualizar el Código de la APK

Esta guía describe los pasos necesarios para realizar cambios en el código de la APK y actualizarla correctamente.

---

## 1. **Ficheros Principales**

Los ficheros clave que puedes necesitar modificar son:

- **`app_watcher.py`**: 
  - Cambios relacionados con la detección de la aplicación activa.
  - Modificar el endpoint de la API o la lógica de monitoreo.

- **`capture_screen.py`**:
  - Cambios en la lógica de captura de pantalla (frecuencia, formato, etc.).
  - Modificar el envío de capturas al servidor.

- **`touch_recorder.py`**:
  - Cambios en la lógica de registro de toques en la pantalla.
  - Ajustar el dispositivo de eventos o el formato de los datos enviados.

- **`main.py`**:
  - Cambios en la coordinación de los procesos.
  - Añadir o eliminar scripts que se ejecutan al iniciar la APK.

---

## 2. **Pasos para Actualizar el Código**

1. **Realiza los Cambios Necesarios**:
   - Edita los ficheros mencionados según los cambios que necesites.

2. **Prueba el Código Localmente**:
   - Ejecuta los scripts en tu entorno local para asegurarte de que funcionan correctamente.
   - Usa el siguiente comando para probar un script específico:
     ```bash
     python nombre_del_script.py
     ```

3. **Empaqueta la APK**:
   - Asegúrate de estar en el directorio del proyecto BeeWare:
     ```bash
     cd ApkArnau
     ```
   - Construye la APK:
     ```bash
     briefcase build android
     ```
   - Empaqueta la APK:
     ```bash
     briefcase package android
     ```

4. **Instala y Prueba la APK**:
   - Instala la APK generada en tu dispositivo móvil.
   - Verifica que los cambios funcionan como se espera.

---

## 3. **Notas Importantes**

- **Permisos**: Si agregas nuevas funcionalidades que requieren permisos adicionales (como acceso a la cámara o ubicación), actualiza el archivo `AndroidManifest.xml`.
- **Dependencias**: Si agregas nuevas librerías, asegúrate de incluirlas en el entorno y probarlas antes de empaquetar.
- **Endpoint de la API**: Si cambias el servidor o el endpoint, actualiza todos los scripts que lo utilicen.

---

## 4. **Contacto**

Si encuentras problemas o necesitas ayuda, revisa la documentación de BeeWare o contacta con el desarrollador principal.