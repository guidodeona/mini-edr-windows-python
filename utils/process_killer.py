import psutil
import os
from utils.logger import log_event
from utils.alertas import print_alert
from utils.database import db

class ProcessKiller:
    """Módulo para terminar procesos maliciosos de forma segura"""
    
    def __init__(self):
        self.protected_processes = [
            "System", "Registry", "smss.exe", "csrss.exe", 
            "wininit.exe", "services.exe", "lsass.exe", "winlogon.exe",
            "explorer.exe", "dwm.exe"
        ]
    
    def is_protected(self, process_name):
        """Verifica si un proceso está protegido (crítico del sistema)"""
        return process_name in self.protected_processes
    
    def kill_process(self, pid, process_name, reason="Proceso sospechoso"):
        """Termina un proceso por PID"""
        
        # Verificar si es un proceso protegido
        if self.is_protected(process_name):
            print_alert(
                f"⚠️ No se puede terminar {process_name} (PID {pid}): Proceso crítico del sistema",
                "warning"
            )
            log_event(f"Intento de terminar proceso protegido: {process_name} (PID {pid})")
            return False
        
        try:
            process = psutil.Process(pid)
            
            # Obtener información antes de terminar
            try:
                cmdline = " ".join(process.cmdline())
                cpu_percent = process.cpu_percent(interval=0.1)
                memory_mb = process.memory_info().rss / 1024 / 1024
            except:
                cmdline = "N/A"
                cpu_percent = 0
                memory_mb = 0
            
            # Intentar terminar el proceso
            process.terminate()
            
            # Esperar hasta 3 segundos para que termine
            try:
                process.wait(timeout=3)
                print_alert(
                    f"✅ Proceso terminado: {process_name} (PID {pid}) - {reason}",
                    "success"
                )
                action = "TERMINATED"
            except psutil.TimeoutExpired:
                # Si no termina, forzar
                process.kill()
                print_alert(
                    f"⚡ Proceso forzado a terminar: {process_name} (PID {pid})",
                    "warning"
                )
                action = "KILLED"
            
            # Registrar en la base de datos
            db.log_suspicious_process(
                pid=pid,
                name=process_name,
                cmdline=cmdline,
                cpu_percent=cpu_percent,
                memory_mb=memory_mb,
                action_taken=action
            )
            
            # Registrar evento
            db.log_event(
                event_type="PROCESS_KILLED",
                severity="CRITICAL",
                module="ProcessKiller",
                description=f"Proceso {process_name} (PID {pid}) terminado",
                details={
                    "pid": pid,
                    "name": process_name,
                    "reason": reason,
                    "action": action,
                    "cmdline": cmdline
                }
            )
            
            log_event(f"Proceso terminado: {process_name} (PID {pid}) - {reason}")
            return True
            
        except psutil.NoSuchProcess:
            print_alert(f"⚠️ El proceso {pid} ya no existe", "warning")
            return False
        except psutil.AccessDenied:
            print_alert(
                f"❌ Acceso denegado al intentar terminar {process_name} (PID {pid}). Ejecute como administrador.",
                "danger"
            )
            return False
        except Exception as e:
            print_alert(f"❌ Error al terminar proceso {pid}: {e}", "danger")
            log_event(f"Error al terminar proceso {pid}: {e}")
            return False
    
    def kill_by_name(self, process_name, reason="Proceso sospechoso"):
        """Termina todos los procesos con un nombre específico"""
        killed_count = 0
        
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if proc.info['name'].lower() == process_name.lower():
                    if self.kill_process(proc.info['pid'], proc.info['name'], reason):
                        killed_count += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        if killed_count > 0:
            print_alert(f"✅ {killed_count} proceso(s) '{process_name}' terminados", "success")
        else:
            print_alert(f"ℹ️ No se encontraron procesos activos con nombre '{process_name}'", "info")
        
        return killed_count
    
    def suspend_process(self, pid, process_name):
        """Suspende un proceso (lo pausa sin terminarlo)"""
        if self.is_protected(process_name):
            print_alert(
                f"⚠️ No se puede suspender {process_name} (PID {pid}): Proceso crítico",
                "warning"
            )
            return False
        
        try:
            process = psutil.Process(pid)
            process.suspend()
            print_alert(f"⏸️ Proceso suspendido: {process_name} (PID {pid})", "warning")
            
            db.log_event(
                event_type="PROCESS_SUSPENDED",
                severity="WARNING",
                module="ProcessKiller",
                description=f"Proceso {process_name} (PID {pid}) suspendido",
                details={"pid": pid, "name": process_name}
            )
            
            return True
        except Exception as e:
            print_alert(f"❌ Error al suspender proceso {pid}: {e}", "danger")
            return False
    
    def resume_process(self, pid, process_name):
        """Reanuda un proceso suspendido"""
        try:
            process = psutil.Process(pid)
            process.resume()
            print_alert(f"▶️ Proceso reanudado: {process_name} (PID {pid})", "info")
            return True
        except Exception as e:
            print_alert(f"❌ Error al reanudar proceso {pid}: {e}", "danger")
            return False

# Instancia global
killer = ProcessKiller()
