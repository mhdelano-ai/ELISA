# Tier-2 flow cell — notes for the machining drawings (generated; text of docs/34 section 5.2)

STEP files carry the nominal geometry. Threads are modelled as tap-drill holes. Everything not listed: ISO 2768-m, edges broken 0.1–0.2 mm, no burrs in the liquid path.

| Part | File | Material | Features that need a call-out |
|---|---|---|---|
| Base | `base.step` | 316L stainless | 4 × M4×0.7-6H through. 2 × ⌀3.0 P7 × 6 deep (press fit for ⌀3 m6 × 16 pins). Strip pocket 10.3 +0.05/0 wide, depth 0.45 ±0.02, floor flat within 0.02 and Ra ≤ 0.8 µm. Top face flat within 0.02. |
| Nozzle plate | `nozzle_plate.step` | PEEK, natural, unfilled | Underside (cell face): flat within 0.02, Ra ≤ 0.4 µm inside ⌀9.3; no tool marks across the O-ring groove floor. O-ring groove ⌀6.9/⌀9.3, depth 0.65 ±0.03. Exit bore ⌀0.5 +0.03/0, both ends sharp and free of burr, within 0.05 of the dowel datum. 2 × ⌀3.0 H7. 4 × ⌀2.7 with 90° countersink ⌀5.0 from the underside (heads below the face). Top face flat within 0.02, Ra ≤ 0.8 µm. |
| Body | `body.step` | PEEK, natural, unfilled | 2 × 1/4-28 UNF-2B, flat-bottom ports to the fitting maker's port drawing (depth 9.5 here; bottom flat, Ra ≤ 0.8 µm, square to the thread). Bed bore ⌀0.5 +0.03/0 through the port floor, concentric with the retainer seat within 0.05, no burr. Retainer seat ⌀1.65 +0.03/0, depth 0.06 +0/−0.01. Underside flat within 0.02, Ra ≤ 0.8 µm. O-ring groove ⌀11.9/⌀14.3, depth 0.75 ±0.03. 4 × M2.5×0.45-6H, 7 deep. 2 × ⌀3.0 H7. |

| Part | Envelope (mm) | Mass (g) |
|---|---|---|
| base | 30 × 44 × 8.0 | 81 |
| nozzle_plate | 30 × 44 × 2.5 | 4 |
| body | 30 × 44 × 12.0 | 19 |
