# cad/ — parametric CAD of cartridge A (docs/13 Rev B) and its dock, C2 prototype stage

Status 2026-11-13: interface phase done (docs/18). Card and dock modules are written by the downstream agents.

## Layout and ownership
| Path | Owner | Content |
|---|---|---|
| `elisa_cad/interface.py` | interface architect | **single source of truth** for every interface number (mm); no side effects on import |
| `elisa_cad/common.py` | interface architect | STEP/SVG/PNG export, colours per material, output dirs, small solid helpers |
| `elisa_cad/interface_plan.py` | interface architect | plans + envelope/claim STEP from interface.py only → `out/interface/` |
| `elisa_cad/card*.py` | CARD agent | layers L0–L4, die, all card features → `out/card/` |
| `elisa_cad/dock_upper*.py` | DOCK UPPER agent | lid/head: pins, springs, yokes, cylinders, heater block, press pad, latch, cover → `out/dock_upper/` |
| `elisa_cad/dock_lower*.py` | DOCK LOWER agent | nest, anvil, cold plate, magnet bay, M_d stage, M_c units, electrode bay → `out/dock_lower/` |
| `elisa_cad/dock_base*.py` | DOCK BASE agent | frame, pumps, bottles, electronics, drip tray, enclosure, routes → `out/dock_base/` |

## Rules for module authors
* Import numbers from `interface.py`; never retype them. If you need a number that is not there, define it in your
  own module with a source tag; if another agent depends on it, report it for the next interface revision.
* Stay inside your space claim (`interface.SPACE_CLAIMS`, dock coords). Card features are in card coords;
  `interface.card_to_dock()` converts (pure translation, `CARD_ORIGIN_IN_DOCK`).
* Source tag in a comment on every constant: `docs/13 §x` | `Derived` | `CHOICE-n` | `DEV-n` | `UNVERIFIED` | `[assessment]`.
* Units mm, N, deg C. Card z = 0 is the foil underside = anvil top.

## How to run
```bash
cd cad
pip install shapely            # once (see requirements.txt)
python -m elisa_cad.interface_plan     # -> out/interface/*.png|svg|step  (~1 min)
```
Each module provides `main()` and writes STEP + PNG/SVG to `out/<module>/` via `common.out_dir()`.

## Rendering notes (tested)
* STEP: `common.export_step(obj_or_assembly, path)` (assemblies keep names and colours).
* SVG line views: `common.export_svg(obj, path, view)` (CadQuery HLR exporter).
* PNG: `common.render_png([(obj, material), ...], path, view)` — matplotlib flat-shaded painter's algorithm from the
  tessellation. VTK offscreen does **not** work in this container (no X/EGL/OSMesa). Painter sorting can show
  artefacts where large faces overlap small bodies; render sub-assemblies or use section/plan views for detail.
