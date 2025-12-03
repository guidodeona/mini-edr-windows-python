import os
import time
from utils.alertas import print_alert
from utils.helpers import hash_file

def scan_files(config, collect_alerts=False):
    leves = []
    criticas = []

    if not config["file_scanner"]["enabled"]:
        return {"leves": leves, "criticas": criticas}

    print_alert("🔍 Escaneando archivos...", "info")
    for path in config["file_scanner"]["watch_paths"]:
        if os.path.exists(path):
            for root, dirs, files in os.walk(path):
                for file in files:
                    ext = os.path.splitext(file)[1].lower()
                    if ext in config["file_scanner"]["dangerous_extensions"]:
                        filepath = os.path.join(root, file)
                        h = hash_file(filepath)
                        msg = f"Archivo sospechoso: {filepath} (SHA256: {h})"
                        print_alert(f"[ALERTA] {msg}", "danger")
                        if collect_alerts:
                            criticas.append(msg)
    # time.sleep(config["file_scanner"]["interval"]) <-- Eliminado
    return {"leves": leves, "criticas": criticas}
