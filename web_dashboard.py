from flask import Flask, jsonify, render_template_string, request
from flask_cors import CORS
from utils.database import db
import psutil
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

# Template HTML del Dashboard
DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NEXO EDR - Dashboard</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #fff;
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        
        header {
            text-align: center;
            margin-bottom: 40px;
        }
        
        h1 {
            font-size: 3em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .subtitle {
            font-size: 1.2em;
            opacity: 0.9;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }
        
        .stat-card {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 25px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            transition: transform 0.3s ease;
        }
        
        .stat-card:hover {
            transform: translateY(-5px);
        }
        
        .stat-card h3 {
            font-size: 0.9em;
            opacity: 0.8;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .stat-value {
            font-size: 2.5em;
            font-weight: bold;
            margin-bottom: 5px;
        }
        
        .stat-label {
            font-size: 0.9em;
            opacity: 0.7;
        }
        
        .events-section {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 30px;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .events-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }
        
        .events-table {
            width: 100%;
            border-collapse: collapse;
        }
        
        .events-table th {
            text-align: left;
            padding: 12px;
            border-bottom: 2px solid rgba(255, 255, 255, 0.3);
            font-weight: 600;
            text-transform: uppercase;
            font-size: 0.85em;
            letter-spacing: 1px;
        }
        
        .events-table td {
            padding: 12px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .events-table tr:hover {
            background: rgba(255, 255, 255, 0.05);
        }
        
        .severity-badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.8em;
            font-weight: bold;
            text-transform: uppercase;
        }
        
        .severity-CRITICAL { background: #ff4444; }
        .severity-WARNING { background: #ffaa00; }
        .severity-INFO { background: #4444ff; }
        .severity-SUCCESS { background: #44ff44; color: #000; }
        
        .refresh-btn {
            background: rgba(255, 255, 255, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.3);
            color: white;
            padding: 10px 20px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1em;
            transition: all 0.3s ease;
        }
        
        .refresh-btn:hover {
            background: rgba(255, 255, 255, 0.3);
            transform: scale(1.05);
        }
        
        .system-info {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 30px;
        }
        
        .info-item {
            background: rgba(255, 255, 255, 0.05);
            padding: 15px;
            border-radius: 10px;
        }
        
        .info-label {
            font-size: 0.85em;
            opacity: 0.7;
            margin-bottom: 5px;
        }
        
        .info-value {
            font-size: 1.2em;
            font-weight: bold;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        
        .live-indicator {
            display: inline-block;
            width: 10px;
            height: 10px;
            background: #44ff44;
            border-radius: 50%;
            margin-right: 8px;
            animation: pulse 2s infinite;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>⚡ NEXO EDR Dashboard</h1>
            <p class="subtitle"><span class="live-indicator"></span>Monitoreo en Tiempo Real</p>
        </header>
        
        <div class="stats-grid" id="stats">
            <!-- Stats will be loaded here -->
        </div>
        
        <div class="system-info" id="system-info">
            <!-- System info will be loaded here -->
        </div>
        
        <div class="events-section" style="margin-top: 40px;">
            <div class="events-header">
                <h2>📋 Eventos Recientes</h2>
                <button class="refresh-btn" onclick="loadData()">🔄 Actualizar</button>
            </div>
            <table class="events-table">
                <thead>
                    <tr>
                        <th>Timestamp</th>
                        <th>Módulo</th>
                        <th>Severidad</th>
                        <th>Descripción</th>
                    </tr>
                </thead>
                <tbody id="events-body">
                    <!-- Events will be loaded here -->
                </tbody>
            </table>
        </div>
    </div>
    
    <script>
        async function loadData() {
            try {
                // Load statistics
                const statsRes = await fetch('/api/stats');
                const stats = await statsRes.json();
                
                const statsHtml = `
                    <div class="stat-card">
                        <h3>Total de Eventos</h3>
                        <div class="stat-value">${stats.total_events || 0}</div>
                        <div class="stat-label">Registrados</div>
                    </div>
                    <div class="stat-card">
                        <h3>Eventos 24h</h3>
                        <div class="stat-value">${stats.events_24h || 0}</div>
                        <div class="stat-label">Últimas 24 horas</div>
                    </div>
                    <div class="stat-card">
                        <h3>Archivos en Cuarentena</h3>
                        <div class="stat-value">${stats.quarantined_files || 0}</div>
                        <div class="stat-label">Aislados</div>
                    </div>
                    <div class="stat-card">
                        <h3>Procesos Sospechosos</h3>
                        <div class="stat-value">${stats.suspicious_processes || 0}</div>
                        <div class="stat-label">Detectados</div>
                    </div>
                `;
                document.getElementById('stats').innerHTML = statsHtml;
                
                // Load system info
                const sysRes = await fetch('/api/system');
                const sys = await sysRes.json();
                
                const sysHtml = `
                    <div class="info-item">
                        <div class="info-label">CPU</div>
                        <div class="info-value">${sys.cpu_percent}%</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Memoria</div>
                        <div class="info-value">${sys.memory_percent}%</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Disco</div>
                        <div class="info-value">${sys.disk_percent}%</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Procesos Activos</div>
                        <div class="info-value">${sys.process_count}</div>
                    </div>
                `;
                document.getElementById('system-info').innerHTML = sysHtml;
                
                // Load events
                const eventsRes = await fetch('/api/events?limit=20');
                const events = await eventsRes.json();
                
                const eventsHtml = events.map(event => `
                    <tr>
                        <td>${new Date(event.timestamp).toLocaleString()}</td>
                        <td>${event.module}</td>
                        <td><span class="severity-badge severity-${event.severity}">${event.severity}</span></td>
                        <td>${event.description}</td>
                    </tr>
                `).join('');
                
                document.getElementById('events-body').innerHTML = eventsHtml || '<tr><td colspan="4" style="text-align: center;">No hay eventos registrados</td></tr>';
                
            } catch (error) {
                console.error('Error loading data:', error);
            }
        }
        
        // Load data on page load
        loadData();
        
        // Auto-refresh every 10 seconds
        setInterval(loadData, 10000);
    </script>
</body>
</html>
"""

@app.route('/')
def dashboard():
    """Página principal del dashboard"""
    return render_template_string(DASHBOARD_HTML)

@app.route('/api/stats')
def get_stats():
    """API: Obtiene estadísticas generales"""
    stats = db.get_statistics()
    return jsonify(stats)

@app.route('/api/events')
def get_events():
    """API: Obtiene eventos recientes"""
    limit = request.args.get('limit', 100, type=int)
    severity = request.args.get('severity')
    module = request.args.get('module')
    
    events = db.get_events(limit=limit, severity=severity, module=module)
    return jsonify(events)

@app.route('/api/system')
def get_system_info():
    """API: Obtiene información del sistema en tiempo real"""
    try:
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        return jsonify({
            'cpu_percent': round(cpu_percent, 1),
            'memory_percent': round(memory.percent, 1),
            'memory_used_gb': round(memory.used / (1024**3), 2),
            'memory_total_gb': round(memory.total / (1024**3), 2),
            'disk_percent': round(disk.percent, 1),
            'disk_used_gb': round(disk.used / (1024**3), 2),
            'disk_total_gb': round(disk.total / (1024**3), 2),
            'process_count': len(psutil.pids())
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/search')
def search_events():
    """API: Busca eventos por término"""
    term = request.args.get('q', '')
    if not term:
        return jsonify([])
    
    events = db.search_events(term)
    return jsonify(events)

def start_dashboard(host='0.0.0.0', port=5000, debug=False):
    """Inicia el servidor del dashboard"""
    print(f"\n🌐 Dashboard disponible en: http://localhost:{port}")
    print(f"🔗 Acceso remoto: http://{host}:{port}\n")
    app.run(host=host, port=port, debug=debug)

if __name__ == '__main__':
    start_dashboard(debug=True)
