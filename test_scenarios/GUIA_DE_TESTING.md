# 🧪 GUÍA DE TESTING - NEXO EDR

## 📁 Escenarios de Prueba Creados

He creado 4 escenarios de ataque simulados para probar todas las capacidades de tu EDR:

### 🦠 **Escenario 1: Ransomware**

**Archivo:** `scenario_1_ransomware.ps1`
**Simula:** Ataque de ransomware que encripta archivos
**Detecta:**

- Notas de rescate (YARA: Ransomware_Note)
- Scripts de eliminación de backups (YARA: Suspicious_Batch_Commands)
- Archivos .locked

**Ejecutar:**

```powershell
cd C:\Users\Memotito\OneDrive\Desktop\mini-edr\test_scenarios
.\scenario_1_ransomware.ps1
```

---

### ⌨️ **Escenario 2: Keylogger**

**Archivo:** `scenario_2_keylogger.ps1`
**Simula:** Malware que captura teclas y roba credenciales
**Detecta:**

- Código Python con APIs de Windows (YARA: Keylogger_Indicators)
- Archivos .exe sospechosos
- Logs de teclas capturadas

**Ejecutar:**

```powershell
.\scenario_2_keylogger.ps1
```

---

### 🚪 **Escenario 3: Backdoor**

**Archivo:** `scenario_3_backdoor.ps1`
**Simula:** Acceso remoto no autorizado via Netcat
**Detecta:**

- Scripts PowerShell maliciosos (YARA: Suspicious_PowerShell_Download)
- Comandos Netcat (YARA: Backdoor_Netcat)
- Scripts de persistencia

**Ejecutar:**

```powershell
.\scenario_3_backdoor.ps1
```

---

### 🎯 **MASTER TEST SUITE**

**Archivo:** `MASTER_TEST_SUITE.ps1`
**Descripción:** Suite completa de testing automatizado
**Tests incluidos:**

1. ✓ YARA Detection Engine
2. ✓ Dangerous Extension Detection
3. ✓ Watchdog Real-Time Monitoring
4. ✓ Quarantine System
5. ✓ Performance Stress Test (50 archivos)

**Ejecutar:**

```powershell
# Modo rápido (tests básicos)
.\MASTER_TEST_SUITE.ps1 -Quick

# Modo completo (todos los tests)
.\MASTER_TEST_SUITE.ps1 -Full

# Modo interactivo (menú)
.\MASTER_TEST_SUITE.ps1
```

---

## 🎬 **Flujo de Testing Recomendado**

### **Opción A: Testing Rápido (5 minutos)**

1. Ejecuta el MASTER TEST SUITE en modo rápido:

   ```powershell
   cd test_scenarios
   .\MASTER_TEST_SUITE.ps1 -Quick
   ```

2. Inicia tu EDR:

   ```powershell
   cd ..
   python main.py
   ```

3. Selecciona **Opción 2** (Escaneo Completo)

4. Verifica los resultados:
   - Consola: alertas en rojo
   - Carpeta `quarantine/`: archivos aislados
   - `logs/informe_*.txt`: reporte detallado

---

### **Opción B: Testing en Tiempo Real (10 minutos)**

1. Inicia tu EDR primero:

   ```powershell
   python main.py
   ```

2. Selecciona **Opción 10** (Modo Monitor)

3. En otra terminal PowerShell, ejecuta:

   ```powershell
   cd test_scenarios
   .\scenario_1_ransomware.ps1
   ```

4. **Observa el dashboard** - las alertas aparecerán instantáneamente

5. Repite con los otros escenarios (2 y 3)

---

### **Opción C: Testing Completo (15 minutos)**

```powershell
# 1. Ejecutar suite completa
cd test_scenarios
.\MASTER_TEST_SUITE.ps1 -Full

# 2. Iniciar EDR
cd ..
python main.py

# 3. Probar cada funcionalidad
# - Opción 4: Escaneo de archivos
# - Opción 10: Modo Monitor
# - Opción 11: Ver cuarentena

# 4. Ejecutar escenarios individuales
cd test_scenarios
.\scenario_1_ransomware.ps1
.\scenario_2_keylogger.ps1
.\scenario_3_backdoor.ps1
```

---

## 📊 **Resultados Esperados**

### **Detecciones YARA:**

- ✓ Mimikatz_Strings
- ✓ Suspicious_PowerShell_Download
- ✓ Ransomware_Note
- ✓ Suspicious_Batch_Commands
- ✓ Keylogger_Indicators
- ✓ Backdoor_Netcat

### **Archivos en Cuarentena:**

Deberías ver entre **15-70 archivos** en cuarentena dependiendo del test ejecutado.

### **Logs Generados:**

- `logs/actividad.log` - Registro completo de eventos
- `logs/informe_*.txt` - Reporte de escaneo
- `logs/informe_*.json` - Datos en formato JSON

---

## 🔥 **Tests Avanzados**

### **Test de Evasión (Desafío):**

Intenta crear un archivo malicioso que NO sea detectado:

```powershell
# ¿Este pasará el EDR?
"NOT_MIMIKATZ_JUST_RANDOM_TEXT" > Desktop\maybe_safe.exe
```

### **Test de Falsos Positivos:**

Verifica que archivos legítimos no sean detectados:

```powershell
# Archivo completamente seguro
"Este es mi documento de trabajo" > Desktop\reporte_2025.txt
```

### **Test de Performance:**

```powershell
# Crear 100 archivos maliciosos simultáneamente
1..100 | ForEach-Object {
    "mimikatz" > "Desktop\threat_$_.exe"
}
```

---

## ⚠️ **Importante**

- Todos estos scripts son **100% seguros** - solo crean archivos de texto
- No ejecutan código malicioso real
- Puedes eliminar todas las carpetas de prueba cuando termines:
  ```powershell
  Remove-Item "$env:USERPROFILE\Desktop\*_TEST" -Recurse -Force
  ```

---

## 🎓 **Aprendizaje**

Estos escenarios están basados en **ataques reales** documentados:

- **Ransomware:** WannaCry, Locky, Ryuk
- **Keylogger:** Olympic Vision, Agent Tesla
- **Backdoor:** Cobalt Strike, Meterpreter

Tu EDR ahora puede detectar patrones similares a herramientas profesionales como:

- CrowdStrike Falcon
- SentinelOne
- Microsoft Defender ATP

---

## 📞 **Soporte**

Si algún test falla:

1. Verifica que `yara-python` esté instalado
2. Confirma que `config.json` tenga `auto_quarantine: true`
3. Revisa que las rutas en `watch_paths` existan
4. Consulta `logs/actividad.log` para debugging

---

**¡Buena suerte con el testing!** 🚀
