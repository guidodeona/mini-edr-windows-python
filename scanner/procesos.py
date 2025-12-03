import psutil
import time
from utils.alertas import print_alert

def scan_processes(config, collect_alerts=False):
    leves = []
    criticas = []

    if not config["process_scanner"]["enabled"]:
        return {"leves": leves, "criticas": criticas}

    print_alert("🔍 Escaneando procesos...", "info")
    for proc in psutil.process_iter(['pid','name','exe','cpu_percent','memory_percent']):
        try:
            nombre = proc.info['name'].lower()
            ruta = str(proc.info['exe']).lower() if proc.info['exe'] else ""

            # Sospechoso
            if nombre in [x.lower() for x in config["process_scanner"]["suspicious_names"]]:
                msg = f"Proceso sospechoso: {proc.info['name']} (PID {proc.info['pid']})"
                print_alert(f"[ALERTA] {msg}", "danger")
                if collect_alerts:
                    criticas.append(msg)
            # Alto CPU/RAM
            if proc.info['cpu_percent'] > 50 or proc.info['memory_percent'] > 50:
                msg = f"Proceso con alto consumo: {proc.info['name']}"
                print_alert(f"[ALERTA] {msg}", "warning")
                if collect_alerts:
                    leves.append(msg)
            # Rutas sospechosas
            if "temp" in ruta or "appdata" in ruta:
                msg = f"Proceso ejecutado desde ruta sospechosa: {ruta}"
                print_alert(f"[ALERTA] {msg}", "warning")
                if collect_alerts:
                    leves.append(msg)

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    # time.sleep(config["process_scanner"]["interval"])  <-- Eliminado para no bloquear el monitor
    return {"leves": leves, "criticas": criticas}
