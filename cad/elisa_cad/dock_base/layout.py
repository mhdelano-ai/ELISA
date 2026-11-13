"""Placed bodies of the DOCK BASE: custom parts (real geometry) and catalogue envelopes (outer dimensions, ports
and connector faces marked). Every item carries mass, source tag and group. Geometry built in parts.py."""
from __future__ import annotations

from dataclasses import dataclass, field

from . import params as P

AL, SS, PU = 2.70e-6, 8.0e-6, 0.035e-6     # kg/mm^3 (Al, stainless, PU foam) [assessment, handbook class values]


@dataclass
class Item:
    name: str
    group: str            # frame | enclosure | tray | bracket | cold | pumps | bottles | pneumatics | electronics
    #                       | gamry | sensors | bench
    kind: str             # custom | catalogue | envelope
    box: tuple            # ((x0,y0,z0),(x1,y1,z1)) outer envelope
    material: str = "envelope"
    mass: float = 0.0     # kg
    src: str = ""
    spec: str = ""
    shape: str = "box"    # box | cyl_z | cyl_y | custom
    ports: list = field(default_factory=list)   # [(name, (x,y,z))] marked as small markers
    cut_claims_ok: tuple = ()                    # claims this item may legitimately touch (zero-volume contact)


def bx(x0, y0, z0, x1, y1, z1):
    return ((x0, y0, z0), (x1, y1, z1))


def vol(b):
    (x0, y0, z0), (x1, y1, z1) = b
    return (x1 - x0) * (y1 - y0) * (z1 - z0)


ITEMS: list[Item] = []


def add(*a, **k):
    it = Item(*a, **k)
    ITEMS.append(it)
    return it


# ============================================================================================ frame / structure
FX, FY, FZ = P.FX, P.FY, P.FZ
e, s, pi_ = P.EXTR, P.SHEET_T, P.POST_INSET
add("base_plate", "frame", "custom", bx(0, 0, P.BASE_PLATE_Z[0], FX, FY, P.BASE_PLATE_Z[1]), "aluminium",
    FX * FY * 10 * AL, "CHOICE-B1", "Al 6082-T6 10 mm tooling plate, CNC: 4 x M10 foot bores, sump pocket, "
    "tapped holes for posts, deck spacers, isolators, PE stud", shape="custom")
for i, (fx, fy) in enumerate(P.FEET_XY):
    add(f"foot_{i+1}", "frame", "catalogue", bx(fx - 20, fy - 20, 0, fx + 20, fy + 20, P.FOOT_PAD[1]), "elastomer",
        0.08, "UNVERIFIED", "levelling swivel pad D40 x 5, M10 screw adjustable from above +-3 mm", shape="cyl_z")
POSTS = [(pi_, pi_), (FX - pi_ - e, pi_), (pi_, FY - pi_ - e), (FX - pi_ - e, FY - pi_ - e)]
z_post = (P.BASE_PLATE_Z[1] + 1.0, P.TOP_RAIL_Z[0])      # stands on the tray floor (clamped through it)
for i, (x, y) in enumerate(POSTS):
    add(f"post_{i+1}", "frame", "catalogue", bx(x, y, z_post[0], x + e, y + e, z_post[1]), "aluminium",
        0.5e-3 * (z_post[1] - z_post[0]), "[assessment] 20x20 slot-6 profile, 0.5 kg/m class UNVERIFIED")
zr0, zr1 = P.TOP_RAIL_Z
rails = {
    "rail_left": bx(pi_, pi_ + e, zr0, pi_ + e, FY - pi_ - e, zr1),
    "rail_right": bx(FX - pi_ - e, pi_ + e, zr0, FX - pi_, FY - pi_ - e, zr1),
    "rail_rear": bx(pi_ + e, FY - pi_ - e, zr0, FX - pi_ - e, FY - pi_, zr1),
    "rail_front_left": bx(pi_ + e, pi_, zr0, P.PART_X["left"][0], pi_ + e, zr1),
    "rail_front_right": bx(P.PART_X["right"][1], pi_, zr0, FX - pi_ - e, pi_ + e, zr1),
    "rail_well_rear": bx(P.PART_X["left"][1], 318.0, zr0, P.PART_X["right"][0], 318.0 + e, zr1),
}
for k, b in rails.items():
    L = max(b[1][i] - b[0][i] for i in range(3))
    add(k, "frame", "catalogue", b, "aluminium", 0.5e-3 * L, "[assessment] 20x20 profile")

# bay deck (carries LOWER_bay; IR-1 bolt pattern)
D = P.DECK
add("bay_deck", "frame", "custom", bx(D["x"][0], D["y"][0], D["z"][0], D["x"][1], D["y"][1], D["z"][1]), "aluminium",
    (D["x"][1] - D["x"][0]) * (D["y"][1] - D["y"][0]) * 10 * AL, "CHOICE-B1; IR-1",
    "Al 6082 10 mm, fly-cut top = LOWER_bay bottom face Z 40; 9 x M6 grid 70 x 75, dowel D6 + slot", shape="custom")
for i, (x, y) in enumerate(P.DECK_SPACERS_XY):
    add(f"deck_spacer_{i+1}", "frame", "custom", bx(x - 15, y - 15, P.TRAY["z0"] + 1, x + 15, y + 15, D["z"][0]),
        "aluminium", 30 * 30 * 14 * AL, "[assessment]", "Al block 30 x 30, M8 through base plate and tray (sealed washer)")

# partitions (well walls) and rear-low cover (keeps Z <= 180 in Y 205-315, docs/18 §12)
pl, pr = P.PART_X["left"], P.PART_X["right"]
add("partition_left", "enclosure", "custom", bx(pl[0], s, P.TRAY["z0"] + 1, pl[1], 314.0, FZ - s), "aluminium",
    2 * 302 * 312 * AL, "[assessment]", "2 mm Al sheet; glands G_W (tubes), G_C (cables), PEEK line hole", shape="custom")
add("partition_right", "enclosure", "custom", bx(pr[0], s, P.TRAY["z0"] + 1, pr[1], 314.0, FZ - s), "aluminium",
    2 * 302 * 312 * AL, "[assessment]", "2 mm Al sheet; gland G_E, Gamry lead duct hole", shape="custom")
add("rear_low_cover", "enclosure", "custom", bx(pl[1], 202.0, 178.0, pr[0], 312.0, 180.0), "aluminium",
    172 * 114 * 2 * AL, "docs/18 §12 (Z <= 180)", "2 mm Al, umbilical grommet at (235, 207), drains to the tray")
add("well_rear_wall", "enclosure", "custom", bx(pl[1], 312.0, 180.0, pr[0], 314.0, FZ - s), "aluminium",
    172 * 148 * 2 * AL, "[assessment]", "2 mm Al sheet between the open lid well and the pump bay")

# ============================================================================================ enclosure panels
add("panel_left", "enclosure", "custom", bx(0, s, P.BASE_PLATE_Z[1], s, FY - s, FZ - s), "aluminium", FY * 315 * s * AL,
    "CHOICE-B8", "2 mm Al, removable (service to electronics); louvres for cooler exhaust and electronics intake;"
    " SM-FL PEEK line grommet at (0, 110, 160)", shape="custom")
add("panel_right", "enclosure", "custom", bx(FX - s, s, P.BASE_PLATE_Z[1], FX, FY - s, FZ - s), "aluminium", FY * 315 * s * AL,
    "CHOICE-B8", "2 mm Al; Gamry cable gland at (470, 108, 135); air inlet low rear", shape="custom")
add("panel_front_left", "enclosure", "custom", bx(0, 0, P.BASE_PLATE_Z[1], pl[1], s, FZ), "aluminium",
    149 * 315 * s * AL, "CHOICE-B8", "opening for the cold-box door; E-stop and status light above it", shape="custom")
add("panel_front_bay", "enclosure", "custom", bx(pl[1], 0, P.BASE_PLATE_Z[1], pr[0], s, 165.0), "aluminium",
    172 * 150 * s * AL, "CHOICE-B8", "stops 5 mm below the anvil top (Z 170) so the card is reached from the top/front")
add("panel_front_right", "enclosure", "custom", bx(pr[0], 0, P.BASE_PLATE_Z[1], FX, s, FZ), "aluminium",
    149 * 315 * s * AL, "CHOICE-B8", "bottle door (hinged right side) Z 20-255", shape="custom")
add("panel_rear", "enclosure", "custom", bx(0, FY - s, P.BASE_PLATE_Z[1], FX, FY, FZ), "aluminium",
    FX * 315 * s * AL, "CHOICE-B8", "pump service door X 150-465 (hinged, captive screws); connector panel left; "
    "electronics exhaust louvre", shape="custom")
add("panel_top_left", "enclosure", "custom", bx(s, s, FZ - s, pl[1], FY - s, FZ), "aluminium", 149 * FY * s * AL,
    "CHOICE-B8", "fixed")
add("panel_top_right", "enclosure", "custom", bx(pr[0], s, FZ - s, FX - s, FY - s, FZ), "aluminium", 149 * FY * s * AL,
    "CHOICE-B8", "hatch over Y 200-318 for the waste bottle (lift-out)", shape="custom")
add("panel_top_rear", "enclosure", "custom", bx(pl[1], 318.0, FZ - s, pr[0], FY - s, FZ), "aluminium",
    172 * 102 * s * AL, "CHOICE-B8", "over the pump bay")

# drip tray
add("drip_tray", "tray", "custom", bx(P.TRAY["inset"], P.TRAY["inset"], P.TRAY["z0"], FX - P.TRAY["inset"],
    FY - P.TRAY["inset"], P.TRAY["z0"] + P.TRAY["rim_h"]), "steel", 0.21e6 * 1.0 * SS, "docs/13 §6.8; CHOICE-B9",
    "316 stainless 1.0 mm folded, rim 13, corner notches for posts, sump 40x40x8 with level switch; interdigitated "
    "leak electrodes at 4 places", shape="custom")
(sx0, sy0), (sx1, sy1), sd = P.TRAY["sump"]
add("leak_level_switch", "sensors", "envelope", bx(sx0 + 10, sy0 + 10, P.TRAY["z0"] - sd + 1, sx1 - 10, sy1 - 10,
    P.TRAY["z0"] + 10), "envelope", 0.02, "UNVERIFIED", "conductive or optical level switch in the sump")
for i, (x, y) in enumerate([(60, 175), (235, 60), (300, 360), (400, 110)]):
    add(f"leak_electrode_{i+1}", "sensors", "envelope", bx(x - 30, y - 8, P.TRAY["z0"] + 1, x + 30, y + 8,
        P.TRAY["z0"] + 2.6), "pcb", 0.01, "UNVERIFIED", "interdigitated electrode PCB strip 60 x 16 (docs/13 §6.8)")

# ============================================================================================ cold compartment
(cx0, cy0, cz0), (cx1, cy1, cz1) = P.COLD_BOX["outer"]
w = P.COLD_BOX["wall"]
add("cold_box", "cold", "custom", P.COLD_BOX["outer"], "PTFE", 0.6, "CHOICE-B5",
    "PU foam 20 mm between a 1.5 mm Al liner and a 1 mm Al skin; front wall = hinged insulated door (magnetic "
    "gasket), drain hole at the liner low corner -> tray, dry-air purge inlet", shape="custom")
COLD_INNER = ((cx0 + w, cy0 + 18.0, cz0 + w), (cx1 - w, cy1 - w, cz1 - w))
C = P.COOLER
cw_x = ((cx0 + cx1) / 2 - C["Ww"] / 2, (cx0 + cx1) / 2 + C["Ww"] / 2)
add("cooler_DA024_warm", "cold", "catalogue", bx(cw_x[0], cy1, 40.0, cw_x[1], cy1 + C["Hw"], 40.0 + C["Lw"]),
    "aluminium", C["mass"], "V:LAIRD_TCA_CAT", "Laird/Tark DA-024-24-02-00-00 warm side (sink + fan) 80 x 56 x 60; "
    "exhaust -X to the left-panel louvre", ports=[("24V", (cw_x[0], cy1 + 30, 80.0))])
ccx = ((cx0 + cx1) / 2 - C["Wc"] / 2, (cx0 + cx1) / 2 + C["Wc"] / 2)
add("cooler_DA024_cold", "cold", "catalogue", bx(ccx[0], COLD_INNER[1][1] - C["Hc"], 50.0, ccx[1],
    COLD_INNER[1][1], 50.0 + C["Lc"]), "cold", 0.0, "V:LAIRD_TCA_CAT", "cold plate 40 x 60 x 14 on the liner rear wall")
add("cooler_spacer", "cold", "custom", bx(ccx[0], COLD_INNER[1][1], 50.0, ccx[1], cy1, 50.0 + C["Lc"]), "aluminium",
    60 * 40 * 20 * AL, "[assessment]", "Al spacer through the 20 mm rear insulation (cold plate -> TEC)")
# rocker cradle (custom) + bead vial, conjugate holder + tube
iz0 = COLD_INNER[0][2]
add("bead_rocker_cradle", "cold", "custom", bx(50.0, 32.0, iz0 + 15, 90.0, 62.0, iz0 + 30), "aluminium",
    0.05, "CHOICE-B6", "Al cradle on a horizontal shaft (axis X, Y 47, Z 72) rocking +-20 deg at 0.2-0.5 Hz; "
    "paused in read windows (docs/13 §7.2)")
add("bead_vial_2mL", "cold", "catalogue", bx(64.5, 41.5, iz0 + 30, 75.5, 52.5, iz0 + 30 + P.TUBE_2["h"]), "liquid",
    0.005, "UNVERIFIED (2 mL screw-cap microtube class)", "bead stock, fill 0.3-0.5 mL per card (§6)", shape="cyl_z",
    ports=[("vial_line", (70.0, 47.0, iz0 + 30 + P.TUBE_2["h"]))])
add("rocker_motor", "cold", "envelope", bx(123.0, 35.0, 60.0, 145.0, 59.0, 84.0), "envelope", 0.03,
    "UNVERIFIED", "micro gear motor 22 x 24 x 24 + crank, outside the insulation, shaft through the +X wall")
add("conj_holder_block", "cold", "custom", bx(50.0, 85.0, iz0, 80.0, 115.0, iz0 + 25), "aluminium",
    30 * 30 * 25 * AL, "[assessment]", "Al block bolted to the liner floor, bore for a 2 mL tube (conduction cooling)")
add("conj_tube_2mL", "cold", "catalogue", bx(59.5, 94.5, iz0 + 5, 70.5, 105.5, iz0 + 5 + P.TUBE_2["h"]), "liquid",
    0.005, "UNVERIFIED (2 mL screw-cap tube + 2-port pressure cap)", "conjugate, fill 0.5 mL per card (§6)",
    shape="cyl_z", ports=[("P_cf_out", (65.0, 100.0, iz0 + 50)), ("gas_in", (62.0, 97.0, iz0 + 50))])
add("SV_b_selection_valve", "cold", "envelope", bx(100.0, 55.0, cz1 + 2, 140.0, 95.0, cz1 + 47), "envelope", 0.4,
    "UNVERIFIED (6-port low-volume selection valve, e.g. a Cavro Smart Valve class part; dimensions not found)",
    "ports: vial, P_b, waste, air (0.2 um filter), A1, coil from S_b; port face +X",
    ports=[("P_b", (140.0, 77.0, cz1 + 25)), ("coil", (140.0, 62.0, cz1 + 25)), ("vial", (120.0, 70.0, cz1 + 2))])
add("P_in_pressure_sensor", "sensors", "envelope", bx(4.0, 100.0, cz1 + 0.5, 34.0, 120.0, cz1 + 20.5), "envelope", 0.05,
    "UNVERIFIED", "flow-through (no dead leg) pressure sensor, 1/16 in fittings, <= 1 uL swept, 0-10 bar, "
    "non-metallic wetted path; at the upstream end so >= 0.3 m PEEK remains to P_in (docs/13 §6.8)",
    ports=[("in", (4.0, 110.0, 160.0)), ("out", (34.0, 110.0, 160.0))])

# ============================================================================================ pumps
Cn = P.CENTRIS
PUMP_X = {n: P.PUMP_X0 + i * P.PUMP_PITCH for i, n in enumerate(P.PUMP_ORDER)}
py0, py1 = P.PUMP_BODY_Y
pz0 = P.PUMP_SHELF_Z[1]
add("pump_shelf", "bracket", "custom", bx(152.0, 321.0, P.PUMP_SHELF_Z[0], 446.0, 396.0, P.PUMP_SHELF_Z[1]),
    "aluminium", 294 * 75 * 6 * AL, "[assessment]", "Al 6 mm on 4 elastomer isolators (UNVERIFIED, D20 x 15)")
add("pump_back_plate", "bracket", "custom", bx(152.0, 319.0, P.PUMP_SHELF_Z[1], 446.0, 323.0, 225.0), "aluminium",
    294 * 4 * 188 * AL, "[assessment]", "Al 4 mm spine, pump rear faces bolted (Centris mounting holes UNVERIFIED)")
for i, (x, y) in enumerate([(165, 335), (433, 335), (165, 385), (433, 385)]):
    add(f"pump_isolator_{i+1}", "bracket", "catalogue", bx(x - 10, y - 10, P.TRAY["z0"] + 1, x + 10, y + 10,
        P.PUMP_SHELF_Z[0]), "elastomer", 0.02, "UNVERIFIED", "rubber-metal isolator D20 x 15", shape="cyl_z")
for n in P.PUMP_ORDER:
    x = PUMP_X[n]
    add(f"{n}_body", "pumps", "catalogue", bx(x - Cn["W"] / 2, py0, pz0, x + Cn["W"] / 2, py1, pz0 + Cn["H"]),
        "envelope", Cn["mass"], "V:TECAN_CENTRIS_P", f"Tecan Cavro Centris, {P.PUMP_SYRINGE_uL[n]} uL syringe; "
        f"valve {P.PUMP_VALVE[n]}", ports=[("RS485/24V", (x, py0, pz0 + 30))])
    add(f"{n}_valve_syringe", "pumps", "envelope", bx(x - Cn["W"] / 2 + 4, py1, pz0, x + Cn["W"] / 2 - 4,
        py1 + P.PUMP_FRONT_ZONE, pz0 + Cn["H"]), "PTFE", 0.0, "UNVERIFIED (front zone depth)",
        "valve head (top) + syringe (below), front face toward the rear service door",
        ports=[("valve", (x, py1 + P.PUMP_FRONT_ZONE, pz0 + Cn["H"] - 12))])

# ============================================================================================ bottles + pneumatics
D5, D10 = P.DURAN_500, P.DURAN_1000
add("A1_bottle_500mL", "bottles", "catalogue", bx(337.0, 10.0, 17.0, 337.0 + D5["d"], 10.0 + D5["d"], 17.0 + D5["h"]),
    "PTFE", 0.40 + 0.50, "UNVERIFIED dims (DURAN GL45 500 mL listings)", "A1 wash buffer, 2-port GL45 cap (out, "
    "vent filter)", shape="cyl_z", ports=[("A1_out", (380.0, 53.0, 17.0 + D5["h"] + D5["cap_h"]))])
add("A1_cap", "bottles", "envelope", bx(357.5, 30.5, 17.0 + D5["h"], 402.5, 75.5, 17.0 + D5["h"] + D5["cap_h"]),
    "elastomer", 0.03, "UNVERIFIED", "GL45 2-port cap", shape="cyl_z")
add("HQDP_holder", "bottles", "custom", bx(428.0, 28.0, 17.0, 458.0, 58.0, 147.0), "anodised", 0.08, "CHOICE-B3",
    "opaque Al sleeve D30 (dark) for a 15 mL conical tube, 2-port pressure cap on top", shape="cyl_z",
    ports=[("P_rf_out", (443.0, 43.0, 152.0)), ("gas_in", (440.0, 40.0, 152.0))])
add("waste_bottle_1L", "bottles", "catalogue", bx(335.0, 208.0, 17.0, 335.0 + D10["d"], 208.0 + D10["d"],
    17.0 + D10["h"]), "PTFE", 0.60 + 1.0, "UNVERIFIED dims (DURAN GL45 1000 mL listings)",
    "waste >= 1 L (docs/13 §3.7), capacitive level sensor on a bracket at 800 mL", shape="cyl_z")
add("waste_airgap_head", "bottles", "custom", bx(360.0, 233.0, 17.0 + D10["h"], 411.0, 284.0, 259.0), "PEEK",
    0.05, "CHOICE-B4", "GL45 cap with 9 drip nipples ending 10 mm above a funnel (air gap), vent with charcoal filter",
    shape="cyl_z", ports=[("in", (385.5, 258.5, 259.0))])
add("waste_level_sensor", "sensors", "envelope", bx(437.0, 245.0, 160.0, 447.0, 270.0, 190.0), "envelope", 0.02,
    "UNVERIFIED", "capacitive proximity sensor through the glass at 80 % fill")
add("bottle_rack", "bracket", "custom", bx(330.0, 6.0, 16.0, 446.0, 97.0, 17.0), "aluminium", 0.15, "[assessment]",
    "location plate with rings for the A1 bottle and HQDP sleeve")
add("FR1_filter_regulator", "pneumatics", "envelope", bx(340.0, 150.0, 17.0, 380.0, 190.0, 157.0), "envelope", 0.25,
    "UNVERIFIED (SMC AW20-class filter-regulator, dims not read)", "lab air 400-700 kPa -> 300 kPa (lid pilots), 5 um")
add("R2_precision_reg", "pneumatics", "envelope", bx(385.0, 150.0, 17.0, 425.0, 190.0, 97.0), "envelope", 0.2,
    "UNVERIFIED", "300 -> 120 kPa supply for the Flow EZ 345 mbar (needs 1100 mbar, max 1300; V:FLUIGENT_FEZ_P)")
add("air_pressure_switch", "pneumatics", "envelope", bx(385.0, 118.0, 17.0, 405.0, 136.0, 60.0), "envelope", 0.05,
    "UNVERIFIED", "low-supply alarm (< 250 kPa) -> fault")
add("switch_valves_3x3-2", "pneumatics", "envelope", bx(250.0, 250.0, 150.0, 286.0, 274.0, 175.0), "envelope", 0.2,
    "UNVERIFIED", "3 x 3/2 solenoid valves on a manifold: ch2 -> P_mv | conjugate bottle | HQDP bottle; bottle vent")
add("A1_manifold", "bottles", "custom", bx(340.0, 122.0, 170.0, 400.0, 146.0, 190.0), "PEEK", 0.05, "[assessment]",
    "1-in / 6-out PEEK distribution block (A1 to the 5 pumps + spare)")
add("purge_restrictor", "pneumatics", "envelope", bx(402.0, 122.0, 150.0, 422.0, 146.0, 170.0), "envelope", 0.02,
    "UNVERIFIED", "fixed restrictor ~0.1 L/min dry air to the cold box")
for i, n in enumerate(["FEZ_ch1_P_c", "FEZ_ch2_P_mv_bottles"]):
    x0 = 160.0 + i * 74.0
    add(n, "pneumatics", "catalogue", bx(x0, 212.0, 17.0, x0 + 71.8, 212.0 + 91.9, 17.0 + 131.0), "envelope", 0.634,
        "V:FLUIGENT_FEZ_P", "Fluigent Flow EZ LU-FEZ-0345 (0-345 mbar, 6 W); supply 1100 mbar; outlet on the top face UNVERIFIED",
        ports=[("out", (x0 + 36, 240.0 + 22.0 * i, 148.0)), ("supply", (x0 + 36, 303.9, 40.0))])
add("FS1_SLF3S_P_a", "sensors", "catalogue", bx(300.0, 220.0, 150.0, 308.9, 268.0, 165.5), "envelope", 0.01,
    "docs/11 §5.3 (SENSIRION_SLF3S): 48 x 15.5 x 8.9", "Sensirion SLF3S-0600F on the S_A -> P_a line (rinse flows)")
add("FS2_P_s", "sensors", "catalogue", bx(325.5, 140.0, 103.0, 334.4, 188.0, 118.5), "envelope", 0.01,
    "UNVERIFIED part (LG16 class, FS >= 20 uL/min needed; LG16-0150D 7 uL/min marginal, docs/11 §5.3)",
    "flow sensor on P_s -> S_RC (fallback sweep 10 uL/min); envelope as SLF3S")

# ============================================================================================ electronics bay
add("electronics_box", "electronics", "custom", bx(4.0, 207.0, 35.0, 144.0, 396.0, 318.0), "aluminium",
    1.6, "CHOICE-B7", "1 mm Al sub-enclosure (EMC zone 'noisy'), on 4 standoffs Z 16-35 above the tray; cable "
    "glands to G_C and to the umbilical route", shape="custom")
E = []
E.append(("PSU_M_24V_350W", bx(9.0, 212.0, 40.0, 39.0, 327.0, 255.0), 0.76,
          "Mean Well LRS-350-24 class (215 x 115 x 30, 0.76 kg; search-result listings, datasheet not opened -> "
          "UNVERIFIED)", "motion + valves + logic rail"))
E.append(("PSU_T_24V_350W", bx(42.0, 212.0, 40.0, 72.0, 327.0, 255.0), 0.76, "as PSU_M (UNVERIFIED)",
          "thermal rail (Peltiers, heaters) - separate supply, docs/13 §6.3"))
E.append(("PSU_L_12V_lownoise", bx(42.0, 335.0, 40.0, 72.0, 390.0, 130.0), 0.2, "UNVERIFIED",
          "low-noise 12 V/15 W for sensors, RH/T, scanner"))
E.append(("mains_filter_fuse", bx(9.0, 335.0, 40.0, 39.0, 390.0, 130.0), 0.2, "UNVERIFIED",
          "EMI filter + fuses + K1 safety contactor (E-stop)"))
E.append(("mount_plate", bx(74.0, 210.0, 38.0, 76.0, 370.0, 315.0), 0.25, "[assessment]",
          "2 mm Al plate with DIN rails"))
E.append(("controller_watchdog", bx(78.0, 212.0, 230.0, 98.0, 312.0, 315.0), 0.15, "UNVERIFIED (MCU board to be "
          "selected)", "dock controller + independent hardware watchdog (heartbeat from Python)"))
E.append(("relay_interlock", bx(78.0, 318.0, 230.0, 98.0, 368.0, 315.0), 0.15, "UNVERIFIED",
          "relay/interlock board: E-stop loop, lid switch, safe-state relays, leak inputs"))
E.append(("stepper_drivers_x6", bx(78.0, 212.0, 140.0, 98.0, 312.0, 225.0), 0.2, "UNVERIFIED",
          "6 drivers (M_c x2, cam Z, pogo lift, rocker, spare); disabled in read windows"))
E.append(("thermal_drivers_x4", bx(78.0, 318.0, 140.0, 98.0, 368.0, 225.0), 0.2, "UNVERIFIED",
          "4 Peltier/heater channels, PWM >= 25 kHz + LC filter (CHOICE-B7), constant through reads"))
E.append(("valve_pilot_driver_21", bx(78.0, 212.0, 40.0, 98.0, 286.0, 136.0), 0.15, "UNVERIFIED",
          "21 low-side channels for the lid pilot valves (24 V), cable via the umbilical"))
E.append(("LabJack_U3_iso", bx(105.0, 212.0, 230.0, 135.0, 327.0, 305.0), 0.15,
          "LabJack U3 75 x 115 x 30 (search-result listings; labjack.com page did not state it -> UNVERIFIED)",
          "Inject Start via opto-isolator; USB via a USB isolator (U3 itself not isolated, UNVERIFIED)"))
E.append(("USB_isolator_hub", bx(105.0, 212.0, 145.0, 135.0, 262.0, 195.0), 0.1, "UNVERIFIED",
          "isolated USB hub (controller, U3, LINK, RS-485 adapter for 5 pumps)"))
E.append(("Fluigent_LINK", bx(78.0, 290.0, 40.0, 135.0, 369.0, 136.0), 0.219,
          "Fluigent LINK ~79 x 57 x 96 mm, 219 g (store listing via search; not opened -> UNVERIFIED)",
          "USB to the Flow EZ chain"))
E.append(("intake_filter_grille", bx(4.0, 331.0, 140.0, 10.0, 394.0, 300.0), 0.05, "UNVERIFIED",
          "passive intake grille + filter mat on the left wall"))
E.append(("fan_exhaust_80", bx(20.0, 371.0, 140.0, 100.0, 396.0, 220.0), 0.05, "UNVERIFIED",
          "80 mm fan on the box rear wall -> rear-panel louvre; constant speed (never switched in reads)"))
for n, b, m, src, spec in E:
    add(n, "electronics", "envelope", b, "pcb" if "PSU" not in n else "envelope", m, src, spec)
add("connector_panel", "electronics", "custom", bx(24.0, FY - s - 3.0, 40.0, 140.0, FY - s, 200.0), "aluminium",
    0.15, "CHOICE-B7", "IEC inlet + switch + fuse, PE stud, USB-B x3 (controller, DAQ via isolator, LINK), "
    "Ethernet (spare), Inject Start (2-pin, from SM-FL connector 1 pins 1-2), E-stop aux, RS-485 (spare)")
add("estop", "electronics", "catalogue", bx(55.0, -25.0, 265.0, 95.0, 0.0, 305.0), "heater", 0.1, "UNVERIFIED",
    "E-stop mushroom D40 on the front-left panel; opens K1 (safe state of docs/13 §4)", shape="cyl_y")
add("status_light", "electronics", "envelope", bx(20.0, -6.0, 312.0, 130.0, 0.0, 324.0), "gold", 0.05, "UNVERIFIED",
    "RGB light bar: green idle/run, blue read window (do not touch), amber operator action, red fault latch")

# ============================================================================================ Gamry route
bx_, by_, bz_ = P.BULKHEAD
add("gamry_lead_duct", "gamry", "custom", bx(bx_ + 0.5, by_ - 8, bz_ - 10, 440.0, by_ + 8, bz_ + 10), "copper", 0.2,
    "docs/13 §6.3; CHOICE-B10", "Al U-channel + lid, isolated from the frame (nylon standoffs), bonded only at the "
    "junction box; carries 6 shielded leads")
add("gamry_junction_box", "gamry", "custom", bx(440.0, by_ - 16, bz_ - 20, FX - s, by_ + 16, bz_ + 20), "copper",
    0.25, "CHOICE-B10", "Al box: lead terminals for the Gamry cell-cable clips, star-ground point; gland in the right "
    "panel for the 60 cm cell cable", ports=[("cell_cable", (FX, by_, bz_))])
(gx0, gy0, gz0), (gx1, gy1, gz1) = P.GAMRY
add("Gamry_Ref600plus", "bench", "catalogue", P.GAMRY, "anodised", P.GAMRY_MASS, "docs/18 §8 (gamry.com legacy page)",
    "Reference 600+, front panel (cell cable D-25) toward -Y", ports=[("cell", ((gx0 + gx1) / 2, gy0, 100.0))])


def by_group():
    g = {}
    for it in ITEMS:
        g.setdefault(it.group, []).append(it)
    return g


def get(name):
    for it in ITEMS:
        if it.name == name:
            return it
    raise KeyError(name)
