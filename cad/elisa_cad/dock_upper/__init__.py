"""DOCK UPPER (lid / head) of the cartridge-A bench dock, C2 prototype stage (docs/20).

Modules:
  params.py  -- every DOCK UPPER number with a source tag (imports interface.py, never retypes it)
  calcs.py   -- force, pneumatic, thermal and kinematic calculations (pure; printed by build.py)
  parts.py   -- CadQuery solids of custom parts and labelled envelopes of catalogue parts
  assy.py    -- head and lid assemblies in the three configurations (closed, head raised, open 85 deg)
  checks.py  -- one-off checks (interference, clearances, sweep, loading path)
  build.py   -- regenerates STEP + PNG into cad/out/dock_upper/ :  cd cad && python -m elisa_cad.dock_upper.build
"""
