import os
import shutil
import datetime
from utils.alertas import print_alert

def quarantine_file(filepath, quarantine_folder="quarantine"):
    """
    Mueve un archivo peligroso a la carpeta de cuarentena.
    Retorna True si tuvo éxito, False si falló.
    """
    try:
        # Crear carpeta de cuarentena si no existe
        if not os.path.exists(quarantine_folder):
            os.makedirs(quarantine_folder)
        
        # Generar nombre único con timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.basename(filepath)
        quarantine_path = os.path.join(quarantine_folder, f"{timestamp}_{filename}")
        
        # Mover el archivo
        shutil.move(filepath, quarantine_path)
        
        print_alert(f"🔒 ARCHIVO EN CUARENTENA: {filepath} → {quarantine_path}", "danger")
        return True
        
    except Exception as e:
        print_alert(f"❌ Error al poner en cuarentena {filepath}: {e}", "danger")
        return False

def list_quarantined_files(quarantine_folder="quarantine"):
    """
    Lista todos los archivos en cuarentena.
    """
    if not os.path.exists(quarantine_folder):
        print_alert("No hay archivos en cuarentena.", "info")
        return []
    
    files = os.listdir(quarantine_folder)
    if not files:
        print_alert("No hay archivos en cuarentena.", "info")
    else:
        print_alert(f"\n📂 Archivos en Cuarentena ({len(files)}):", "warning")
        for f in files:
            print(f"  - {f}")
    
    return files

def restore_file(filename, quarantine_folder="quarantine", restore_path=None):
    """
    Restaura un archivo desde la cuarentena.
    Si restore_path es None, intenta extraer la ruta original del nombre.
    """
    quarantine_path = os.path.join(quarantine_folder, filename)
    
    if not os.path.exists(quarantine_path):
        print_alert(f"❌ Archivo no encontrado en cuarentena: {filename}", "danger")
        return False
    
    try:
        # Extraer nombre original (eliminar timestamp)
        original_name = "_".join(filename.split("_")[2:]) if "_" in filename else filename
        
        if restore_path is None:
            # Restaurar al escritorio por defecto
            restore_path = os.path.join(os.path.expanduser("~"), "Desktop", original_name)
        
        shutil.move(quarantine_path, restore_path)
        print_alert(f"✅ Archivo restaurado: {restore_path}", "success")
        return True
        
    except Exception as e:
        print_alert(f"❌ Error al restaurar {filename}: {e}", "danger")
        return False
