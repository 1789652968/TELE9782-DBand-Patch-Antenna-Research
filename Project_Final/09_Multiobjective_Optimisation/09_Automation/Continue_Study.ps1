$ErrorActionPreference='Stop'
$auto=$PSScriptRoot
$study=Split-Path -Parent $auto
$lastScreen=Join-Path $study '03_Feed_Optimisation/WideTransformer/round2.json'
while (-not (Test-Path -LiteralPath $lastScreen)) {
    if ((Select-String -LiteralPath (Join-Path $auto 'Screen.err') -Pattern 'Traceback' -Quiet)) { Write-Error 'Screen failed; inspect Screen.err' }
    Start-Sleep -Seconds 12
}
Push-Location $auto
try {
    & 'D:\TELE9782\CST Studio Suite 2024\Opera\code\bin\python.exe' -u Round2_Search.py 1> Search.log 2> Search.err
    if ($LASTEXITCODE -ne 0) { throw 'Round 2 adaptive CST workflow failed; inspect Search.err and Search.log' }
    $rt='C:\Users\Admin\AppData\Local\spyder-6\envs\spyder-runtime'
    $env:PATH="$rt;$rt\Library\bin;$env:PATH"
    & "$rt\python.exe" -u Round2_Report.py 1> Report.log 2> Report.err
    if ($LASTEXITCODE -ne 0) { throw 'Report failed; inspect Report.err' }
} finally { Pop-Location }

