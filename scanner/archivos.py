import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from utils.alertas import print_alert
from utils.helpers import hash_file
from utils.quarantine import quarantine_file

try:
    import yara
    YARA_AVAILABLE = True
except ImportError:
    YARA_AVAILABLE = False
    print_alert("⚠️ YARA no está instalado. Corriendo sin análisis avanzado.", "warning")

# Variable global para comunicar alertas al Dashboard
latest_file_alert = None

# Variable global para reglas YARA compiladas
yara_rules = None

def load_yara_rules(rules_path):
    """Carga y compila las reglas YARA."""
    global yara_rules
    
    if not YARA_AVAILABLE:
        return False
    
    if not os.path.exists(rules_path):
        print_alert(f"⚠️ Archivo de reglas YARA no encontrado: {rules_path}", "warning")
        return False
    
    try:
        yara_rules = yara.compile(filepath=rules_path)
        print_alert(f"✅ Reglas YARA cargadas desde: {rules_path}", "success")
        return True
    except Exception as e:
        print_alert(f"❌ Error al cargar reglas YARA: {e}", "danger")
        return False

def scan_file_with_yara(filepath):
    """
    Escanea un archivo con YARA.
    Retorna una lista de reglas que coincidieron.
    """
    if not YARA_AVAILABLE or yara_rules is None:
        return []
    
    try:
        matches = yara_rules.match(filepath)
        return matches
    except Exception as e:
        # Archivo puede estar bloqueado o ser inaccesible
        return []

class FileEventHandler(FileSystemEventHandler):
    def __init__(self, config):
        self.config = config
        self.dangerous_extensions = config["file_scanner"]["dangerous_extensions"]
        self.auto_quarantine = config["file_scanner"].get("auto_quarantine", False)
        self.quarantine_folder = config["file_scanner"].get("quarantine_folder", "quarantine")

    def on_created(self, event):
        global latest_file_alert
        if event.is_directory:
            return
        
        filepath = event.src_path
        ext = os.path.splitext(filepath)[1].lower()
        is_dangerous = False
        threat_type = ""
        
        # 1. Verificar extensión peligrosa
        if ext in self.dangerous_extensions:
            is_dangerous = True
            threat_type = f"Extensión peligrosa: {ext}"
        
        # 2. Escanear con YARA
        yara_matches = scan_file_with_yara(filepath)
        if yara_matches:
            is_dangerous = True
            matched_rules = [match.rule for match in yara_matches]
            threat_type = f"YARA: {', '.join(matched_rules)}"
        
        if is_dangerous:
            msg = f"¡AMENAZA DETECTADA!: {filepath} ({threat_type})"
            print_alert(f"[ALERTA REAL-TIME] {msg}", "danger")
            latest_file_alert = msg
            
            # Cuarentena automática
            if self.auto_quarantine:
                quarantine_file(filepath, self.quarantine_folder)
                latest_file_alert = f"🔒 CUARENTENA: {filepath}"

    def on_modified(self, event):
        global latest_file_alert
        if event.is_directory:
            return
        
        filepath = event.src_path
        ext = os.path.splitext(filepath)[1].lower()
        
        # Solo verificar modificaciones de archivos sospechosos
        if ext in self.dangerous_extensions:
            yara_matches = scan_file_with_yara(filepath)
            if yara_matches:
                matched_rules = [match.rule for match in yara_matches]
                msg = f"Archivo modificado con YARA match: {filepath} ({', '.join(matched_rules)})"
                print_alert(f"[ALERTA REAL-TIME] {msg}", "warning")
                latest_file_alert = msg

def start_file_monitor(config):
    """Inicia el monitoreo en tiempo real en un hilo separado."""
    # Cargar reglas YARA
    yara_path = config["file_scanner"].get("yara_rules_path", "rules/malware.yar")
    load_yara_rules(yara_path)
    
    event_handler = FileEventHandler(config)
    observer = Observer()
    
    paths_monitored = 0
    for path in config["file_scanner"]["watch_paths"]:
        if os.path.exists(path):
            observer.schedule(event_handler, path, recursive=True)
            paths_monitored += 1
    
    if paths_monitored > 0:
        observer.start()
        print_alert(f"👀 Monitoreo en tiempo real activo en {paths_monitored} directorios.", "success")
        return observer
    else:
        print_alert("⚠️ No se encontraron directorios para monitorear.", "warning")
        return None

def scan_files(config, collect_alerts=False):
    leves = []
    criticas = []

    if not config["file_scanner"]["enabled"]:
        return {"leves": leves, "criticas": criticas}

    # Cargar reglas YARA si no están cargadas
    if yara_rules is None and YARA_AVAILABLE:
        yara_path = config["file_scanner"].get("yara_rules_path", "rules/malware.yar")
        load_yara_rules(yara_path)

    auto_quarantine = config["file_scanner"].get("auto_quarantine", False)
    quarantine_folder = config["file_scanner"].get("quarantine_folder", "quarantine")

    print_alert("🔍 Escaneando archivos (Estático + YARA)...", "info")
    
    for path in config["file_scanner"]["watch_paths"]:
        if os.path.exists(path):
            for root, dirs, files in os.walk(path):
                for file in files:
                    filepath = os.path.join(root, file)
                    ext = os.path.splitext(file)[1].lower()
                    is_dangerous = False
                    threat_info = ""
                    
                    # 1. Verificar extensión
                    if ext in config["file_scanner"]["dangerous_extensions"]:
                        is_dangerous = True
                        threat_info = f"Extensión: {ext}"
                    
                    # 2. Escanear con YARA
                    yara_matches = scan_file_with_yara(filepath)
                    if yara_matches:
                        is_dangerous = True
                        matched_rules = [match.rule for match in yara_matches]
                        threat_info += f" | YARA: {', '.join(matched_rules)}"
                    
                    if is_dangerous:
                        msg = f"Amenaza encontrada: {filepath} ({threat_info})"
                        print_alert(f"[ALERTA] {msg}", "danger")
                        
                        if collect_alerts:
                            criticas.append(msg)
                        
                        # Cuarentena automática
                        if auto_quarantine:
                            quarantine_file(filepath, quarantine_folder)
    
    return {"leves": leves, "criticas": criticas}

