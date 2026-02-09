import psutil
import time
from utils.alertas import print_alert
from utils.database import db
from utils.process_killer import killer

def scan_processes(config, collect_alerts=False):
    leves = []
    criticas = []

    if not config["process_scanner"]["enabled"]:
        return {"leves": leves, "criticas": criticas}

    print_alert("🔍 Escaneando procesos...", "info")
    
    auto_kill = config["process_scanner"].get("auto_kill", False)
    kill_on_high_cpu = config["process_scanner"].get("kill_on_high_cpu", False)
    cpu_threshold = config["process_scanner"].get("cpu_threshold", 80)
    
    for proc in psutil.process_iter(['pid','name','exe','cpu_percent','memory_percent']):
        try:
            nombre = proc.info['name'].lower()
            ruta = str(proc.info['exe']).lower() if proc.info['exe'] else ""
            pid = proc.info['pid']
            cpu = proc.info['cpu_percent']
            mem = proc.info['memory_percent']

            # Proceso sospechoso por nombre
            if nombre in [x.lower() for x in config["process_scanner"]["suspicious_names"]]:
                msg = f"Proceso sospechoso: {proc.info['name']} (PID {pid})"
                print_alert(f"[ALERTA] {msg}", "danger")
                
                # Registrar en base de datos
                db.log_event(
                    event_type="SUSPICIOUS_PROCESS",
                    severity="CRITICAL",
                    module="ProcessScanner",
                    description=msg,
                    details={"pid": pid, "name": proc.info['name'], "path": ruta}
                )
                
                if collect_alerts:
                    criticas.append(msg)
                
                # Auto-kill si está habilitado
                if auto_kill:
                    killer.kill_process(pid, proc.info['name'], reason="Proceso en lista negra")
            
            # Alto CPU/RAM
            if cpu > 50 or mem > 50:
                msg = f"Proceso con alto consumo: {proc.info['name']} (CPU: {cpu}%, RAM: {mem}%)"
                print_alert(f"[ALERTA] {msg}", "warning")
                
                db.log_event(
                    event_type="HIGH_RESOURCE_USAGE",
                    severity="WARNING",
                    module="ProcessScanner",
                    description=msg,
                    details={"pid": pid, "name": proc.info['name'], "cpu": cpu, "memory": mem}
                )
                
                if collect_alerts:
                    leves.append(msg)
                
                # Kill si CPU excede threshold
                if kill_on_high_cpu and cpu > cpu_threshold:
                    killer.kill_process(pid, proc.info['name'], reason=f"CPU > {cpu_threshold}%")
            
            # Rutas sospechosas
            if "temp" in ruta or "appdata" in ruta:
                msg = f"Proceso ejecutado desde ruta sospechosa: {ruta}"
                print_alert(f"[ALERTA] {msg}", "warning")
                
                db.log_event(
                    event_type="SUSPICIOUS_PATH",
                    severity="WARNING",
                    module="ProcessScanner",
                    description=msg,
                    details={"pid": pid, "name": proc.info['name'], "path": ruta}
                )
                
                if collect_alerts:
                    leves.append(msg)

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    
    return {"leves": leves, "criticas": criticas}

