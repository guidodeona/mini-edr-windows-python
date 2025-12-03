import json
import time
from utils.alertas import print_alert
from utils.informe import crear_informe, crear_informe_json
from scanner.procesos import scan_processes
from scanner.archivos import scan_files
from scanner.red import scan_network
from scanner.sistema import scan_system
from scanner.registro import scan_registry
from scanner.canary import scan_canary

def cargar_config():
    try:
        with open("config.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print_alert(f"[ERROR] No se pudo cargar config.json: {e}", "danger")
        exit()

config = cargar_config()

def escaneo_rapido():
    print_alert("\n🚀 Iniciando ESCANEO RÁPIDO...\n", "info")
    scan_processes(config)
    scan_network(config)
    print_alert("✔ Escaneo rápido finalizado.\n", "success")
    time.sleep(1)

def escaneo_completo():
    print_alert("\n🛡️ Iniciando ESCANEO COMPLETO...\n", "info")
    
    alertas_detectadas = []
    alertas_criticas = []

    for func in [scan_processes, scan_files, scan_network, scan_system, scan_registry, scan_canary]:
        try:
            result = func(config, collect_alerts=True)
            alertas_detectadas.extend(result.get("leves", []))
            alertas_criticas.extend(result.get("criticas", []))
        except TypeError:
            # Si el módulo no soporta collect_alerts
            func(config)

    crear_informe(alertas_detectadas, alertas_criticas)
    crear_informe_json(alertas_detectadas, alertas_criticas)
    print_alert("✔ Escaneo completo finalizado.\n", "success")
    time.sleep(1)

def modo_monitor():
    print_alert("\n👀 INICIANDO MODO MONITOR (Ctrl+C para detener)...\n", "info")
    interval = config.get("monitor_interval", 10)
    try:
        while True:
            # Ejecutamos escaneos silenciosos o con alertas
            # Para no saturar, podemos hacer un escaneo rápido + canary + registry
            scan_processes(config)
            scan_network(config)
            scan_registry(config)
            scan_canary(config)
            
            # Opcional: scan_files si es rápido, pero cuidado con directorios grandes
            # scan_files(config) 

            time.sleep(interval)
    except KeyboardInterrupt:
        print_alert("\n🛑 Modo monitor detenido.\n", "warning")

def menu_principal():
    while True:
        print("\n" + "="*50)
        print("     ⚡ ASISTENTE DE CIBERSEGURIDAD — NEXO ⚡")
        print("="*50)
        print("\nSeleccione una opción:\n")
        print("  1) Escaneo rápido")
        print("  2) Escaneo completo")
        print("  3) Escanear procesos")
        print("  4) Escanear archivos")
        print("  5) Escanear red")
        print("  6) Escanear sistema")
        print("  7) Ver ayuda")
        print("  8) Escanear registro (Persistencia)")
        print("  9) Verificar Honeyfile (Canary)")
        print("  10) MODO MONITOR (Tiempo real)")
        print("  0) Salir\n")

        opcion = input("👉 Opción: ")

        if opcion == "1":
            escaneo_rapido()
        elif opcion == "2":
            escaneo_completo()
        elif opcion == "3":
            scan_processes(config)
        elif opcion == "4":
            scan_files(config)
        elif opcion == "5":
            scan_network(config)
        elif opcion == "6":
            scan_system(config)
        elif opcion == "7":
            mostrar_ayuda()
        elif opcion == "8":
            scan_registry(config)
        elif opcion == "9":
            scan_canary(config)
        elif opcion == "10":
            modo_monitor()
        elif opcion == "0":
            print_alert("Saliendo del asistente...", "warning")
            break
        else:
            print_alert("Opción inválida.", "danger")

def mostrar_ayuda():
    print("\n📘 AYUDA DEL ASISTENTE\n")
    print("Este asistente escanea:")
    print("  • Procesos sospechosos")
    print("  • Archivos peligrosos")
    print("  • Puertos abiertos")
    print("  • Servicios del sistema")
    print("  • Integridad básica")
    print("  • Persistencia en Registro")
    print("  • Integridad de Honeyfile")
    print("\nLos resultados aparecen en:")
    print("  → Terminal (alertas)")
    print("  → logs/actividad.log")
    print("  → Informe final en logs/informe_YYYYMMDD_HHMMSS.txt\n")

def seleccionar_modo():
    print("\n===============================")
    print("   ASISTENTE DE CIBERSEGURIDAD")
    print("===============================\n")
    print("Seleccione el modo:")
    print("  1) Menú interactivo")
    print("  2) Escaneo rápido directo")
    print("  3) Escaneo completo directo")
    print("  4) Modo Monitor directo\n")

    modo = input("👉 Modo: ")

    if modo == "1":
        menu_principal()
    elif modo == "2":
        escaneo_rapido()
    elif modo == "3":
        escaneo_completo()
    elif modo == "4":
        modo_monitor()
    else:
        print_alert("Modo inválido.", "danger")

if __name__ == "__main__":
    seleccionar_modo()
