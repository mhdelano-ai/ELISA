"""Labelled section of the tier-2 flow cell through the plane y = 0 (the axis of the strip), drawn to scale from
params.py with matplotlib.  Upper panel: the whole stack.  Lower panel: the liquid path around the bed."""
from __future__ import annotations

import math

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Circle, Rectangle  # noqa: E402

from . import params as P  # noqa: E402

PEEK, PEEK2, STEEL, LIQ, VOID = "#e6cf9c", "#d9bd80", "#aab0b8", "#7fb2ee", "#ffffff"
STRIP, SHIM, RUBBER, BED, SCREEN, MEMB, WE = "#f4f4f0", "#7d848d", "#2b2b2b", "#d9822b", "#5c6470", "#b03060", \
    "#1c1c1c"


def _draw(ax, bed_ul=0.019, detail=False):
    zb, zt = P.PLATE_T, P.PLATE_T + P.BODY_T
    zo = zb + P.OUTLET_Z
    rp = P.PORT_TAP_DRILL / 2.0
    lw = 0.6 if detail else 0.4

    def rect(x0, x1, z0, z1, fc, ec="none", z=1, **kw):
        ax.add_patch(Rectangle((x0, z0), x1 - x0, z1 - z0, facecolor=fc, edgecolor=ec, linewidth=lw, zorder=z, **kw))

    def sym(r0, r1, z0, z1, fc, z=2):
        rect(r0, r1, z0, z1, fc, z=z)
        rect(-r1, -r0, z0, z1, fc, z=z)

    # solids
    rect(P.X0, P.X1, -P.BASE_T, 0, STEEL, "k")
    rect(P.X0, P.X1, 0, zb, PEEK2, "k")
    rect(P.X0, P.X1, zb, zt, PEEK, "k")
    # base: strip pocket, shim, strip, electrode
    x_free = -P.WE_FROM_FREE_END
    rect(P.POCKET_X_END, P.X1, -P.POCKET_DEPTH, 0, VOID, z=2)
    rect(x_free, P.X1, -P.POCKET_DEPTH, -P.POCKET_DEPTH + P.SHIM_T, SHIM, z=3)
    rect(x_free, x_free + P.STRIP_L, -P.GAP - P.STRIP_T, -P.GAP, STRIP, "k", z=3)
    rect(-P.WE_D / 2, P.WE_D / 2, -P.GAP - 0.03, -P.GAP, WE, z=4)
    # liquid: thin layer, exit bore, bed bore, collecting groove, riser, channel, body riser, through-hole
    rect(-P.CHAMBER_R, P.CHAMBER_R, -P.GAP, 0, LIQ, z=3)
    rect(-P.EXIT_D / 2, P.EXIT_D / 2, 0, zb, LIQ, z=3)
    rect(-P.BED_D / 2, P.BED_D / 2, zb, zb + P.INLET_FLOOR, LIQ, z=3)
    sym(P.RING_R0, P.RING_R1, 0, P.RING_DEPTH, LIQ, z=3)
    rect(P.RISER_PLATE_X - P.RISER_PLATE_D / 2, P.RISER_PLATE_X + P.RISER_PLATE_D / 2, 0, zb, LIQ, z=3)
    rect(P.CHANNEL_X_END - P.CHANNEL_W / 2, P.RISER_PLATE_X + P.CHANNEL_W / 2, zb - P.CHANNEL_DEPTH, zb, LIQ, z=3)
    rect(P.RISER_BODY_X - P.RISER_BODY_D / 2, P.RISER_BODY_X + P.RISER_BODY_D / 2, zb,
         zo + P.OUTLET_THROUGH_D / 2, LIQ, z=3)
    rect(P.X0 + P.PORT_DEPTH, P.RISER_BODY_X, zo - P.OUTLET_THROUGH_D / 2, zo + P.OUTLET_THROUGH_D / 2, LIQ, z=3)
    # ports (empty: the fitting and the tube go here)
    rect(-rp, rp, zt - P.PORT_DEPTH, zt, VOID, "k", z=3)
    rect(P.X0, P.X0 + P.PORT_DEPTH, zo - rp, zo + rp, VOID, "k", z=3)
    # O-ring grooves and O-rings
    sym(P.GROOVE_STRIP_ID / 2, P.GROOVE_STRIP_OD / 2, 0, P.GROOVE_STRIP_DEPTH, VOID, z=3)
    sym(P.GROOVE_IFACE_ID / 2, P.GROOVE_IFACE_OD / 2, zb, zb + P.GROOVE_IFACE_DEPTH, VOID, z=3)
    for (d_i, cs), zc in ((P.ORING_STRIP, (P.GROOVE_STRIP_DEPTH - P.GAP) / 2), (P.ORING_IFACE,
                                                                               zb + P.GROOVE_IFACE_DEPTH / 2)):
        for s in (-1, 1):
            ax.add_patch(Circle((s * (d_i + cs) / 2, zc), cs / 2 * 0.72, facecolor=RUBBER, edgecolor="none", zorder=4))
    # retainer pocket in the plate: washer, screen, membrane; then the bed in the body
    zp = zb - P.RET_POCKET_DEPTH
    rect(-P.RET_POCKET_D / 2, P.RET_POCKET_D / 2, zp, zb, VOID, z=4)
    sym(P.WASHER_ID / 2, P.WASHER_OD / 2, zp, zp + P.WASHER_H, RUBBER, z=5)
    rect(-P.WASHER_ID / 2, P.WASHER_ID / 2, zp, zp + P.WASHER_H, LIQ, z=5)
    rect(-P.SCREEN_D / 2, P.SCREEN_D / 2, zp + P.WASHER_H, zp + P.WASHER_H + P.SCREEN_T, SCREEN, z=5)
    rect(-P.MEMBRANE_DISC_D / 2, P.MEMBRANE_DISC_D / 2, zb - P.MEMBRANE_T, zb, MEMB, z=6)
    z_seat = zb
    L_bed = bed_ul / (math.pi * P.BED_D ** 2 / 4)
    rect(-P.BED_D / 2, P.BED_D / 2, z_seat, z_seat + L_bed, BED, z=6)
    return zb, zt, zo, L_bed


def draw(path, bed_ul=0.019):
    fig, (a1, a2, a3) = plt.subplots(3, 1, figsize=(11, 19.5), gridspec_kw=dict(height_ratios=[1.0, 1.25, 0.8]))
    zp = P.PLATE_T - P.RET_POCKET_DEPTH
    zb, zt, zo, L_bed = _draw(a1, bed_ul)
    a1.set_xlim(P.X0 - 9, P.STRIP_L - P.WE_FROM_FREE_END + 9)
    a1.set_ylim(-P.BASE_T - 4.5, zt + 5)
    a1.set_aspect("equal")
    a1.set_title("Tier-2 flow cell, section along the strip (y = 0), to scale; dimensions in mm", fontsize=11)
    kw = dict(fontsize=8.5, arrowprops=dict(arrowstyle="-", lw=0.6, color="0.25"), va="center")
    a1.annotate("inlet port 1/4-28, flat bottom\n(transfer line from the injector)", (0, zt - 2), (6, zt + 3), **kw)
    a1.annotate("outlet port 1/4-28\n(to waste)", (P.X0 + 3, zo), (P.X0 - 8.5, zo + 6), **kw)
    a1.annotate("body, PEEK", (9, zb + 7), (16, zb + 9), **kw)
    a1.annotate("nozzle plate, PEEK", (11, zb / 2), (16, zb + 3.5), **kw)
    a1.annotate("base, 316L", (9, -4), (15, -4), **kw)
    a1.annotate("MicruX strip, pads to the\nMicruX connector cable", (21, -P.GAP - 0.2), (15, -10.3), **kw)
    a1.annotate("4 × M4 and 2 × ⌀3 pins lie outside\nthis plane (y = ±16)", (P.X0 + 6, zt), (P.X0 - 8.5, zt + 3.5),
                fontsize=8.5, va="center", arrowprops=dict(arrowstyle="-", lw=0.0, color="none"))
    a1.set_xlabel("x (mm), + towards the contact pads")
    a1.set_ylabel("z (mm), 0 = top face of the base")

    _draw(a2, bed_ul, detail=True)
    a2.set_xlim(-8.2, 8.2)
    a2.set_ylim(-1.4, 6.4)
    a2.set_aspect("equal")
    a2.set_title("Detail: bed, retainer and thin layer (same section)", fontsize=11)
    z_seat = zb
    zp = zb - P.RET_POCKET_DEPTH
    lab = [
        (f"bed bore ⌀{P.BED_D} × {P.INLET_FLOOR} in the port floor", (0.0, zb + 1.6), (2.4, 5.9)),
        (f"bed: 1×10⁶ beads of 2.8 µm = {L_bed:.2f} mm (drawn)", (0.1, z_seat + L_bed / 2), (2.4, 5.3)),
        (f"membrane ⌀{P.MEMBRANE_DISC_D}, 1 µm pores, pressed against the body face\nby a 2 µm screen on an "
         f"FKM washer ⌀{P.WASHER_OD}/⌀{P.WASHER_ID}\n(the spring), in a pocket ⌀{P.RET_POCKET_D} × "
         f"{P.RET_POCKET_DEPTH} in the plate", (0.7, zp + 0.1), (2.4, 4.4)),
        (f"O-ring {P.ORING_IFACE[0]:.0f} × {P.ORING_IFACE[1]:.0f}, body to plate", (6.5, zb + 0.4), (4.2, 3.75)),
        (f"exit bore ⌀{P.EXIT_D} × {P.EXIT_LENGTH:.2f}; with the washer hole {P.EXIT_VOLUME_UL:.2f} µL",
         (0.2, 1.3), (1.1, 1.75)),
        (f"O-ring {P.ORING_STRIP[0]:.0f} × {P.ORING_STRIP[1]:.0f} on the strip", (4.05, 0.3), (5.0, 1.15)),
        (f"thin layer, gap {P.GAP:.2f}", (1.0, -P.GAP / 2), (3.4, -0.75)),
        (f"working electrode ⌀{P.WE_D:.0f}", (-0.6, -P.GAP - 0.02), (-2.4, -1.05)),
        (f"shim {P.SHIM_T} under the strip sets the gap", (5.6, -P.POCKET_DEPTH + P.SHIM_T / 2), (3.4, -1.2)),
        (f"collecting groove r {P.RING_R0}–{P.RING_R1}", (2.6, 0.25), (1.1, 0.75)),
        ("riser and cross channel\nin the plate", (-3.6, zb - 0.25), (-8.0, 1.3)),
        (f"riser ⌀{P.RISER_BODY_D} to the outlet port", (P.RISER_BODY_X, 4.4), (-8.0, 5.6)),
        ("stop for the strip", (P.POCKET_X_END, -P.POCKET_DEPTH / 2), (-8.0, -0.9)),
    ]
    for txt, xy, xyt in lab:
        a2.annotate(txt, xy, xyt, fontsize=8.5, va="center",
                    arrowprops=dict(arrowstyle="-", lw=0.6, color="0.2"), zorder=10)
    for (x, z, dx, dz) in ((0, 4.6, 0, -0.7), (0, 1.9, 0, -0.7), (0.6, -0.05, 0.9, 0), (-0.6, -0.05, -0.9, 0),
                           (-2.6, 0.8, 0, 0.8), (-4.6, 3.2, 0, 0.9)):
        a2.annotate("", (x + dx, z + dz), (x, z), arrowprops=dict(arrowstyle="->", lw=1.0, color="#103a80"),
                    zorder=9)
    a2.set_xlabel("x (mm)")
    a2.set_ylabel("z (mm)")

    # third panel: the joint between bed bore and exit bore
    _draw(a3, bed_ul, detail=True)
    a3.set_xlim(-1.6, 1.6)
    a3.set_ylim(zp - 0.35, zb + 0.35)
    a3.set_aspect("equal")
    a3.set_title("Joint between bed bore and exit bore (Revision B): the washer is the spring that presses screen "
                 "and membrane\nagainst the flat underside of the body; body and plate meet face to face", fontsize=10)
    for txt, xy, xyt in [
        ("body (PEEK), underside flat, Ra ≤ 0.4", (-1.2, zb + 0.15), (-1.55, zb + 0.30)),
        (f"bed in the ⌀{P.BED_D} bore", (0.0, zb + 0.06), (0.35, zb + 0.28)),
        (f"membrane ⌀{P.MEMBRANE_DISC_D} × {P.MEMBRANE_T} (sealing band 0.5 wide)", (0.6, zb - 0.005), (0.5, zb + 0.2)),
        (f"screen ⌀{P.SCREEN_D:.2f} × {P.SCREEN_T}", (0.7, zb - 0.05), (0.95, zb + 0.04)),
        (f"washer ⌀{P.WASHER_OD}/⌀{P.WASHER_ID}, {P.WASHER_T} → {P.WASHER_H:.3f}", (0.5, zp + 0.09), (0.95, zp - 0.05)),
        (f"pocket ⌀{P.RET_POCKET_D} × {P.RET_POCKET_DEPTH}", (0.8, zp + 0.01), (0.95, zp - 0.2)),
        (f"exit bore ⌀{P.EXIT_D}", (0.0, zp - 0.2), (-1.0, zp - 0.25)),
        ("nozzle plate (PEEK)", (-1.2, zp), (-1.55, zp + 0.1)),
    ]:
        a3.annotate(txt, xy, xyt, fontsize=8.5, va="center", arrowprops=dict(arrowstyle="-", lw=0.6, color="0.2"),
                    zorder=10)
    a3.set_xlabel("x (mm)")
    a3.set_ylabel("z (mm)")
    fig.tight_layout()
    fig.savefig(path, dpi=140)
    plt.close(fig)
    return path
