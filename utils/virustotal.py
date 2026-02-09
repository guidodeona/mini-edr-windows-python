import requests
import hashlib
import os
from utils.logger import log_event
from utils.alertas import print_alert

class VirusTotalScanner:
    """Integración con VirusTotal API para verificar archivos sospechosos"""
    
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("VIRUSTOTAL_API_KEY")
        self.base_url = "https://www.virustotal.com/api/v3"
        self.headers = {
            "x-apikey": self.api_key
        } if self.api_key else None
    
    def calculate_file_hash(self, filepath):
        """Calcula el hash SHA256 de un archivo"""
        try:
            sha256_hash = hashlib.sha256()
            with open(filepath, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except Exception as e:
            log_event(f"Error calculando hash de {filepath}: {e}")
            return None
    
    def check_file_hash(self, file_hash):
        """Verifica un hash en VirusTotal"""
        if not self.api_key:
            return {
                "error": "API Key no configurada",
                "message": "Configure VIRUSTOTAL_API_KEY en .env"
            }
        
        try:
            url = f"{self.base_url}/files/{file_hash}"
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                stats = data.get("data", {}).get("attributes", {}).get("last_analysis_stats", {})
                
                return {
                    "found": True,
                    "malicious": stats.get("malicious", 0),
                    "suspicious": stats.get("suspicious", 0),
                    "undetected": stats.get("undetected", 0),
                    "harmless": stats.get("harmless", 0),
                    "total_engines": sum(stats.values()),
                    "permalink": f"https://www.virustotal.com/gui/file/{file_hash}"
                }
            elif response.status_code == 404:
                return {"found": False, "message": "Archivo no encontrado en VT"}
            else:
                return {"error": f"Error HTTP {response.status_code}"}
                
        except requests.exceptions.Timeout:
            return {"error": "Timeout al conectar con VirusTotal"}
        except Exception as e:
            return {"error": f"Error: {str(e)}"}
    
    def scan_file(self, filepath):
        """Escanea un archivo: calcula hash y verifica en VT"""
        file_hash = self.calculate_file_hash(filepath)
        if not file_hash:
            return {"error": "No se pudo calcular hash"}
        
        print_alert(f"🔍 Hash SHA256: {file_hash}", "info")
        result = self.check_file_hash(file_hash)
        
        if result.get("found"):
            malicious = result.get("malicious", 0)
            total = result.get("total_engines", 0)
            
            if malicious > 0:
                print_alert(
                    f"⚠️ MALICIOSO: {malicious}/{total} motores lo detectan como amenaza",
                    "danger"
                )
                print_alert(f"🔗 Ver reporte: {result.get('permalink')}", "warning")
            else:
                print_alert(f"✅ Limpio: 0/{total} detecciones", "success")
        
        return result

def scan_file_with_vt(filepath, api_key=None):
    """Función helper para escanear un archivo con VirusTotal"""
    scanner = VirusTotalScanner(api_key)
    return scanner.scan_file(filepath)
