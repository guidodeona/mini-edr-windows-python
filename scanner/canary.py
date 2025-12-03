import os
from utils.alertas import print_alert

CANARY_FILE = "C:\\Users\\Public\\passwords.txt"
CANARY_CONTENT = "This is a honeyfile. Do not touch."

def setup_canary(path):
    if not os.path.exists(path):
        try:
            with open(path, "w") as f:
                f.write(CANARY_CONTENT)
        except Exception as e:
            print_alert(f"[ERROR] No se pudo crear el honeyfile en {path}: {e}", "danger")

def scan_canary(config, collect_alerts=False):
    leves = []
    criticas = []
    
    canary_path = config.get("canary_path", "C:\\Users\\Public\\passwords.txt")
    
    # Ensure canary exists
    setup_canary(canary_path)

    try:
        with open(canary_path, "r") as f:
            content = f.read()
            
        if content != CANARY_CONTENT:
            msg = f"¡HONEYFILE MODIFICADO! Posible actividad de RANSOMWARE en {canary_path}"
            print_alert(f"[ALERTA CRÍTICA] {msg}", "danger")
            if collect_alerts:
                criticas.append(msg)
                
    except Exception as e:
        msg = f"No se pudo leer el honeyfile: {e}"
        print_alert(f"[ALERTA] {msg}", "warning")
        if collect_alerts:
            leves.append(msg)

    return {"leves": leves, "criticas": criticas}
