$ErrorActionPreference = "Stop"
$TaskName = "TradingBotVaultWeeklyReporter"

if (Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue) {
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
    Write-Host "Autostart rimosso: $TaskName"
} else {
    Write-Host "Task non presente: $TaskName"
}

$StartupDir = [Environment]::GetFolderPath("Startup")
$ShortcutPath = Join-Path $StartupDir "TradingBotVaultWeeklyReporter.lnk"
if (Test-Path $ShortcutPath) {
    Remove-Item $ShortcutPath -Force
    Write-Host "Collegamento Startup rimosso: $ShortcutPath"
}
