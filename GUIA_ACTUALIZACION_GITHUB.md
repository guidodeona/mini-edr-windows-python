# 🚀 Guía para Actualizar el Proyecto en GitHub

## 📋 Resumen de Cambios Implementados

Se han agregado las siguientes mejoras al proyecto NEXO EDR v2.0:

### ✨ Nuevos Archivos Creados:

1. `utils/database.py` - Base de datos SQLite para histórico de eventos
2. `utils/virustotal.py` - Integración con VirusTotal API
3. `utils/process_killer.py` - Gestión avanzada de procesos
4. `utils/notifications.py` - Sistema de notificaciones (Discord/Slack)
5. `web_dashboard.py` - Dashboard web interactivo con Flask
6. `.env.example` - Plantilla de variables de entorno
7. `.gitignore` - Exclusiones de Git actualizadas
8. `CHANGELOG.md` - Historial de cambios del proyecto

### 🔧 Archivos Modificados:

1. `main.py` - Nuevas opciones de menú y funcionalidades
2. `scanner/procesos.py` - Auto-kill y logging a BD
3. `config.json` - Nuevas configuraciones
4. `requirements.txt` - Nuevas dependencias
5. `README.md` - Documentación completa actualizada

---

## 📝 Pasos para Actualizar en GitHub

### Opción 1: Actualización Completa (Recomendada)

Ejecuta estos comandos en orden desde la carpeta del proyecto:

```powershell
# 1. Primero, sincronizar con el repositorio remoto
git pull origin main

# 2. Agregar TODOS los archivos nuevos y modificados
git add .

# 3. Crear un commit con un mensaje descriptivo
git commit -m "🚀 v2.0: Mejoras mayores - VirusTotal, Auto-Kill, Dashboard Web, Notificaciones y BD"

# 4. Subir los cambios a GitHub
git push origin main
```

### Opción 2: Actualización Paso a Paso (Más Control)

Si prefieres tener más control sobre qué archivos subir:

```powershell
# 1. Sincronizar con el repositorio remoto
git pull origin main

# 2. Agregar archivos nuevos uno por uno
git add utils/database.py
git add utils/virustotal.py
git add utils/process_killer.py
git add utils/notifications.py
git add web_dashboard.py
git add .env.example
git add .gitignore
git add CHANGELOG.md

# 3. Agregar archivos modificados
git add main.py
git add scanner/procesos.py
git add config.json
git add requirements.txt
git add README.md

# 4. Verificar qué archivos se van a subir
git status

# 5. Crear el commit
git commit -m "🚀 v2.0: Mejoras mayores - VirusTotal, Auto-Kill, Dashboard Web, Notificaciones y BD"

# 6. Subir a GitHub
git push origin main
```

### Opción 3: Crear una Rama Nueva (Más Seguro)

Si quieres probar primero en una rama separada:

```powershell
# 1. Sincronizar
git pull origin main

# 2. Crear y cambiar a una nueva rama
git checkout -b feature/v2.0-improvements

# 3. Agregar todos los cambios
git add .

# 4. Commit
git commit -m "🚀 v2.0: Mejoras mayores - VirusTotal, Auto-Kill, Dashboard Web, Notificaciones y BD"

# 5. Subir la nueva rama
git push origin feature/v2.0-improvements

# 6. Luego puedes crear un Pull Request en GitHub
# O fusionar directamente:
git checkout main
git merge feature/v2.0-improvements
git push origin main
```

---

## 🔍 Verificación Post-Actualización

Después de hacer push, verifica en GitHub:

1. **Ve a tu repositorio**: https://github.com/guidodeona/mini-edr-windows-python
2. **Verifica que aparezcan**:
   - ✅ Los 8 archivos nuevos
   - ✅ Los 5 archivos modificados
   - ✅ El README actualizado se muestra correctamente
   - ✅ El .gitignore está funcionando (no se subieron .env, logs, etc.)

---

## 📦 Crear un Release en GitHub (Opcional pero Recomendado)

Para marcar esta versión como v2.0:

1. Ve a tu repositorio en GitHub
2. Click en "Releases" (lado derecho)
3. Click en "Create a new release"
4. Tag version: `v2.0.0`
5. Release title: `🚀 NEXO EDR v2.0 - Major Update`
6. Descripción: Copia el contenido del CHANGELOG.md para v2.0
7. Click en "Publish release"

---

## ⚠️ Notas Importantes

### Archivos que NO se subirán (están en .gitignore):

- `.env` (contiene API keys sensibles)
- `logs/*.log` (archivos de log)
- `logs/*.db` (base de datos con eventos)
- `quarantine/*` (archivos en cuarentena)
- `__pycache__/` (archivos compilados de Python)

### Antes de Hacer Push:

- ✅ Asegúrate de NO tener API keys reales en config.json
- ✅ Verifica que .env no esté incluido
- ✅ Revisa que no haya información sensible en los commits

---

## 🆘 Solución de Problemas

### Error: "Your branch is behind"

```powershell
git pull origin main
# Luego continúa con git add, commit, push
```

### Error: "Merge conflict"

```powershell
# Resolver conflictos manualmente en los archivos marcados
# Luego:
git add .
git commit -m "Resolver conflictos de merge"
git push origin main
```

### Error: "Permission denied"

```powershell
# Verifica tus credenciales de GitHub
# O usa GitHub Desktop como alternativa
```

### Quiero deshacer cambios antes de commit

```powershell
git restore <archivo>  # Para un archivo específico
git restore .          # Para todos los archivos
```

---

## 🎉 ¡Listo!

Una vez completados estos pasos, tu proyecto estará actualizado en GitHub con todas las nuevas funcionalidades de la versión 2.0.

**Nuevas funcionalidades disponibles:**

- 🦠 Integración con VirusTotal
- ⚔️ Auto-kill de procesos maliciosos
- 💾 Base de datos SQLite
- 🌐 Dashboard web interactivo
- 🔔 Notificaciones a Discord/Slack
- 📊 Estadísticas y análisis forense

---

**¿Necesitas ayuda?** Revisa la documentación en README.md o contacta al desarrollador.
