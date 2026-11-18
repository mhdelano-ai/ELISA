# Tier-2 flow cell — ordering the three machined parts (e.g. from Xometry)

Generated drawings, revision A, 2026-11-18. Design and reasons: `docs/34_tier2_flow_cell.md` (sections 5.1–5.2).
**Check the drawings before ordering**: they were generated from the CAD model and checked by eye only; the title
blocks have no checker's or approver's name.

| Part | Upload (3D) | Upload (drawing) | Material to select | Quantity suggested |
|---|---|---|---|---|
| T2C-001 Base | `T2C-001_base_revA.step` | `T2C-001_base.pdf` | Stainless steel 316L | 1 |
| T2C-002 Nozzle plate | `T2C-002_nozzle_plate_revA.step` | `T2C-002_nozzle_plate.pdf` | Acetal copolymer (POM-C), natural; not Delrin (homopolymer) | 3 (one per bed unit, docs/34 §7) |
| T2C-003 Body | `T2C-003_body_revA.step` | `T2C-003_body.pdf` | Acetal copolymer (POM-C), natural | 3 |
| T2C-004 Washer (cut gasket) | `T2C-004_washer_revA.step` + `T2C-004_washer.dxf` / `T2C-004_washer_sheet.dxf` | `T2C-004_washer.pdf` | FKM sheet 0.25 mm, 70–75 Shore A | 100 (one per bed) |

Plate and body were PEEK until 2026-11-18; acetal copolymer is cheaper and machines as well. PEEK, unfilled,
natural stays the fallback (docs/34 §5.4): quoting both is a quick way to see the price difference.

For each part in the quote:
* **Tolerance**: standard, *with drawing*. The drawings carry only the features with tighter-than-standard
  tolerances (all flagged, none tighter than ±0.025 mm / ±0.001 in, finer finishes and edge breaks included) and
  the threads. Everything else comes from the STEP file at Xometry's standard tolerance (title block of each
  drawing); how to make the parts is left to the supplier. Say in the notes field: "Undimensioned geometry per
  STEP at standard tolerance; flagged features per attached drawing, to be inspected."
* **Threads**: yes. Base 4 × M4×0.7-6H through; body 4 × M2.5×0.45-6H blind (6.0 full thread) and 2 × 1/4-28
  UNF-2B flat-bottom ports (note 3 of T2C-003). Threads are modelled as tap-drill holes in the STEP files.
* **Finish**: Ra 1.6 µm (63 µin) all over for base, plate and body (title blocks); on the body Ra 0.8 (32 µin)
  at the port bottoms (note 3) and Ra 0.4 (16 µin) inside ⌀3 around the bed bore. Whether Xometry's quote form
  offers Ra 1.6 as a selection was not checked: if not, state it in the notes field. No bead blast, no anodising, no marking on the parts.
* **Inspection**: standard, plus the flagged features. A dimensional report for the flagged features is worth
  requesting for the first lot.
* **Ports**: the values of the 1/4-28 flat-bottom port drawing (depth 0.350 in, full thread 0.28 in minimum,
  bottom flat within 0.002 in at 32 µin, corner radius ≤ 0.007 in, chamfer ⌀0.27 in × 90°) are written out in
  note 3 of T2C-003, so no separate port drawing is needed. Beyond the user's port drawing, T2C-003 adds only the
  inlet port's position (the flow path is a 0.5 mm bore in the port floor).

The washer (⌀1.40 ±0.10 / ⌀0.75 ±0.10 × 0.25 ±0.05, hole concentric within ⌀0.10) is a cut-rubber part: a CNC shop
may not take it. A gasket cutter works from the
DXF; whether Xometry offers rubber-sheet cutting was not checked.

Not machined (buy separately; docs/34 §5.4): MicruX ceramic strips, O-rings 7 × 1 and 12 × 1, ⌀3 m6 × 16 dowel
pins and retaining compound, M4 × 20 socket head and M2.5 × 6 low-head socket (DIN 7984, from below into counterbores) screws, shim stock, VICI 2SR1-10 screens, 1 µm track-etched
membrane.

At assembly: measure the base pocket depth and cut the shim stack to depth − 0.38 − 0.10 mm; measure the plate's
retainer pocket depth and pick washers by thickness (docs/34 §3.1, §4.3, §7).
