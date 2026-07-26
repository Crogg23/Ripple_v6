# Gap Acquisition Campaign watchdog: relaunch any incomplete detached loader.
# A loader is "done" when its run log ends with DONE (or ROWS= for one-shot loads).
# Safe because every loader is checkpoint-resumable.
$py = "C:\Code\Ripple_v6\.venv\Scripts\python.exe"
$wd = "C:\Code\Ripple_v6"
$jobs = @(
    @{n = "faers";     s = "scripts\fda_faers_load.py";            done = "^DONE" },
    @{n = "neiss";     s = "scripts\cpsc_neiss_load.py";           done = "^DONE" },
    @{n = "sec13f";    s = "scripts\sec_13f_load.py";              done = "^DONE" },
    @{n = "cldockets"; s = "scripts\courtlistener_dockets_load.py"; done = "ROWS=" },
    @{n = "arcos";     s = "scripts\dea_arcos_full_load.py";       done = "ROWS=" }
)
while ($true) {
    $procs = Get-CimInstance Win32_Process -Filter "Name='python.exe'" |
        Select-Object -ExpandProperty CommandLine
    $allDone = $true
    foreach ($j in $jobs) {
        $log = Get-ChildItem "C:\Code\Ripple_v6\logs\$($j.n)_run*.log" -ErrorAction SilentlyContinue |
            Sort-Object LastWriteTime | Select-Object -Last 1
        $isDone = $false
        if ($log) { $isDone = [bool](Select-String -Path $log.FullName -Pattern $j.done -Quiet) }
        if ($isDone) { continue }
        $allDone = $false
        $running = $procs | Where-Object { $_ -match [regex]::Escape($j.s) }
        if (-not $running) {
            $stamp = Get-Date -Format "HHmmss"
            Start-Process -FilePath $py -ArgumentList @("-u", $j.s, "--run") -WorkingDirectory $wd `
                -WindowStyle Hidden `
                -RedirectStandardOutput "C:\Code\Ripple_v6\logs\$($j.n)_run_w$stamp.log" `
                -RedirectStandardError  "C:\Code\Ripple_v6\logs\$($j.n)_err_w$stamp.log"
            Add-Content "C:\Code\Ripple_v6\logs\watchdog.log" "$(Get-Date -Format s) relaunched $($j.n)"
        }
    }
    if ($allDone) {
        Add-Content "C:\Code\Ripple_v6\logs\watchdog.log" "$(Get-Date -Format s) all loaders done; watchdog exiting"
        break
    }
    Start-Sleep -Seconds 600
}
