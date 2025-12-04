# ESCENARIO 2: Simulación de Keylogger
# Simula archivos y scripts típicos de keyloggers

Write-Host "`n⌨️  SIMULACIÓN DE KEYLOGGER - MODO SEGURO`n" -ForegroundColor Magenta

$testFolder = "$env:USERPROFILE\Desktop\KEYLOGGER_TEST"
New-Item -Path $testFolder -ItemType Directory -Force | Out-Null

Write-Host "[FASE 1] Creando keylogger simulado en Python..." -ForegroundColor Yellow

$pythonKeylogger = @"
# Fake Keylogger - Educational Purpose Only
import ctypes
from ctypes import wintypes

# Windows API functions used by real keyloggers
user32 = ctypes.WinDLL('user32', use_last_error=True)

# GetAsyncKeyState - Detecta teclas presionadas
GetAsyncKeyState = user32.GetAsyncKeyState
GetAsyncKeyState.argtypes = [ctypes.c_int]
GetAsyncKeyState.restype = ctypes.c_short

# GetForegroundWindow - Obtiene ventana activa
GetForegroundWindow = user32.GetForegroundWindow
GetForegroundWindow.argtypes = []
GetForegroundWindow.restype = wintypes.HWND

# SetWindowsHookEx - Hook de teclado
SetWindowsHookEx = user32.SetWindowsHookExA

class Keylogger:
    def __init__(self):
        self.log_file = "keystroke_log.txt"
    
    def capture_keystrokes(self):
        # Código que captura teclas (SIMULADO)
        print("[KEYLOG] Capturing keystrokes...")
    
    def get_active_window(self):
        window = GetForegroundWindow()
        return window

# Si esto fuera real, aquí guardaría las teclas
log = Keylogger()
log.capture_keystrokes()
"@

$pythonKeylogger | Out-File "$testFolder\keylogger.py" -Encoding UTF8

Write-Host "[FASE 2] Creando log falso de teclas capturadas..." -ForegroundColor Yellow

$fakeLog = @"
[2025-12-03 15:23:45] Window: Google Chrome - Gmail
Keys: usuario@gmail.com
[TAB]
Keys: MiContraseña123!
[ENTER]

[2025-12-03 15:25:12] Window: Notepad
Keys: Información confidencial de la empresa...

[2025-12-03 15:30:00] Window: cmd.exe
Keys: net user Administrator P@ssw0rd
"@

$fakeLog | Out-File "$testFolder\keystroke_log.txt"

Write-Host "[FASE 3] Creando ejecutable simulado (.exe)..." -ForegroundColor Yellow

# Archivo que simula ser un ejecutable (solo texto)
$fakeExe = @"
MZ_FAKE_EXECUTABLE_HEADER
This is not a real executable, just a text file.
But it has .exe extension to trigger EDR detection.

Contains keylogger indicators:
- GetAsyncKeyState
- SetWindowsHookEx  
- Keystroke logging functionality
"@

$fakeExe | Out-File "$testFolder\windows_update.exe"

Write-Host "[FASE 4] Script de instalación automática..." -ForegroundColor Yellow

$autoInstall = @"
@echo off
echo Installing Windows Update Service...

:: Copiar a carpeta del sistema
copy /y keylogger.py %APPDATA%\Microsoft\Windows\svchost.py

:: Crear tarea programada para ejecutar al inicio
schtasks /create /tn "WindowsUpdateService" /tr "python %APPDATA%\Microsoft\Windows\svchost.py" /sc onlogon /f

:: Ocultar archivo
attrib +h +s %APPDATA%\Microsoft\Windows\svchost.py

echo Installation complete. System will restart.
shutdown /r /t 60
"@

$autoInstall | Out-File "$testFolder\install_update.bat"

Write-Host "`n✅ Simulación creada en: $testFolder" -ForegroundColor Green
Write-Host "`n🎯 TU EDR DEBERÍA DETECTAR:" -ForegroundColor Cyan
Write-Host "   • keylogger.py (YARA: Keylogger_Indicators)" -ForegroundColor White
Write-Host "   • windows_update.exe (Extensión peligrosa)" -ForegroundColor White
Write-Host "   • install_update.bat (YARA: Suspicious_Batch_Commands)" -ForegroundColor White
Write-Host "   • keystroke_log.txt (puede activar reglas personalizadas)`n" -ForegroundColor White

Write-Host "💡 SUGERENCIA: Agrega '.py' a dangerous_extensions en config.json`n" -ForegroundColor Yellow

Start-Process explorer.exe $testFolder
