"""Generate static 4x4 study figures from the released raw evidence and postprocessing."""
from pathlib import Path
import csv
import json
import math
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

STUDY = Path(__file__).resolve().parents[1]
FIGURES = STUDY / "Figures"
RESULTS = STUDY / "02_Simulation_Results"
COLORS = ["#24568c", "#b65123"]


def table(path):
    with path.open(newline="", encoding="utf-8-sig") as rows:
        return list(csv.DictReader(rows))


def finish(fig, name):
    fig.savefig(FIGURES / name, dpi=175, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def compare():
    rows = table(STUDY / "03_Comparison/Array_1x2_vs_4x4_Comparison.csv")
    fig, panels = plt.subplots(1, 2, figsize=(10.5, 4.2), layout="constrained")
    definitions = [
        ("Efficiency at 150 GHz", "%", ["Radiation", "Total (50 Ω)"],
         ["radiation_efficiency_pct", "total_efficiency_50ohm_pct"], 100),
        ("Directivity and gain at 150 GHz", "dBi", ["Maximum D", "Peak gain", "+Z gain"],
         ["directivity_dBi", "peak_realized_gain_50ohm_dBi", "plus_z_realized_gain_50ohm_dBi"], 14),
    ]
    for ax, (title, unit, names, fields, limit) in zip(panels, definitions):
        for j, row in enumerate(rows):
            xs = [k + (j - .5)*.35 for k in range(len(fields))]
            bars = ax.bar(xs, [float(row[f]) for f in fields], .33, color=COLORS[j],
                          label=["Optimised 1×2", "Basic 4×4"][j])
            ax.bar_label(bars, fmt="%.2f", padding=3, fontsize=9)
        ax.set(title=title, ylabel=unit, xticks=range(len(names)), xticklabels=names, ylim=(0, limit))
        ax.grid(axis="y", alpha=.25)
        ax.set_axisbelow(True)
    panels[0].legend(loc="lower left")
    finish(fig, "Efficiency_Directivity_Gain_Comparison.png")


def geometry():
    layout = json.loads((STUDY / "Design/Geometry_Parameters/Final_4x4/layout.json").read_text())
    fig, ax = plt.subplots(figsize=(7.6, 7), layout="constrained")
    bx, by = layout["board_x"], layout["board_y"]
    ax.add_patch(Rectangle((bx[0], by[0]), bx[1]-bx[0], by[1]-by[0], color="#edf1f5"))
    px, py = layout["port_x"], layout["port_y"]
    ax.add_patch(Rectangle((px, py-.25), bx[0]-px, .50, color="#dfe9f2"))
    for part in layout["parts"]:
        if part["kind"] == "patch":
            continue
        (x, rx), (y, ry) = part["x"], part["y"]
        ax.add_patch(Rectangle((x, y), rx-x, ry-y, color=COLORS[0], linewidth=0))
    for part in layout["parts"]:
        if part["kind"] != "patch":
            continue
        (x, rx), (y, ry) = part["x"], part["y"]
        ax.add_patch(Rectangle((x, y), rx-x, ry-y, color=COLORS[1], linewidth=0))
        cx = (x + rx) / 2
        for gap_x in (cx-.1688/2-.020, cx+.1688/2):
            ax.add_patch(Rectangle((gap_x,y),.020,.165,color="#edf1f5",linewidth=0))
    ax.vlines(px, py-.25, py+.25, linewidth=2, color="#282c34")
    ax.annotate("X-min port", (px, py), xytext=(-4.05,-.10),
                arrowprops={"arrowstyle":"->"}, ha="center", fontsize=9)
    ax.annotate("Stepped feed", (px+.24, py), xytext=(-3.98,-1.55),
                arrowprops={"arrowstyle":"->"}, ha="center", fontsize=9)
    ax.set(xlim=(-4.6,2.55), ylim=(-3.16,2.60), aspect="equal", xlabel="x (mm)", ylabel="y (mm)",
           title="Final 4×4 corporate feed and X-min input")
    finish(fig, "Corporate_Feed_and_Port_Layout.png")


def probes():
    rows = table(RESULTS / "Farfield/Patch_Feed_Probes_150.csv")
    fig, panels = plt.subplots(1, 2, figsize=(9, 4.5), layout="constrained")
    configurations = [("Ez_abs_Vm", "|Ez| (V/m)", "viridis", ".0f"),
                      ("Ez_phase_about_circular_mean_deg", "Ez phase about circular mean (°)", "coolwarm", ".1f")]
    for ax, (field, title, cmap, fmt) in zip(panels, configurations):
        grid = [[float(rows[4*r+c][field]) for c in range(4)] for r in range(4)]
        scale = {} if "abs" in field else {"vmin":-20,"vmax":20}
        im = ax.imshow(grid, origin="lower", cmap=cmap, **scale)
        midpoint = (min(map(min,grid))+max(map(max,grid)))/2
        for r in range(4):
            for c in range(4):
                value=grid[r][c]
                ink = ("black" if value > midpoint else "white") if "abs" in field else ("white" if abs(value)>15 else "black")
                ax.text(c, r, format(value,fmt), ha="center", va="center", color=ink, fontsize=9)
        ax.set(title=title, xticks=range(4), yticks=range(4), xticklabels=range(1,5), yticklabels=range(1,5),
               xlabel="Patch column", ylabel="Patch row")
        fig.colorbar(im, ax=ax, fraction=.045)
    fig.suptitle("Local net E-field sampled upstream of each inset, 150 GHz")
    finish(fig, "Patch_Excitation_150GHz.png")


def mesh():
    rows = table(RESULTS / "Verification/Mesh_Sensitivity.csv")
    fig, panels = plt.subplots(1, 3, figsize=(10.5,3.7), layout="constrained")
    cells = [int(row["mesh_cells"])/1000 for row in rows]
    for ax, (field, label, decimals) in zip(panels, [
        ("radiation_efficiency_pct","Radiation efficiency (%)",3),
        ("directivity_dBi","Peak directivity (dBi)",3),
        ("s11_50ohm_dB","S11 at 50 Ω (dB)",3),
    ]):
        ys = [float(row[field]) for row in rows]
        ax.plot(cells, ys, "o-", color=COLORS[1])
        low, high = min(ys),max(ys)
        pad = (high-low)*.25
        ax.set(ylim=(low-pad, high+pad), xlabel="Mesh cells (thousands)", ylabel=label)
        for x,y in zip(cells,ys):
            ax.annotate(f"{y:.{decimals}f}", (x,y), xytext=(0,8), textcoords="offset points", ha="center", fontsize=9)
        ax.grid(alpha=.25)
    fig.suptitle("Stepped-feed 4×4 mesh sensitivity at 150 GHz")
    finish(fig, "Mesh_Sensitivity_150GHz.png")


if __name__ == "__main__":
    FIGURES.mkdir(exist_ok=True)
    plt.rcParams.update({"font.size":10, "axes.spines.top":False, "axes.spines.right":False})
    compare()
    geometry()
    probes()
    mesh()
