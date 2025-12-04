import json
import sys
import os

# Set UTF-8 encoding for Windows console
if os.name == 'nt':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

from scanner.archivos import scan_files
from utils.alertas import get_console

def main():
    # Cargar configuración
    with open("config.json", "r", encoding="utf-8") as f:
        config = json.load(f)
    
    console = get_console()
    
    print("\n" + "="*60)
    print("PRUEBA DE ESCANEO DE ARCHIVOS - MINI EDR")
    print("="*60 + "\n")
    
    print("Escaneando archivos en carpeta de prueba...\n")
    
    # Ejecutar escaneo
    result = scan_files(config, collect_alerts=True)
    
    print("\n" + "="*60)
    print("RESUMEN DE RESULTADOS")
    print("="*60 + "\n")
    
    print(f"Alertas Criticas: {len(result.get('criticas', []))}")
    print(f"Alertas Leves: {len(result.get('leves', []))}\n")
    
    if result.get('criticas'):
        print("DETECCIONES CRITICAS:")
        for alerta in result['criticas']:
            print(f"   - {alerta}")
        print()
    
    if result.get('leves'):
        print("DETECCIONES LEVES:")
        for alerta in result['leves']:
            print(f"   - {alerta}")
        print()
    
    print("="*60 + "\n")
    print("Prueba completada. Revisa la carpeta 'quarantine' para ver archivos en cuarentena.\n")

if __name__ == "__main__":
    main()
