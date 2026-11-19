$ErrorActionPreference='Stop'
$r='D:\TELE9782\Project_Final\08_Efficiency_Optimisation'
$cst='D:\TELE9782\CST Studio Suite 2024\Opera\code\bin\python.exe'
$runtime='C:\Users\Admin\AppData\Local\spyder-6\envs\spyder-runtime'
Set-Location -LiteralPath "$r\08_Automation"
$log="$r\09_Documentation\Resume_Execution.log"
function Invoke-StudyStep($exe,$entry) {
    Add-Content $log ("START "+(Get-Date -Format s)+" "+$entry)
    & $exe -u $entry >> $log 2>&1
    if($LASTEXITCODE -ne 0){throw "$entry failed with $LASTEXITCODE"}
    Add-Content $log ("DONE "+(Get-Date -Format s)+" "+$entry)
}
try{
 Invoke-StudyStep $cst 'Efficiency_Study.py'
 Invoke-StudyStep $cst 'Efficiency_Edge_Fields.py'
 Invoke-StudyStep $cst 'Efficiency_Verify.py'
 $env:PATH="$runtime;$runtime\Library\bin;$env:PATH"
 Invoke-StudyStep "$runtime\python.exe" 'Finish.py'
} catch { Add-Content $log ($_ | Out-String); exit 1 }

