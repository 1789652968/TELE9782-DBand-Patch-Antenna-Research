# 150 GHz 4×4 design methodology

This experiment compares the already verified 82.99% 1×2 design with a conventional sixteen-element array. The comparison retains the physical costs of the longer feed and larger board. A change in efficiency, directivity, or bandwidth is attributable to the two complete implementations, which differ in size, routing, junction count, and electromagnetic coupling.

## Starting point and material model

The source is the archived [Round 1 delivery](../../Project_Final/08_Efficiency_Optimisation/06_Final_Candidate/TELE9782_DBand_Efficiency_Final/) and its saved parameter and power files. The initial 4×4 takes (W=0.667) mm, (L=0.5148) mm, inset depth 0.165 mm and gap 0.020 mm from that design. Both use 75 μm Polyimide with relative permittivity 3.5 and loss tangent 0.0027, and 2 μm Gold at (4.561\times10^7) S/m. Initial uniform line and transformer widths are 0.1688 and 0.1031 mm. Each initial stepped transformer is 0.28 mm long.

Patches have identical orientation and feed from their −Y edges. The X pitch is 1.12 mm, the original 1×2 pitch, and the Y pitch is 1.25 mm to leave clear space between a row feed rail and the neighboring patches. At 150 GHz these pitches are about 0.56 and 0.63 free-space wavelengths. The initial main ground and substrate measure 5.520 × 5.532 mm and support an attached 0.5 mm single-port launch. The original main board measures 2.500 × 1.500 mm. Board-area metrics exclude the separately stated launch tab.

## Single-layer corporate feed

A side inlet allows four equivalent row inputs without trace crossings or feeding patches from opposite radiating edges. The first two corporate splits distribute power to four rows. Each row has a symmetric one-to-four feed which divides into two matched pairs, then into the four uniformly oriented inset feeds. Fifteen T-junctions yield sixteen paths. At each split the initial narrow sections approximate quarter-wave transformers for nominal 50 Ω downstream loads. All sixteen drawn centreline paths have equal nominal length. The side inlet and off-aperture distribution network make the full shape asymmetric across X. Finite-ground scattering, matching, local current and phase still depend on the coupled, distributed geometry.

The generator checks planar conductor connectivity and verifies each patch only contacts its own inset trace. CST Boolean unions create the top conductor and retain the separate backside ground across the dielectric thickness. The 150 GHz surface-current export and sixteen sampled complex electric fields immediately before the inset edges provide solved-topology checks. The Ez values are local net fields. They can indicate excitation and asymmetry, and they include standing-wave and coupling contributions.

## Solver and comparison

CST Studio Suite 2024 solves with the established hexahedral time-domain setup, open boundaries, −60 dB convergence threshold and the 130–170 GHz sweep. The waveguide port points along +X for the side feed. Its physical mode is retained and the exported S11 and realized gain are compared at a common 50 Ω. All efficiencies and power balances use raw CST powers at 150 GHz. The feed geometry is generated from a parameter file so dimensional adjustments are made by rebuilding the same topology. Independent mesh settings and any matching changes are recorded in the comparison report and verification files.
