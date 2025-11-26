# Mini-EDR en Python para Windows 🛡️

## Descripción
Asistente de ciberseguridad en Python para Windows que realiza escaneo completo del sistema, detectando:

- Procesos y servicios sospechosos  
- Archivos peligrosos  
- Puertos abiertos  
- Drivers instalados  
- Estado del firewall  
- Tareas programadas  

Genera **informes automáticos** con alertas leves y críticas.

---

## Funcionalidades

1. Escaneo de procesos  
2. Escaneo de archivos  
3. Escaneo de red  
4. Escaneo del sistema (servicios, drivers, firewall, tareas)  
5. Informes automáticos en `logs/informe_YYYYMMDD_HHMMSS.txt`

---

## Instalación

```bash
git clone https://github.com/TU_USUARIO/mini-edr-windows-python.git
cd mini-edr-windows-python
pip install psutil pywin32
