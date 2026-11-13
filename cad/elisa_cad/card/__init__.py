"""Cartridge A card (docs/13 Rev B, C2 laminated prototype): parametric parts L0-L4, die, assembly, checks.

Design document: docs/19_cartridge_A_physical_design.md. Interface numbers come from elisa_cad.interface only.
Run from cad/:  python -m elisa_cad.card.build   -> cad/out/card/
Modules:
  profiles.py  2D (shapely) profiles of every layer, die masks and fluid regions (single geometric source here)
  parts.py     3D solids (CadQuery) built from the profiles + L3 machining
  checks.py    one-off checks (volumes, webs, tips, registration, mass) -> out/card/checks.json
  render.py    PNG views, sections, plans
  build.py     main(): STEP, DXF/SVG, PNG, checks
"""
