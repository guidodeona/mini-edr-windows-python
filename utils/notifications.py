import os
import requests
from datetime import datetime
from utils.logger import log_event

class NotificationSystem:
    """Sistema de notificaciones para alertas críticas"""
    
    def __init__(self, config):
        self.config = config
        self.discord_webhook = config.get("discord_webhook")
        self.slack_webhook = config.get("slack_webhook")
        self.email_enabled = config.get("email_enabled", False)
    
    def send_discord(self, title, message, severity="info"):
        """Envía notificación a Discord via webhook"""
        if not self.discord_webhook:
            return False
        
        # Colores según severidad
        colors = {
            "info": 3447003,      # Azul
            "warning": 16776960,  # Amarillo
            "danger": 15158332,   # Rojo
            "success": 3066993    # Verde
        }
        
        # Emojis según severidad
        emojis = {
            "info": "ℹ️",
            "warning": "⚠️",
            "danger": "🚨",
            "success": "✅"
        }
        
        embed = {
            "title": f"{emojis.get(severity, 'ℹ️')} {title}",
            "description": message,
            "color": colors.get(severity, 3447003),
            "timestamp": datetime.utcnow().isoformat(),
            "footer": {
                "text": "NEXO EDR - Sistema de Seguridad"
            }
        }
        
        payload = {
            "embeds": [embed]
        }
        
        try:
            response = requests.post(self.discord_webhook, json=payload, timeout=5)
            if response.status_code == 204:
                return True
            else:
                log_event(f"Error enviando notificación Discord: {response.status_code}")
                return False
        except Exception as e:
            log_event(f"Error enviando notificación Discord: {e}")
            return False
    
    def send_slack(self, title, message, severity="info"):
        """Envía notificación a Slack via webhook"""
        if not self.slack_webhook:
            return False
        
        # Colores según severidad
        colors = {
            "info": "#36a64f",
            "warning": "#ff9900",
            "danger": "#ff0000",
            "success": "#00ff00"
        }
        
        payload = {
            "attachments": [
                {
                    "color": colors.get(severity, "#36a64f"),
                    "title": title,
                    "text": message,
                    "footer": "NEXO EDR",
                    "ts": int(datetime.now().timestamp())
                }
            ]
        }
        
        try:
            response = requests.post(self.slack_webhook, json=payload, timeout=5)
            if response.status_code == 200:
                return True
            else:
                log_event(f"Error enviando notificación Slack: {response.status_code}")
                return False
        except Exception as e:
            log_event(f"Error enviando notificación Slack: {e}")
            return False
    
    def send_notification(self, title, message, severity="info"):
        """Envía notificación a todos los canales configurados"""
        results = {}
        
        if self.discord_webhook:
            results['discord'] = self.send_discord(title, message, severity)
        
        if self.slack_webhook:
            results['slack'] = self.send_slack(title, message, severity)
        
        return results
    
    def notify_critical_event(self, event_type, details):
        """Notifica un evento crítico"""
        title = f"🚨 ALERTA CRÍTICA: {event_type}"
        message = f"**Detalles:** {details}\n**Timestamp:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        return self.send_notification(title, message, severity="danger")
    
    def notify_malware_detected(self, filename, path, detections=0):
        """Notifica detección de malware"""
        title = "🦠 MALWARE DETECTADO"
        message = f"""
**Archivo:** {filename}
**Ruta:** {path}
**Detecciones:** {detections} motores antivirus
**Acción:** Archivo movido a cuarentena
**Timestamp:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """
        
        return self.send_notification(title, message, severity="danger")
    
    def notify_suspicious_process(self, process_name, pid, action):
        """Notifica proceso sospechoso"""
        title = "⚠️ PROCESO SOSPECHOSO"
        message = f"""
**Proceso:** {process_name}
**PID:** {pid}
**Acción tomada:** {action}
**Timestamp:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """
        
        return self.send_notification(title, message, severity="warning")
    
    def notify_canary_triggered(self, canary_path):
        """Notifica que un archivo canary fue accedido"""
        title = "🐤 CANARY ACTIVADO - POSIBLE INTRUSIÓN"
        message = f"""
**Archivo señuelo accedido:** {canary_path}
**Esto indica actividad no autorizada en el sistema**
**Timestamp:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """
        
        return self.send_notification(title, message, severity="danger")

def create_notification_system(config):
    """Factory function para crear el sistema de notificaciones"""
    return NotificationSystem(config)
