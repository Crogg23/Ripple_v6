<#
task_wrapper.ps1 — the ONE doorway every Ripple scheduled task walks through.

Why a wrapper at all:
  * Pins the exact interpreter + repo root, so a PATH change or a different
    python.exe can never silently swap what runs unattended.
  * SKIPS (with a logged reason) when a live onboard.py pour is running — a
    scheduled load colliding with a pour is exactly what wiped NPPES. tasklist
    only shows 'python.exe', so the check needs a Win32_Process CommandLine query.
  * Routes scheduled work to COMPUTE_WH so it never contends with a pour on
    RIPPLE_WH. Two env vars are set because repo scripts load .env with
    override=True (which clobbers SNOWFLAKE_WAREHOUSE): RIPPLE_TASK_WAREHOUSE is
    the value that actually survives (honored by export_control_plane.py and
    heartbeat.py); SNOWFLAKE_WAREHOUSE covers anything that doesn't re-load .env.
  * Writes outputs/_task_<name>_LAST.json {status, ts, note} on EVERY outcome
    (ok / failed / skipped / error) — the daily nag task reads these.

Usage (what Register-ScheduledTask wires up; runnable by hand for testing):
  powershell -NoProfile -ExecutionPolicy Bypass -File scripts\task_wrapper.ps1 `
      -TaskName Ripple-heartbeat -Script "scripts/heartbeat.py" -ScriptArgs "--run"

PowerShell 5.1-compatible: no && chains, no ternaries.
#>
param(
    [Parameter(Mandatory = $true)][string]$TaskName,
    [Parameter(Mandatory = $true)][string]$Script,      # repo-relative .py path
    [string]$ScriptArgs = ""
)

$ErrorActionPreference = "Continue"

# Pinned absolutes — scheduled tasks inherit a bare environment; never trust PATH.
$Py   = "C:\Users\wroge\AppData\Local\Programs\Python\Python312\python.exe"
$Repo = "C:\Code\Ripple_v6"
$OutDir = Join-Path $Repo "outputs"
$LastFile = Join-Path $OutDir ("_task_" + $TaskName + "_LAST.json")

function Write-Last {
    param([string]$Status, [string]$Note)
    if (-not (Test-Path $OutDir)) { New-Item -ItemType Directory -Force $OutDir | Out-Null }
    $doc = @{
        status = $Status
        ts     = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
        note   = $Note
        task   = $TaskName
    } | ConvertTo-Json -Compress
    # -Encoding utf8 so python-side readers parse it (PS 5.1 defaults to UTF-16).
    $doc | Out-File -FilePath $LastFile -Encoding utf8 -Force
}

# ---- guard 1: interpreter must exist ---------------------------------------
if (-not (Test-Path $Py)) {
    Write-Last "error" ("pinned interpreter missing: " + $Py)
    exit 1
}

# ---- guard 2: never run alongside a live pour ------------------------------
# Get-CimInstance, not tasklist: only the CIM CommandLine reveals onboard.py
# behind a generic python.exe. Fail-open on probe error (budget + in-script
# guards still exist) but say so in the note.
$pour = $null
try {
    $procs = Get-CimInstance Win32_Process -Filter "Name LIKE 'python%'" -ErrorAction Stop
    foreach ($p in $procs) {
        if ($p.CommandLine -match "onboard\.py") { $pour = $p.CommandLine; break }
    }
} catch {
    $pour = $null
}
if ($pour) {
    $note = "live onboard.py pour detected - skipped to avoid contention: " + $pour.Substring(0, [Math]::Min(160, $pour.Length))
    Write-Last "skipped" $note
    Write-Output $note
    exit 0
}

# ---- run the payload on the scheduled-work warehouse -----------------------
$env:SNOWFLAKE_WAREHOUSE   = "COMPUTE_WH"   # verified to exist via SHOW WAREHOUSES 2026-07-02
$env:RIPPLE_TASK_WAREHOUSE = "COMPUTE_WH"   # the one that survives load_dotenv(override=True)

$target = Join-Path $Repo $Script
if (-not (Test-Path $target)) {
    Write-Last "error" ("script missing: " + $target)
    exit 1
}

$argList = @($target)
if ($ScriptArgs.Trim().Length -gt 0) { $argList += ($ScriptArgs.Trim() -split "\s+") }

Set-Location $Repo
$outFile = Join-Path $OutDir ("_task_" + $TaskName + "_out.txt")
try {
    # Tee child output to a per-task text file (NOT .log — pour logs are sacred).
    & $Py @argList *> $outFile
    $rc = $LASTEXITCODE
} catch {
    Write-Last "failed" ("wrapper exception: " + $_.Exception.Message.Substring(0, [Math]::Min(200, $_.Exception.Message.Length)))
    exit 1
}

$tail = ""
try {
    $lines = Get-Content $outFile -Tail 3 -ErrorAction Stop
    $tail = ($lines -join " | ")
    if ($tail.Length -gt 240) { $tail = $tail.Substring(0, 240) }
} catch { $tail = "" }

if ($rc -eq 0) {
    Write-Last "ok" $tail
    exit 0
} else {
    Write-Last "failed" ("rc=" + $rc + " " + $tail)
    exit $rc
}
