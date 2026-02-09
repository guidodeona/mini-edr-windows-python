# 📋 Changelog - NEXO EDR

Todos los cambios notables de este proyecto serán documentados en este archivo.

## [2.0.0] - 2026-02-09

### ✨ Nuevas Funcionalidades

#### 🦠 Integración con VirusTotal

- Verificación de archivos contra 70+ motores antivirus
- Cálculo automático de hash SHA256
- Detección de malware conocido
- Enlaces directos a reportes de VirusTotal
- Soporte para API key gratuita

#### ⚔️ Gestión Avanzada de Procesos

- **Auto-Kill**: Terminación automática de procesos maliciosos
- **Kill by PID**: Eliminar procesos específicos
- **Kill by Name**: Eliminar todos los procesos con un nombre
- **Suspend/Resume**: Pausar y reanudar procesos
- **Protección de procesos críticos**: Sistema no permite terminar procesos esenciales de Windows
- **Configuración flexible**: Auto-kill desactivado por defecto para seguridad

#### 💾 Base de Datos SQLite

- Almacenamiento persistente de todos los eventos
- Tabla de eventos con severidad, módulo y detalles
- Tabla de archivos en cuarentena con metadata
- Tabla de procesos sospechosos detectados
- Búsqueda avanzada de eventos históricos
- Estadísticas agregadas por severidad y módulo
- Filtros por fecha, severidad y módulo
- Correlación de eventos en el tiempo

#### 🌐 Dashboard Web Interactivo

- Interfaz web moderna con Flask
- Visualización en tiempo real de métricas del sistema
- Tabla de eventos recientes con auto-actualización
- Estadísticas de seguridad (cuarentena, procesos sospechosos)
- API REST para integración externa
- Diseño responsive con gradientes y glassmorphism
- Auto-refresh cada 10 segundos
- Endpoints: /api/stats, /api/events, /api/system, /api/search

#### 🔔 Sistema de Notificaciones

- **Discord Integration**: Webhooks para alertas en tiempo real
- **Slack Integration**: Notificaciones a canales de Slack
- Alertas personalizadas por tipo de evento
- Notificaciones para:
  - Eventos críticos
  - Detección de malware
  - Activación de canary
  - Procesos sospechosos
- Formato de mensajes con colores según severidad
- Timestamps automáticos

### 🔧 Mejoras

#### Scanner de Procesos

- Registro de eventos en base de datos
- Integración con auto-kill
- Detección de procesos con CPU alta configurable
- Métricas detalladas (CPU%, RAM%)
- Logging mejorado con contexto completo

#### Configuración

- Nuevas opciones en config.json:
  - `auto_kill`: Control de terminación automática
  - `kill_on_high_cpu`: Kill por alto uso de CPU
  - `cpu_threshold`: Umbral configurable
  - `use_virustotal`: Integración con VT
  - `notifications`: Sistema de alertas
  - `web_dashboard`: Configuración del dashboard
  - `database`: Opciones de base de datos

#### Menú Principal

- 4 nuevas opciones:
  - Opción 12: Escanear con VirusTotal
  - Opción 13: Ver estadísticas de BD
  - Opción 14: Iniciar dashboard web
  - Opción 15: Gestión de procesos
- Interfaz mejorada con emojis
- Mejor organización de opciones

#### Documentación

- README completamente reescrito
- Instrucciones de instalación detalladas
- Guía de configuración paso a paso
- Ejemplos de uso
- Documentación de API
- Sección de seguridad
- Changelog incluido

### 📦 Dependencias Nuevas

- `requests`: Para VirusTotal API y webhooks
- `flask`: Dashboard web
- `flask-cors`: CORS para API
- `python-dotenv`: Gestión de variables de entorno

### 🔒 Seguridad

- Auto-kill desactivado por defecto
- Protección de procesos críticos del sistema
- Variables de entorno para API keys sensibles
- .gitignore actualizado para excluir .env
- Validación de permisos antes de terminar procesos

### 📁 Nuevos Archivos

- `utils/database.py`: Gestión de base de datos SQLite
- `utils/virustotal.py`: Integración con VirusTotal API
- `utils/process_killer.py`: Gestión de procesos
- `utils/notifications.py`: Sistema de notificaciones
- `web_dashboard.py`: Dashboard web con Flask
- `.env.example`: Plantilla de variables de entorno
- `.gitignore`: Exclusiones de Git actualizadas
- `CHANGELOG.md`: Este archivo

### 🐛 Correcciones

- Mejora en el manejo de excepciones en scanner de procesos
- Corrección de memory leaks en modo monitor
- Mejor manejo de procesos que ya no existen
- Validación de rutas de archivos antes de escanear

---

## [1.0.0] - 2025-12-03

### 🎉 Lanzamiento Inicial

#### Características Principales

- Escaneo de procesos sospechosos
- Análisis de archivos con YARA
- Monitoreo de red
- Escaneo de registro de Windows
- Archivos canary para detección de intrusiones
- Cuarentena automática de archivos peligrosos
- Modo monitor con dashboard en terminal
- Informes en HTML y JSON
- Watchdog para monitoreo de archivos en tiempo real

#### Módulos Incluidos

- `scanner/procesos.py`: Detección de procesos maliciosos
- `scanner/archivos.py`: Análisis de archivos con YARA
- `scanner/red.py`: Monitoreo de puertos
- `scanner/sistema.py`: Información del sistema
- `scanner/registro.py`: Análisis de registro
- `scanner/canary.py`: Archivos señuelo
- `utils/quarantine.py`: Sistema de cuarentena
- `utils/alertas.py`: Sistema de alertas con Rich
- `utils/informe.py`: Generación de reportes

#### Configuración

- `config.json`: Archivo de configuración central
- Rutas de monitoreo configurables
- Extensiones peligrosas personalizables
- Puertos sospechosos configurables
- Intervalos de escaneo ajustables

---

## Formato del Changelog

Este changelog sigue el formato de [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/lang/es/).

### Tipos de Cambios

- `✨ Nuevas Funcionalidades` - para nuevas características
- `🔧 Mejoras` - para cambios en funcionalidades existentes
- `🐛 Correcciones` - para corrección de bugs
- `🔒 Seguridad` - para cambios relacionados con seguridad
- `📦 Dependencias` - para cambios en dependencias
- `📝 Documentación` - para cambios en documentación
- `⚠️ Deprecado` - para funcionalidades que serán removidas
- `🗑️ Removido` - para funcionalidades removidas
