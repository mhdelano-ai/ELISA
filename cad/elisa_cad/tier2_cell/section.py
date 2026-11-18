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
    # retainer and bed
    z_seat = zb + P.RETAINER_POCKET_DEPTH
    rect(-P.RETAINER_POCKET_D / 2, P.RETAINER_POCKET_D / 2, zb, z_seat, SCREEN, z=5)
    rect(-0.75, 0.75, z_seat - 0.012, z_seat, MEMB, z=6)
    L_bed = bed_ul / (math.pi * P.BED_D ** 2 / 4)
    rect(-P.BED_D / 2, P.BED_D / 2, z_seat, z_seat + L_bed, BED, z=6)
    return zb, zt, zo, L_bed


def draw(path, bed_ul=0.019):
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(11, 13.5), gridspec_kw=dict(height_ratios=[1.0, 1.25]))
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
    z_seat = zb + P.RETAINER_POCKET_DEPTH
    lab = [
        (f"bed bore ⌀{P.BED_D} × {P.INLET_FLOOR} in the port floor", (0.0, zb + 1.6), (2.4, 5.9)),
        (f"bed: 1×10⁶ beads of 2.8 µm = {L_bed:.2f} mm (drawn)", (0.1, z_seat + L_bed / 2), (2.4, 5.3)),
        ("membrane, 1 µm pores, on a 2 µm screen\n(1/16 in × 0.075) in a seat ⌀"
         f"{P.RETAINER_POCKET_D} × {P.RETAINER_POCKET_DEPTH}", (0.7, zb + 0.03), (2.4, 4.45)),
        (f"O-ring {P.ORING_IFACE[0]:.0f} × {P.ORING_IFACE[1]:.0f}, body to plate", (6.5, zb + 0.4), (4.2, 3.75)),
        (f"exit bore ⌀{P.EXIT_D} × {P.PLATE_T} ({P.EXIT_VOLUME_UL:.2f} µL)", (0.2, 1.3), (1.1, 1.75)),
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
    fig.tight_layout()
    fig.savefig(path, dpi=140)
    plt.close(fig)
    return path
