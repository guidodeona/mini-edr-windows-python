import sqlite3
import json
from datetime import datetime
import os

class EventDatabase:
    """Base de datos SQLite para almacenar histórico de eventos de seguridad"""
    
    def __init__(self, db_path="logs/events.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.init_database()
    
    def init_database(self):
        """Inicializa la base de datos y crea las tablas necesarias"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabla de eventos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                event_type TEXT NOT NULL,
                severity TEXT NOT NULL,
                module TEXT NOT NULL,
                description TEXT NOT NULL,
                details TEXT,
                resolved INTEGER DEFAULT 0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Tabla de archivos en cuarentena
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS quarantined_files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                original_path TEXT NOT NULL,
                quarantine_path TEXT NOT NULL,
                file_hash TEXT,
                reason TEXT,
                vt_detections INTEGER,
                quarantined_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Tabla de procesos sospechosos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS suspicious_processes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pid INTEGER NOT NULL,
                name TEXT NOT NULL,
                cmdline TEXT,
                cpu_percent REAL,
                memory_mb REAL,
                action_taken TEXT,
                detected_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Índices para búsquedas rápidas
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_timestamp ON events(timestamp)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_severity ON events(severity)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_module ON events(module)")
        
        conn.commit()
        conn.close()
    
    def log_event(self, event_type, severity, module, description, details=None):
        """Registra un evento en la base de datos"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        timestamp = datetime.now().isoformat()
        details_json = json.dumps(details) if details else None
        
        cursor.execute("""
            INSERT INTO events (timestamp, event_type, severity, module, description, details)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (timestamp, event_type, severity, module, description, details_json))
        
        conn.commit()
        event_id = cursor.lastrowid
        conn.close()
        
        return event_id
    
    def log_quarantine(self, original_path, quarantine_path, file_hash=None, reason=None, vt_detections=0):
        """Registra un archivo en cuarentena"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO quarantined_files 
            (original_path, quarantine_path, file_hash, reason, vt_detections)
            VALUES (?, ?, ?, ?, ?)
        """, (original_path, quarantine_path, file_hash, reason, vt_detections))
        
        conn.commit()
        conn.close()
    
    def log_suspicious_process(self, pid, name, cmdline=None, cpu_percent=0, memory_mb=0, action_taken=None):
        """Registra un proceso sospechoso"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO suspicious_processes 
            (pid, name, cmdline, cpu_percent, memory_mb, action_taken)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (pid, name, cmdline, cpu_percent, memory_mb, action_taken))
        
        conn.commit()
        conn.close()
    
    def get_events(self, limit=100, severity=None, module=None, start_date=None, end_date=None):
        """Obtiene eventos con filtros opcionales"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        query = "SELECT * FROM events WHERE 1=1"
        params = []
        
        if severity:
            query += " AND severity = ?"
            params.append(severity)
        
        if module:
            query += " AND module = ?"
            params.append(module)
        
        if start_date:
            query += " AND timestamp >= ?"
            params.append(start_date)
        
        if end_date:
            query += " AND timestamp <= ?"
            params.append(end_date)
        
        query += " ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)
        
        cursor.execute(query, params)
        events = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return events
    
    def get_statistics(self):
        """Obtiene estadísticas generales"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        stats = {}
        
        # Total de eventos
        cursor.execute("SELECT COUNT(*) FROM events")
        stats['total_events'] = cursor.fetchone()[0]
        
        # Eventos por severidad
        cursor.execute("SELECT severity, COUNT(*) FROM events GROUP BY severity")
        stats['by_severity'] = dict(cursor.fetchall())
        
        # Eventos por módulo
        cursor.execute("SELECT module, COUNT(*) FROM events GROUP BY module")
        stats['by_module'] = dict(cursor.fetchall())
        
        # Archivos en cuarentena
        cursor.execute("SELECT COUNT(*) FROM quarantined_files")
        stats['quarantined_files'] = cursor.fetchone()[0]
        
        # Procesos sospechosos
        cursor.execute("SELECT COUNT(*) FROM suspicious_processes")
        stats['suspicious_processes'] = cursor.fetchone()[0]
        
        # Eventos de las últimas 24 horas
        cursor.execute("""
            SELECT COUNT(*) FROM events 
            WHERE timestamp >= datetime('now', '-1 day')
        """)
        stats['events_24h'] = cursor.fetchone()[0]
        
        conn.close()
        return stats
    
    def search_events(self, search_term):
        """Busca eventos por término de búsqueda"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM events 
            WHERE description LIKE ? OR details LIKE ?
            ORDER BY timestamp DESC
            LIMIT 100
        """, (f"%{search_term}%", f"%{search_term}%"))
        
        events = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return events

# Instancia global
db = EventDatabase()
