import socket
import time
from utils.alertas import print_alert

def scan_network(config, collect_alerts=False):
    leves = []
    criticas = []

    if not config["network_scanner"]["enabled"]:
        return {"leves": leves, "criticas": criticas}

    print_alert("🔍 Escaneando puertos...", "info")
    for port in config["network_scanner"]["watch_ports"]:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)
            result = s.connect_ex(('127.0.0.1', port))
            if result == 0:
                msg = f"Puerto abierto detectado: {port}"
                print_alert(f"[ALERTA] {msg}", "warning")
                if collect_alerts:
                    leves.append(msg)
            s.close()
        except:
            continue
    time.sleep(config["network_scanner"]["interval"])
    return {"leves": leves, "criticas": criticas}
