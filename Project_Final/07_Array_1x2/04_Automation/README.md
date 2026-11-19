# Automation and reproduction

Commands below use the current directory 04_Automation. Execute the CST steps serially on a licensed workstation. A scratch copy of the array folder preserves the delivered files. To rebuild the study from scratch, use a fresh study directory with the same 01–06 directory names and these automation files, adjacent to the original validated results. Completed screening cases are reused if their angular exports are present.

In PowerShell define the two interpreters.

~~~powershell
$cst = 'D:\TELE9782\CST Studio Suite 2024\Opera\code\bin\python.exe'
$analysisDir = 'C:\Users\Admin\AppData\Local\spyder-6\envs\spyder-runtime'
$analysis = Join-Path $analysisDir 'python.exe'
$env:PATH = "$analysisDir;$analysisDir\Library\bin;$env:PATH"
~~~

Rebuild and extract the electromagnetic results.

~~~powershell
& $cst Array_Optimisation.py
& $cst Array_Sweep_Fields.py
~~~

For the complete second-stage resonance comparison, run & $analysis Array_Final_Selection.py after the first two commands. It runs the retuned 1.20 mm coarse case, checks whether a fine candidate is warranted, tests mesh stability, performs native fixed-reference production, and calls the rerun and mode scripts. If it has completed, proceed directly to the numerical postprocessing steps below. The independent holdout is obtained with & $cst Array_Refine.py Refined MeshHoldout mesh_near=38 mesh_box=57 after native verification. Array_Holdout.py also performs this check and then regenerates all outputs. The first script performs the feed sweep, controlled spacing comparison, Fine run and ground control. Where a third grid was required use the geometry and mesh settings recorded in Mesh_Convergence.csv with Array_Refine.py. To repeat an individual geometry, supply source name, new case name and key=value parameters.

~~~powershell
& $cst Array_Fixed_Reference.py Refined
& $cst Array_Rerun.py Final50
& $cst Array_Line_Mode.py
& $cst Array_Touchstone.py
& $analysis Array_Results_Extraction.py
& $analysis Array_Comparison.py
& $analysis Array_Coupling.py
& $analysis Array_Current_Maps.py
& $analysis Array_Common_Reference.py
& $analysis Array_Report.py
& $analysis Array_Config_Check.py
& $analysis Array_Power_Closure.py
& $analysis Array_Delivery.py
~~~

The hosted scripts use the CST 2024 Python interface installed with the software. Numerical post-processing uses NumPy 2 and Matplotlib. Array_Build.py and Single_Control.py share Reference_ModelHistory.json. Array_Fields.py exports native complex fields at explicit point coordinates. The postprocessor reads exported values and native CST farfields, with no ideal array synthesis. To inspect the original modal setup use the Refined working project. Open the final project for the production model. Use the CST Touchstone export for the exact 50 Ω curve.