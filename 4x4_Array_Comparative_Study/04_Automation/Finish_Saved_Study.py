"""Complete the study after the saved finest-grid project has been read back."""
from pathlib import Path
import subprocess,sys,time
root=Path(__file__).resolve().parents[1]
auto=root/'04_Automation'
f=root/'01_CST_Project/Licensed_23_33_4x4'
case=f/'Export_Complete.json'
for _ in range(36):
    if case.exists():break
    err=auto/'Export_Recovery.err'
    if err.is_file() and 'Traceback' in err.read_text(encoding='utf-8',errors='replace'):
        raise RuntimeError('Saved-result recovery stopped; inspect Export_Recovery.err')
    time.sleep(5)
else:raise RuntimeError('Waited 3 minutes for saved-result recovery')
with (auto/'Study_Complete.log').open('ab') as log:
    subprocess.run([sys.executable,'-u',str(auto/'Study_Sequence.py')],cwd=auto,stdout=log,check=True)
subprocess.run([sys.executable,'-u',str(auto/'Finalize_4x4.py')],cwd=auto,check=True)

