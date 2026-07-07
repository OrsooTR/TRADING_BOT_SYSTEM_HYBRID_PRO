$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$Launcher = Join-Path $ProjectRoot "start_vault_weekly_reporter.bat"
$TaskName = "TradingBotVaultWeeklyReporter"

if (-not (Test-Path $Launcher)) {
    throw "Launcher non trovato: $Launcher"
}

try {
    $Action = New-ScheduledTaskAction -Execute $Launcher -WorkingDirectory $ProjectRoot
    $Trigger = New-ScheduledTaskTrigger -AtLogOn
    $Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -MultipleInstances IgnoreNew

    Register-ScheduledTask `
        -TaskName $TaskName `
        -Action $Action `
        -Trigger $Trigger `
        -Settings $Settings `
        -Description "Watcher del vault e rendicontazione settimanale automatica del progetto trading bot." `
        -Force | Out-Null

    Start-ScheduledTask -TaskName $TaskName
    Write-Host "Autostart installato tramite Operazioni Pianificate: $TaskName"
} catch {
    $StartupDir = [Environment]::GetFolderPath("Startup")
    $ShortcutPath = Join-Path $StartupDir "TradingBotVaultWeeklyReporter.lnk"
    $Shell = New-Object -ComObject WScript.Shell
    $Shortcut = $Shell.CreateShortcut($ShortcutPath)
    $Shortcut.TargetPath = $Launcher
    $Shortcut.WorkingDirectory = $ProjectRoot
    $Shortcut.Description = "Watcher del vault e rendicontazione settimanale automatica."
    $Shortcut.Save()

    Start-Process -FilePath $Launcher -WorkingDirectory $ProjectRoot -WindowStyle Hidden
    Write-Host "Operazioni Pianificate non disponibili. Autostart installato nella cartella Startup utente: $ShortcutPath"
}
