<#
register_windows_tasks.ps1 — register (or remove) the Ripple keep-alive scheduled tasks.

    powershell -NoProfile -ExecutionPolicy Bypass -File scripts\register_windows_tasks.ps1
    powershell -NoProfile -ExecutionPolicy Bypass -File scripts\register_windows_tasks.ps1 -Unregister

Registers four tasks, all routed through scripts\task_wrapper.ps1 (pinned
interpreter, pour-collision skip, COMPUTE_WH routing, _task_<name>_LAST.json
status drops) except the nag, which is pure PowerShell:

    Ripple-DR-export   weekly  Sun 09:00  export_control_plane.py --apply
    Ripple-refresh     weekly  Sat 08:00  bridge_fuel_load.py --spec all --refresh --run
    Ripple-heartbeat   hourly             heartbeat.py --run
    Ripple-nag         daily   18:00      task_nag.ps1 (popup on failed/stale tasks)

Why Register-ScheduledTask and NOT schtasks.exe: schtasks cannot express
StartWhenAvailable (missed-start catch-up). This laptop sleeps; without
catch-up every trigger that lands during sleep is silently skipped forever —
the exact failure mode the nag exists to catch. -WakeToRun is set on the two
weekly jobs (worth waking the machine for) but not the hourly heartbeat
(waking a laptop 24x/day is battery abuse; StartWhenAvailable catches it up
on wake instead).

-LogonType choice, documented per the plan:
  * Workers (DR-export / refresh / heartbeat) run as S4U: no password stored
    anywhere, and the task runs whether or not Chris is logged on. S4U tokens
    can't touch network shares — irrelevant here, everything is local + HTTPS.
  * Ripple-nag runs Interactive: an S4U session has no desktop, so its
    MessageBox would be invisible. Interactive = fires only when logged in,
    which is the only time a popup can be seen anyway.
  * ELEVATION: registering an S4U principal requires an elevated shell. From a
    normal shell this script FALLS BACK to Interactive (tasks then run only
    while logged on — on a personal laptop that is nearly always) and tells you.
    Re-run once from an elevated PowerShell to upgrade the workers to S4U.

PowerShell 5.1-compatible: no && chains, no ternaries.
#>
param(
    [switch]$Unregister
)

$ErrorActionPreference = "Stop"

$Repo    = "C:\Code\Ripple_v6"
$Wrapper = Join-Path $Repo "scripts\task_wrapper.ps1"
$NagPs1  = Join-Path $Repo "scripts\task_nag.ps1"
$PsExe   = Join-Path $env:SystemRoot "System32\WindowsPowerShell\v1.0\powershell.exe"

$TaskNames = @("Ripple-DR-export", "Ripple-refresh", "Ripple-heartbeat", "Ripple-nag")

if ($Unregister) {
    foreach ($name in $TaskNames) {
        try {
            Unregister-ScheduledTask -TaskName $name -Confirm:$false -ErrorAction Stop
            Write-Output ("unregistered: " + $name)
        } catch {
            Write-Output ("not present:  " + $name)
        }
    }
    exit 0
}

function New-WrapperAction {
    param([string]$TaskName, [string]$Script, [string]$ScriptArgs)
    $arg = "-NoProfile -NonInteractive -ExecutionPolicy Bypass -File `"$Wrapper`" " +
           "-TaskName $TaskName -Script `"$Script`" -ScriptArgs `"$ScriptArgs`""
    return New-ScheduledTaskAction -Execute $PsExe -Argument $arg -WorkingDirectory $Repo
}

# StartWhenAvailable = run as soon as possible after a missed trigger (the sleep fix).
$settingsWake   = New-ScheduledTaskSettingsSet -StartWhenAvailable -WakeToRun `
                    -ExecutionTimeLimit (New-TimeSpan -Hours 6) -MultipleInstances IgnoreNew
$settingsNoWake = New-ScheduledTaskSettingsSet -StartWhenAvailable `
                    -ExecutionTimeLimit (New-TimeSpan -Hours 3) -MultipleInstances IgnoreNew

# S4U: passwordless, runs without logon. Interactive: has a desktop for the popup.
$s4u         = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType S4U -RunLevel Limited
$interactive = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive -RunLevel Limited

function Register-RippleWorker {
    # Try the S4U principal first (runs without logon); registering S4U needs an
    # elevated shell, so from a normal shell we fall back to Interactive and say so.
    param([string]$Name, $Action, $Trigger, $Settings, [string]$Description, [string]$When)
    try {
        Register-ScheduledTask -TaskName $Name -Force -Action $Action -Trigger $Trigger `
            -Settings $Settings -Principal $s4u -Description $Description -ErrorAction Stop | Out-Null
        Write-Output ("registered: " + $Name + " (" + $When + ", S4U)")
    } catch {
        Register-ScheduledTask -TaskName $Name -Force -Action $Action -Trigger $Trigger `
            -Settings $Settings -Principal $interactive -Description $Description -ErrorAction Stop | Out-Null
        Write-Output ("registered: " + $Name + " (" + $When + ", Interactive FALLBACK - S4U needs an elevated shell; re-run elevated to upgrade)")
    }
}

# --- Ripple-DR-export: weekly control-plane DR export (the guard for the worst failure)
$trigDr = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Sunday -At 09:00
Register-RippleWorker -Name "Ripple-DR-export" `
    -Action (New-WrapperAction "Ripple-DR-export" "scripts/export_control_plane.py" "--apply") `
    -Trigger $trigDr -Settings $settingsWake `
    -Description "Ripple: weekly off-Snowflake export of non-rebuildable control-plane tables (survives a DROP)." `
    -When "weekly Sun 09:00, wake+catch-up"

# --- Ripple-refresh: weekly deterministic re-ingest of due sources.
# --spec all is load-bearing: without it bridge_fuel_load just LISTS specs and
# exits 0 (a silent no-op the nag would happily call healthy). --refresh makes
# every spec SHA-gated, so unchanged sources cost one HEAD/hash, not a reload.
$trigRf = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Saturday -At 08:00
Register-RippleWorker -Name "Ripple-refresh" `
    -Action (New-WrapperAction "Ripple-refresh" "scripts/bridge_fuel_load.py" "--spec all --refresh --run") `
    -Trigger $trigRf -Settings $settingsWake `
    -Description "Ripple: weekly deterministic bridge-fuel refresh of due/overdue sources." `
    -When "weekly Sat 08:00, wake+catch-up"

# --- Ripple-heartbeat: hourly tick (LINK/MEASURE/RECONCILE cadences live in the script)
# 5.1 has no -Hourly switch: a Once trigger with an hourly repetition is the idiom.
$trigHb = New-ScheduledTaskTrigger -Once -At (Get-Date).Date.AddHours(7) `
    -RepetitionInterval (New-TimeSpan -Hours 1) -RepetitionDuration (New-TimeSpan -Days 3650)
Register-RippleWorker -Name "Ripple-heartbeat" `
    -Action (New-WrapperAction "Ripple-heartbeat" "scripts/heartbeat.py" "--run") `
    -Trigger $trigHb -Settings $settingsNoWake `
    -Description "Ripple: hourly heartbeat tick (run-if-overdue tiers; budget-gated; pour-aware)." `
    -When "hourly, catch-up no wake"

# --- Ripple-nag: daily visible alert on failed / stale tasks
$trigNag = New-ScheduledTaskTrigger -Daily -At 18:00
$nagArg = "-NoProfile -ExecutionPolicy Bypass -File `"$NagPs1`""
Register-ScheduledTask -TaskName "Ripple-nag" -Force `
    -Action (New-ScheduledTaskAction -Execute $PsExe -Argument $nagArg -WorkingDirectory $Repo) `
    -Trigger $trigNag -Settings $settingsNoWake -Principal $interactive `
    -Description "Ripple: daily popup listing scheduled tasks that failed or went stale (>2x cadence)." | Out-Null
Write-Output "registered: Ripple-nag (daily 18:00, Interactive so the popup has a desktop)"

Write-Output ""
Write-Output "verify:"
Get-ScheduledTask -TaskName "Ripple-*" | Format-Table TaskName, State -AutoSize
