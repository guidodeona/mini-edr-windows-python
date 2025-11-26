import win32service
import subprocess
import os
from utils.alertas import print_alert

def scan_system(config, collect_alerts=False):
    leves = []
    criticas = []

    if not config["system_scanner"]["enabled"]:
        return {"leves": leves, "criticas": criticas}

    print_alert("🔍 Escaneando sistema (servicios, drivers, firewall, tareas)...", "info")

    # ------------------------------
    # 1️⃣ Escaneo de servicios
    # ------------------------------
    try:
        services = win32service.EnumServicesStatusEx(None)
        for s in services:
            try:
                nombre = s[0]
                if "malware" in nombre.lower():
                    msg = f"Servicio sospechoso: {nombre}"
                    print_alert(f"[ALERTA] {msg}", "danger")
                    if collect_alerts:
                        criticas.append(msg)
            except Exception:
                continue  # Ignora servicios protegidos
    except Exception:
        print_alert("[INFO] Algunos servicios protegidos no pudieron ser listados, se ignoraron.", "info")

    # ------------------------------
    # 2️⃣ Escaneo de drivers instalados
    # ------------------------------
    try:
        result = subprocess.run(["driverquery"], capture_output=True, text=True)
        lines = result.stdout.splitlines()[2:]  # Ignora encabezado
        for line in lines:
            if "malware" in line.lower() or "unknown" in line.lower():
                msg = f"Driver sospechoso: {line.strip()}"
                print_alert(f"[ALERTA] {msg}", "danger")
                if collect_alerts:
                    criticas.append(msg)
    except Exception:
        print_alert("[INFO] No se pudieron listar algunos drivers.", "info")

    # ------------------------------
    # 3️⃣ Escaneo de firewall (estado y reglas)
    # ------------------------------
    try:
        result = subprocess.run(["netsh", "advfirewall", "show", "allprofiles"], capture_output=True, text=True)
        if "state ON" not in result.stdout.upper():
            msg = "Firewall desactivado en uno o más perfiles"
            print_alert(f"[ALERTA] {msg}", "warning")
            if collect_alerts:
                leves.append(msg)
    except Exception:
        print_alert("[INFO] No se pudo verificar el estado del firewall.", "info")

    # ------------------------------
    # 4️⃣ Escaneo de tareas programadas
    # ------------------------------
    try:
        result = subprocess.run(["schtasks"], capture_output=True, text=True)
        lines = result.stdout.splitlines()[1:]  # Ignora encabezado
        for line in lines:
            if "malware" in line.lower() or "unknown" in line.lower():
                msg = f"Tarea sospechosa: {line.strip()}"
                print_alert(f"[ALERTA] {msg}", "danger")
                if collect_alerts:
                    criticas.append(msg)
    except Exception:
        print_alert("[INFO] No se pudieron listar todas las tareas programadas.", "info")

    return {"leves": leves, "criticas": criticas}
