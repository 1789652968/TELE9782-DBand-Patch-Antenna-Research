# Execution log

1. Original single geometry, fine-mesh numerical baseline and saved verification read. Provenance hashes recorded.
2. Initial connected array solved. Feed development and five nominal spacings tested on a fixed board. Candidate values, warnings and intermediate native file locations are recorded in Optimisation_History.csv.
3. Screening selection was Transformer. More than one grid on the same geometry was solved. Accepted mesh source: Refined. GroundControl is a separate enlarged-board single.
4. Final50 was solved with the explicit 50 Ω history setting. The saved modal trace was independently renormalized by CST Touchstone export. The delivered file was reopened and freshly solved. Complex S11 and all farfield monitor metrics were compared.
5. Native EM field, current, power and angular exports were reduced to tables and plots. Source and file-existence checks completed. The report lists numerical uncertainty and the limits of a simulation-only design.
