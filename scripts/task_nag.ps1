<#
task_nag.ps1 — the daily "is anything silently broken?" alarm.

Reads every outputs\_task_*_LAST.json the wrapper writes and pops a VISIBLE
MessageBox listing tasks that either FAILED on their last run or haven't
succeeded in more than 2x their expected cadence (a sleeping laptop that missed
a week of triggers looks exactly like this). No problems -> no popup, silent exit.

Registered with -LogonType Interactive (NOT S4U like the workers): an S4U session
has no desktop, so its MessageBox would render into the void. Interactive means
the nag only fires when Chris is logged in — which is the only time a popup is
worth anything anyway.

PowerShell 5.1-compatible: no && chains, no ternaries.
#>
$ErrorActionPreference = "Continue"

$Repo   = "C:\Code\Ripple_v6"
$OutDir = Join-Path $Repo "outputs"

# Expected cadence per task, in hours. Stale threshold = 2x this.
$Cadence = @{
    "Ripple-heartbeat" = 1
    "Ripple-DR-export" = 168
    "Ripple-refresh"   = 168
}

$problems = @()
$now = (Get-Date).ToUniversalTime()

$files = Get-ChildItem -Path $OutDir -Filter "_task_*_LAST.json" -ErrorAction SilentlyContinue
foreach ($f in $files) {
    if ($f.Name -eq "_task_Ripple-nag_LAST.json") { continue }   # don't nag about the nag
    try {
        $doc = Get-Content $f.FullName -Raw | ConvertFrom-Json
    } catch {
        $problems += ($f.Name + ": unreadable status file")
        continue
    }
    $name = $doc.task
    if (-not $name) { $name = $f.Name -replace "^_task_", "" -replace "_LAST\.json$", "" }

    if ($doc.status -eq "failed" -or $doc.status -eq "error") {
        $problems += ($name + ": last run " + $doc.status.ToUpper() + " at " + $doc.ts + " - " + $doc.note)
        continue
    }
    # skipped (pour running) is expected behavior, but it still counts toward
    # staleness below — a task skipped for two weeks straight IS a problem.
    if ($Cadence.ContainsKey($name)) {
        $limitH = 2 * $Cadence[$name]
        $ageH = $null
        try {
            $ts = [DateTime]::Parse($doc.ts, $null, [System.Globalization.DateTimeStyles]::AdjustToUniversal)
            $ageH = ($now - $ts).TotalHours
        } catch { $ageH = $null }
        $isStale = $false
        if ($null -eq $ageH) { $isStale = $true }
        elseif ($ageH -gt $limitH) { $isStale = $true }
        if ($isStale -and $doc.status -ne "ok") {
            $problems += ($name + ": no successful run recorded; last status '" + $doc.status + "' at " + $doc.ts)
        } elseif ($null -ne $ageH -and $ageH -gt $limitH) {
            $problems += ($name + ": STALE - last outcome " + [Math]::Round($ageH, 1) + "h ago (cadence " + $Cadence[$name] + "h, limit " + $limitH + "h)")
        }
    }
}

# Tasks that have NEVER written a status file are the sneakiest failure mode.
foreach ($name in $Cadence.Keys) {
    $expected = Join-Path $OutDir ("_task_" + $name + "_LAST.json")
    if (-not (Test-Path $expected)) {
        $problems += ($name + ": never ran (no status file) - check Get-ScheduledTask " + $name)
    }
}

# Record our own outcome for the audit trail.
$self = @{
    status = "ok"
    ts     = $now.ToString("yyyy-MM-ddTHH:mm:ssZ")
    note   = ("checked " + $files.Count + " status files, " + $problems.Count + " problems")
    task   = "Ripple-nag"
} | ConvertTo-Json -Compress
$self | Out-File -FilePath (Join-Path $OutDir "_task_Ripple-nag_LAST.json") -Encoding utf8 -Force

if ($problems.Count -gt 0) {
    $msg = "Ripple scheduled tasks need attention:`n`n" + ($problems -join "`n")
    Write-Output $msg
    try {
        Add-Type -AssemblyName System.Windows.Forms
        [System.Windows.Forms.MessageBox]::Show($msg, "Ripple task nag",
            [System.Windows.Forms.MessageBoxButtons]::OK,
            [System.Windows.Forms.MessageBoxIcon]::Warning) | Out-Null
    } catch {
        Write-Output "(MessageBox unavailable - console output only)"
    }
    exit 1
}
Write-Output "all scheduled tasks healthy"
exit 0
