import json
import time
import os
from dotenv import load_dotenv
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
from utils.database import db
from utils.virustotal import scan_file_with_vt
from utils.process_killer import killer
from utils.notifications import create_notification_system
import threading

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
        # Cargar variables de entorno
        load_dotenv()
        
        with open("config.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print_alert(f"[ERROR] No se pudo cargar config.json: {e}", "danger")
        exit()

config = cargar_config()

# Inicializar sistema de notificaciones si está habilitado
notifier = None
if config.get("notifications", {}).get("enabled"):
    notifier = create_notification_system(config.get("notifications", {}))

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
        menu_table.add_row("12", "🦠 Escanear Archivo con VirusTotal")
        menu_table.add_row("13", "📊 Ver Estadísticas de Base de Datos")
        menu_table.add_row("14", "🌐 Iniciar Dashboard Web")
        menu_table.add_row("15", "⚔️ Gestión de Procesos")
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
        elif opcion == "12":
            escanear_con_virustotal()
            pausa()
        elif opcion == "13":
            mostrar_estadisticas_db()
            pausa()
        elif opcion == "14":
            iniciar_dashboard_web()
            pausa()
        elif opcion == "15":
            menu_gestion_procesos()
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

def escanear_con_virustotal():
    """Escanea un archivo específico con VirusTotal"""
    console.print("\n🦠 ESCANEO CON VIRUSTOTAL\n", style="bold cyan")
    filepath = console.input("Ingrese la ruta completa del archivo: ")
    
    if not os.path.exists(filepath):
        print_alert("❌ El archivo no existe", "danger")
        return
    
    api_key = os.getenv("VIRUSTOTAL_API_KEY")
    if not api_key:
        print_alert("⚠️ No se encontró VIRUSTOTAL_API_KEY en .env", "warning")
        print_alert("Obtén tu API key gratuita en: https://www.virustotal.com/gui/my-apikey", "info")
        return
    
    result = scan_file_with_vt(filepath, api_key)
    
    if result.get("found") and result.get("malicious", 0) > 0:
        # Notificar si está habilitado
        if notifier and config.get("notifications", {}).get("notify_on_malware"):
            notifier.notify_malware_detected(
                os.path.basename(filepath),
                filepath,
                result.get("malicious", 0)
            )

def mostrar_estadisticas_db():
    """Muestra estadísticas de la base de datos"""
    console.print("\n📊 ESTADÍSTICAS DE BASE DE DATOS\n", style="bold cyan")
    
    stats = db.get_statistics()
    
    from rich.table import Table
    table = Table(title="Resumen de Eventos", show_header=True)
    table.add_column("Métrica", style="cyan")
    table.add_column("Valor", style="yellow")
    
    table.add_row("Total de Eventos", str(stats.get("total_events", 0)))
    table.add_row("Eventos (24h)", str(stats.get("events_24h", 0)))
    table.add_row("Archivos en Cuarentena", str(stats.get("quarantined_files", 0)))
    table.add_row("Procesos Sospechosos", str(stats.get("suspicious_processes", 0)))
    
    console.print(table)
    
    # Eventos por severidad
    if stats.get("by_severity"):
        console.print("\n📈 Por Severidad:", style="bold")
        for severity, count in stats["by_severity"].items():
            console.print(f"  • {severity}: {count}")
    
    # Eventos por módulo
    if stats.get("by_module"):
        console.print("\n📦 Por Módulo:", style="bold")
        for module, count in stats["by_module"].items():
            console.print(f"  • {module}: {count}")

def iniciar_dashboard_web():
    """Inicia el dashboard web en un thread separado"""
    console.print("\n🌐 INICIANDO DASHBOARD WEB\n", style="bold cyan")
    
    web_config = config.get("web_dashboard", {})
    host = web_config.get("host", "0.0.0.0")
    port = web_config.get("port", 5000)
    
    console.print(f"🚀 Dashboard disponible en: http://localhost:{port}", style="bold green")
    console.print(f"🔗 Acceso remoto: http://{host}:{port}", style="bold green")
    console.print("\n⚠️ Presione Ctrl+C para detener el servidor\n", style="yellow")
    
    try:
        from web_dashboard import start_dashboard
        start_dashboard(host=host, port=port, debug=False)
    except KeyboardInterrupt:
        console.print("\n🛑 Dashboard detenido", style="bold red")
    except Exception as e:
        print_alert(f"❌ Error al iniciar dashboard: {e}", "danger")

def menu_gestion_procesos():
    """Menú para gestionar procesos"""
    while True:
        console.clear()
        console.print("\n⚔️ GESTIÓN DE PROCESOS\n", style="bold cyan")
        
        menu = Table(show_header=False, box=box.SIMPLE)
        menu.add_column("Opción", style="cyan bold", width=4)
        menu.add_column("Descripción", style="white")
        
        menu.add_row("1", "🔪 Terminar proceso por PID")
        menu.add_row("2", "🔪 Terminar procesos por nombre")
        menu.add_row("3", "⏸️ Suspender proceso")
        menu.add_row("4", "▶️ Reanudar proceso")
        menu.add_row("5", "📋 Listar procesos activos")
        menu.add_row("0", "⬅️ Volver")
        
        console.print(menu)
        opcion = console.input("\n[bold yellow]👉 Seleccione una opción:[/bold yellow] ")
        
        if opcion == "1":
            try:
                pid = int(console.input("Ingrese el PID del proceso: "))
                nombre = console.input("Ingrese el nombre del proceso: ")
                killer.kill_process(pid, nombre)
            except ValueError:
                print_alert("❌ PID inválido", "danger")
            pausa()
        elif opcion == "2":
            nombre = console.input("Ingrese el nombre del proceso: ")
            killer.kill_by_name(nombre)
            pausa()
        elif opcion == "3":
            try:
                pid = int(console.input("Ingrese el PID del proceso: "))
                nombre = console.input("Ingrese el nombre del proceso: ")
                killer.suspend_process(pid, nombre)
            except ValueError:
                print_alert("❌ PID inválido", "danger")
            pausa()
        elif opcion == "4":
            try:
                pid = int(console.input("Ingrese el PID del proceso: "))
                nombre = console.input("Ingrese el nombre del proceso: ")
                killer.resume_process(pid, nombre)
            except ValueError:
                print_alert("❌ PID inválido", "danger")
            pausa()
        elif opcion == "5":
            import psutil
            console.print("\n📋 PROCESOS ACTIVOS\n", style="bold")
            proc_table = Table()
            proc_table.add_column("PID", style="cyan")
            proc_table.add_column("Nombre", style="yellow")
            proc_table.add_column("CPU %", style="green")
            proc_table.add_column("RAM %", style="magenta")
            
            for proc in sorted(psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']), 
                             key=lambda p: p.info.get('cpu_percent', 0), reverse=True)[:20]:
                try:
                    proc_table.add_row(
                        str(proc.info['pid']),
                        proc.info['name'][:30],
                        f"{proc.info.get('cpu_percent', 0):.1f}",
                        f"{proc.info.get('memory_percent', 0):.1f}"
                    )
                except:
                    continue
            
            console.print(proc_table)
            pausa()
        elif opcion == "0":
            break
        else:
            print_alert("Opción inválida", "danger")
            pausa()

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
