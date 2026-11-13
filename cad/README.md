# cad/ — parametric CAD of cartridge A (docs/13 Rev B) and its dock, C2 prototype stage

Status 2026-11-13: physical design round complete and integrated (docs/18 **Revision B**, docs/19–22 modules,
docs/23 integration). Python ≥ 3.10, CadQuery 2.8 (see `requirements.txt`). Run everything from `cad/`.

## Layout and ownership
| Path | Owner | Content |
|---|---|---|
| `elisa_cad/interface.py` | interface / integration | **single source of truth** for every interface number (mm); Revision B changelog at the top; no side effects on import |
| `elisa_cad/common.py` | interface | STEP/SVG/PNG export, colours per material, output dirs, small solid helpers |
| `elisa_cad/interface_plan.py` | interface | plans + envelope/claim STEP from interface.py only → `out/interface/` |
| `elisa_cad/card/` | CARD (docs/19) | layers L0–L4, die, all card features, DXF/SVG cut files, die mask → `out/card/` |
| `elisa_cad/dock_upper/` | DOCK UPPER (docs/20) | lid/head: pins, springs, yokes, cylinders, heater block, press pad, cam, latches, cover → `out/dock_upper/` |
| `elisa_cad/dock_lower/` | DOCK LOWER (docs/21) | nest, anvil, cold zone, M_c units, M_d stage, electrode bay, tubes, latch brackets, hinge pedestals → `out/dock_lower/` |
| `elisa_cad/dock_base/` | DOCK BASE (docs/22) | frame, deck, pumps, bottles, pneumatics, electronics, enclosure, tubing schedule → `out/dock_base/` |
| `elisa_cad/assembly/` | integration (docs/23) | real card + all modules in dock coordinates, cross-module checks, z-buffer renders → `out/assembly/` |

Each module package has `build.py` (entry point), its own parameters (`params.py` / `geom.py` / `profiles.py`), parts,
calcs and one-off checks; numbers come from `interface.py` (never retyped).

## How to build (run times measured 2026-11-13 on a 4-core container, see docs/23 §12)
```bash
cd cad
pip install shapely ezdxf            # once (requirements.txt)
python -m elisa_cad.interface_plan               # ~10 s    -> out/interface/
python -m elisa_cad.card.build                   # ~25 s    -> out/card/
python -m elisa_cad.dock_upper.build             # ~3.5 min -> out/dock_upper/   (--fast: no STEP/PNG)
python -m elisa_cad.dock_lower.build             # ~5 min   -> out/dock_lower/   (--fast: no M_d sweep)
python -m elisa_cad.dock_base.build              # ~5.5 min -> out/dock_base/    (--fast: no renders)
python -m elisa_cad.assembly.build               # ~22 min -> out/assembly/ (--fast, --no-step, --no-renders)
```
The modules are independent (the assembly imports their code, not their output files); they can be built in any
order or in parallel.

## Output policy (repository size, docs/23 §3.4)
Committed by default: per-part STEP files, ONE assembly state per module, the integrated dock STEPs, PNG/SVG, DXF,
check results. Large redundant state assemblies are regenerated on demand and are **not** written by default:
* `python -m elisa_cad.dock_lower.build --all-states` → `assy_lower_bay_{load,collect_IC1,gather_IC1,drag_mid_IC1,beadout_end}.step` and `sub_*.step` (default: `assy_lower_bay_hold_RC.step` only)
* `python -m elisa_cad.dock_upper.build --all-states` → `lid_assembly_{raised,open}.step`, `subassy_head_closed.step` (default: `lid_assembly_closed.step`)
* `python -m elisa_cad.dock_base.build --all-states` → `base_assembly_with_claims.step` (default: the group STEPs)

## Rules for module authors
* Import numbers from `interface.py`; never retype them. A number another module depends on goes into interface.py
  (next revision); module-local numbers carry a source tag.
* Stay inside your space claim (`interface.SPACE_CLAIMS`, dock coords). Card features are in card coords;
  `interface.card_to_dock()` converts (pure translation, `CARD_ORIGIN_IN_DOCK`).
* Source tag in a comment on every constant: `docs/13 §x` | `Derived` | `CHOICE-n` | `DEV-n` | `I-n` | `UNVERIFIED` | `[assessment]`.
* Units mm, N, deg C. Card z = 0 is the foil underside = anvil top.

## Rendering notes (tested)
* STEP: `common.export_step(obj_or_assembly, path)` (assemblies keep names and colours).
* SVG line views: `common.export_svg(obj, path, view)` (CadQuery HLR exporter).
* PNG, module renders: `common.render_png(...)` — matplotlib painter's algorithm (triangle depth sort); can show
  artefacts where large faces overlap small bodies.
* PNG, integrated renders: `assembly/zrender.py` — software **z-buffer** rasteriser (numpy) with part outlines from
  id/depth discontinuities and tinted section faces; exact occlusion per pixel. VTK offscreen does not work in this
  container (no X/EGL/OSMesa).
