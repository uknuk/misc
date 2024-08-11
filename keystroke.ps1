# $job = Start-Job -FilePath "bin/keystroke.ps1"
# get-job $job.id

$interval = 5

Add-Type -AssemblyName System.Windows.Forms

while ($true) {
    [System.Windows.Forms.SendKeys]::SendWait("{SCROLLLOCK}")
    Start-Sleep -Seconds ($interval * 60)
}
