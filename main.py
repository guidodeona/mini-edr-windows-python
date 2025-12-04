import json
import time
from utils.alertas import print_alert
from utils.informe import crear_informe, crear_informe_json
from scanner.procesos import scan_processes
from scanner.archivos import scan_files, start_file_monitor
import scanner.archivos # Para acceder a la variable global latest_file_alert
from scanner.red import scan_network
from scanner.sistema import scan_system
from scanner.registro import scan_registry
from scanner.canary import scan_canary
from utils.alertas import print_alert, get_console

from rich.panel import Panel
from rich.table import Table
from rich.layout import Layout
from rich.live import Live
from rich.align import Align
from rich.text import Text
from rich import box

console = get_console()

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

def generate_dashboard_table(last_alerts, system_status):
    """Genera la tabla principal del dashboard para el modo Live."""
    table = Table(title="🛡️  MONITOR DE SEGURIDAD EN TIEMPO REAL", box=box.ROUNDED, expand=True)
    table.add_column("Módulo", style="cyan", no_wrap=True)
    table.add_column("Estado", style="green")
    table.add_column("Última Alerta", style="bold red")

    # Filas de estado (simuladas o reales)
    table.add_row("Procesos", "ACTIVO", last_alerts.get("procesos", "-"))
    table.add_row("Red", "ACTIVO", last_alerts.get("red", "-"))
    table.add_row("Archivos (Watchdog)", "VIGILANDO", last_alerts.get("archivos", "-"))
    table.add_row("Registro", "PROTEGIDO", last_alerts.get("registro", "-"))
    table.add_row("Canary", "INTACTO", last_alerts.get("canary", "-"))
    
    return table

def modo_monitor():
    console.clear()
    console.print(Panel.fit("Iniciando MODO MONITOR... (Ctrl+C para detener)", style="bold blue"))
    
    # Iniciar Watchdog
    observer = start_file_monitor(config)
    
    interval = config.get("monitor_interval", 5)
    
    last_alerts = {
        "procesos": "Sin incidentes",
        "red": "Tráfico normal",
        "archivos": "Sin cambios",
        "registro": "Limpio",
        "canary": "Seguro"
    }

    try:
        with Live(generate_dashboard_table(last_alerts, {}), refresh_per_second=1, console=console) as live:
            while True:
                # 1. Chequear Watchdog (Archivos)
                if scanner.archivos.latest_file_alert:
                    last_alerts["archivos"] = scanner.archivos.latest_file_alert

                # 2. Escaneo de Procesos
                proc_res = scan_processes(config, collect_alerts=True)
                if proc_res["criticas"]:
                    last_alerts["procesos"] = proc_res["criticas"][-1]
                elif proc_res["leves"]:
                    last_alerts["procesos"] = proc_res["leves"][-1]
                else:
                    last_alerts["procesos"] = "OK"

                # 3. Escaneo de Red (Simulado update visual)
                scan_network(config) 

                # Actualizar Dashboard
                live.update(generate_dashboard_table(last_alerts, {}))
                
                time.sleep(interval)
    except KeyboardInterrupt:
        console.print("\n🛑 Modo monitor detenido.", style="bold red")
    finally:
        if observer:
            observer.stop()
            observer.join()

def pausa():
    input("\nPresione Enter para continuar...")

def menu_principal():
    while True:
        console.clear()
        
        # Banner Principal
        banner_text = Text("⚡ ASISTENTE DE CIBERSEGURIDAD — NEXO ⚡", justify="center", style="bold white on blue")
        console.print(Panel(banner_text, box=box.DOUBLE_EDGE))
        
        # Tabla de Menú
        menu_table = Table(show_header=False, box=box.SIMPLE)
        menu_table.add_column("Opción", style="cyan bold", width=4)
        menu_table.add_column("Descripción", style="white")
        
        menu_table.add_row("1", "🚀 Escaneo Rápido")
        menu_table.add_row("2", "🛡️  Escaneo Completo")
        menu_table.add_row("3", "🔍 Escanear Procesos")
        menu_table.add_row("4", "📂 Escanear Archivos")
        menu_table.add_row("5", "🌐 Escanear Red")
        menu_table.add_row("6", "💻 Escanear Sistema")
        menu_table.add_row("7", "❓ Ayuda")
        menu_table.add_row("8", "📝 Escanear Registro")
        menu_table.add_row("9", "🐤 Verificar Canary")
        menu_table.add_row("10", "👀 MODO MONITOR (Live Dashboard)")
        menu_table.add_row("11", "🔒 Ver Archivos en Cuarentena")
        menu_table.add_row("0", "❌ Salir")
        
        console.print(menu_table)
        console.print("\n")

        opcion = console.input("[bold yellow]👉 Seleccione una opción:[/bold yellow] ")

        if opcion == "1":
            escaneo_rapido()
            pausa()
        elif opcion == "2":
            escaneo_completo()
            pausa()
        elif opcion == "3":
            scan_processes(config)
            pausa()
        elif opcion == "4":
            scan_files(config)
            pausa()
        elif opcion == "5":
            scan_network(config)
            pausa()
        elif opcion == "6":
            scan_system(config)
            pausa()
        elif opcion == "7":
            mostrar_ayuda()
        elif opcion == "8":
            scan_registry(config)
            pausa()
        elif opcion == "9":
            scan_canary(config)
            pausa()
        elif opcion == "10":
            modo_monitor()
            pausa()
        elif opcion == "11":
            from utils.quarantine import list_quarantined_files
            list_quarantined_files(config["file_scanner"].get("quarantine_folder", "quarantine"))
            pausa()
        elif opcion == "0":
            console.print("Saliendo del asistente...", style="bold red")
            break
        else:
            console.print("Opción inválida.", style="bold red")
            pausa()

def mostrar_ayuda():
    help_text = """
# 📘 AYUDA DEL ASISTENTE — NEXO EDR

Este asistente escanea y **protege activamente** tu sistema:

## 🔍 Detección
- **Procesos**: Detecta nombres sospechosos y alto consumo.
- **Archivos**: Busca extensiones peligrosas + análisis YARA avanzado.
- **Red**: Identifica puertos abiertos inusuales.
- **Registro**: Busca persistencia de malware.
- **Canary**: Verifica si tus archivos señuelo han sido tocados.

## 🛡️ Respuesta Activa
- **Cuarentena Automática**: Los archivos peligrosos se mueven automáticamente a una carpeta segura.
- **YARA Engine**: Detecta malware por contenido, no solo por nombre.

## 📊 Resultados
- Terminal (Alertas visuales en tiempo real)
- `logs/actividad.log`
- Informe final en `logs/`
- `quarantine/` (Archivos en cuarentena)
    """
    console.print(Panel(help_text, title="Ayuda", border_style="green"))
    console.input("Presione Enter para volver al menú...")

def seleccionar_modo():
    console.clear()
    
    banner = Text("⚡ ASISTENTE DE CIBERSEGURIDAD — NEXO ⚡", justify="center", style="bold white on blue")
    console.print(Panel(banner, box=box.DOUBLE_EDGE))
    
    menu = Table(show_header=False, box=box.SIMPLE)
    menu.add_column("Opción", style="cyan bold", width=4)
    menu.add_column("Descripción", style="white")
    
    menu.add_row("1", "📋 Menú Interactivo")
    menu.add_row("2", "🚀 Escaneo Rápido Directo")
    menu.add_row("3", "🛡️  Escaneo Completo Directo")
    menu.add_row("4", "👀 Modo Monitor Directo")
    
    console.print(menu)
    console.print("\n")

    modo = console.input("[bold yellow]👉 Seleccione el modo:[/bold yellow] ")

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
