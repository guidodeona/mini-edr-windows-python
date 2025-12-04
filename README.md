# 🛡️ NEXO EDR - Sistema de Detección y Respuesta de Endpoint

<div align="center">

![Status](https://img.shields.io/badge/Estado-Activo-brightgreen)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/Licencia-MIT-yellow)

**Sistema de Ciberseguridad de Próxima Generación para Windows**

</div>

---

## 🎯 Características Principales

### 🔍 Detección Multi-Capa

- **Procesos**: Monitoreo de procesos sospechosos en tiempo real
- **Archivos**: Escáner de archivos con integración YARA
- **Red**: Detección de puertos abiertos anómalos
- **Registro**: Análisis de persistencia de malware
- **Canary (Honeypot)**: Archivos señuelo para detectar ransomware

### 🛡️ Respuesta Activa

- **Cuarentena Automática**: Los archivos maliciosos se aíslan inmediatamente
- **YARA Engine**: Detección basada en firmas de malware conocido
- **Watchdog Real-Time**: Monitoreo instantáneo de creación/modificación de archivos

### 🎨 Interfaz Avanzada

- **Dashboard en Vivo**: Visualización en tiempo real con Rich library
- **Alertas Codificadas por Color**: Rojo (Crítico), Amarillo (Advertencia), Verde (Seguro)
- **Paneles Interactivos**: Menús profesionales estilo "Command Center"

---

## 🚀 Instalación

### Requisitos

- Python 3.8 o superior
- Windows 10/11

### Pasos

```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/mini-edr.git
cd mini-edr

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Ejecutar
python main.py
```

---

## 📖 Uso

### Modo Interactivo

```bash
python main.py
```

Selecciona las opciones del menú para ejecutar escaneos específicos.

### Modo Monitor (Recomendado)

Activa el **Dashboard en Vivo** que monitorea tu sistema continuamente:

- Selecciona la opción **10** en el menú principal
- El sistema actualizará el estado cada 5 segundos
- Presiona `Ctrl+C` para detener

---

## ⚙️ Configuración

Edita `config.json` para personalizar:

```json
{
  "file_scanner": {
    "watch_paths": ["C:/Users/Public", "C:/Temp"],
    "dangerous_extensions": [".exe", ".dll", ".bat"],
    "auto_quarantine": true,
    "yara_rules_path": "rules/malware.yar"
  }
}
```

### Parámetros Clave

- `auto_quarantine`: `true` para mover archivos peligrosos automáticamente
- `yara_rules_path`: Ruta al archivo de reglas YARA personalizadas
- `monitor_interval`: Segundos entre escaneos en Modo Monitor

---

## 🧪 Pruebas

### Probar Cuarentena

1. Crea un archivo de prueba: `test_virus.bat`
2. Muévelo a una carpeta vigilada (ej. `Desktop`)
3. El sistema lo detectará y lo moverá a `quarantine/`

### Probar YARA

1. Crea un archivo `fake_malware.txt` con el texto: `mimikatz`
2. El motor YARA lo detectará como amenaza

---

## 📂 Estructura del Proyecto

```
mini-edr/
├── main.py              # Punto de entrada principal
├── config.json          # Configuración del sistema
├── requirements.txt     # Dependencias de Python
├── scanner/             # Módulos de escaneo
│   ├── procesos.py
│   ├── archivos.py      # ⭐ Con YARA y Watchdog
│   ├── red.py
│   ├── registro.py
│   └── canary.py
├── utils/               # Utilidades
│   ├── alertas.py       # ⭐ Interfaz Rich
│   ├── quarantine.py    # ⭐ Sistema de cuarentena
│   ├── logger.py
│   └── informe.py
├── rules/               # Reglas YARA
│   └── malware.yar      # ⭐ Firmas de malware
├── logs/                # Logs y reportes
└── quarantine/          # Archivos en cuarentena
```

---

## 🔥 Características Avanzadas

### YARA Rules

El sistema incluye reglas para detectar:

- Mimikatz
- Comandos PowerShell sospechosos
- Notas de ransomware
- Keyloggers
- Backdoors (Netcat)

Añade tus propias reglas en `rules/malware.yar`.

### Cuarentena

Los archivos en cuarentena se almacenan con timestamp:

```
quarantine/
  20251203_195500_virus.exe
  20251203_200130_malware.bat
```

Para restaurar un archivo, usa la opción **11** del menú.

---

## 🛠️ Desarrollo

### Añadir Nuevas Reglas YARA

```yara
rule MiReglaPersonalizada
{
    meta:
        description = "Detecta mi amenaza específica"
        severity = "high"

    strings:
        $s1 = "string_sospechoso"

    condition:
        $s1
}
```

### Personalizar Alertas

Edita `utils/alertas.py` para cambiar colores o iconos.

---

## 📊 Roadmap

- [x] Interfaz CLI profesional
- [x] Monitoreo en tiempo real
- [x] Integración YARA
- [x] Cuarentena automática
- [ ] Dashboard web opcional
- [ ] Integración con VirusTotal API
- [ ] Soporte Linux/macOS

---

## 📄 Licencia

MIT License - Libre para uso personal y comercial.

---

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Abre un **Issue** o envía un **Pull Request**.

---

## ⚠️ Disclaimer

Esta herramienta es para **fines educativos y de investigación**. Úsala bajo tu propia responsabilidad en sistemas de los que tengas autorización.

---

<div align="center">

**Hecho con ❤️ por el equipo NEXO**

[Reportar Bug](https://github.com/tu-usuario/mini-edr/issues) · [Solicitar Feature](https://github.com/tu-usuario/mini-edr/issues)

</div>
