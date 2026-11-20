# 4×4 CST artifacts and source mapping

| Artifact | Owner / location | Contents |
|---|---|---|
| [Final_4x4_Native_CST.zip](https://github.com/1789652968/TELE9782-DBand-Patch-Antenna-Research/releases/download/cst-4x4-comparative-study-v1/Final_4x4_Native_CST.zip) | GitHub Release | Final .cst, its complete same-name CST companion (including Model, Result and supporting native files), and exported data |
| [Native artifact JSON manifest](Final_4x4_Native_CST.manifest.json) | Git | Archive fingerprint, original archive fingerprint and 550 per-member SHA256 entries |
| [Final model and companion model files](Design/CST_Project/Final_4x4/) | Git | Lightweight geometry and Model files. Retrieve the Release ZIP to open historical results |
| [Final native exports](Native_Exports/) | Git | Original complex S-parameters, modal reference, 50 Ω CST Touchstone, power series, 150 GHz spherical patterns, E-field samples, surface current and original geometry screenshot |
| [Trial evidence](Trials/) | Git | Trial raw numerical exports, parameters via Design, solver logs, and rejected 26/39 grid evidence. Exact final-grid duplicate exports are referenced at their final native file paths in the source map |
| [Sources and SHA256](SOURCE_FILE_SHA256.csv) | Git | Path mapping relative to the original 11_Array_4x4 and this study. The original and Git SHA256 values record any path or host redaction |
| [Public exclusions](EXCLUDED_SOURCE_FILES.csv) | Git | Initial native .cst excluded because embedded schematic entries record a private workstation profile |

## Verify and open

The download has **219,838,486 bytes**, **550 members**, SHA256 **c44722650b2c30d7c6b15d615b6ebf311721b9f070c6f9cc55f83b637a8cc94c**. Run PowerShell `Get-FileHash -Algorithm SHA256 Final_4x4_Native_CST.zip`. Extract to a short writable folder and open `01_CST_Project/Final_4x4/Final_4x4.cst` with its same-name folder alongside it in CST Studio Suite 2024. For the 1×2 comparison, see the [prior Release downloads](../Large_Artifacts/ARTIFACT_DOWNLOAD_GUIDE.md).

The public ZIP preserves 548 members byte-for-byte. A machine hostname was replaced with `<workstation>` in the two solver text logs Model.log and MCalc.log. All model contents, native results, numerical exports, timing and mesh evidence are preserved. The source archive and all project directories were left in place. The source ZIP was 219,838,513 bytes, SHA256 `962763da0e6481cee1b06d8ae211581242e8024194913e3459cc8d5c38cbf377`.

The unredacted initial CST and intermediate trial companion databases remain under `11_Array_4x4/01_CST_Project/<case>/`. Historical binary trial results are available from the project owner when needed. The initial design parameters, native CST History, scripted geometry, solved CSVs, field export and log are available here. Temporary wrapper logs, local readback copies, solver caches for intermediate cases, and duplicate ZIP contents were omitted from Git.
