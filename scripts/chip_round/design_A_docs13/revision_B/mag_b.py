"""Revision B magnet arithmetic for docs/13 (scratch, not in the repository).
Field of uniformly magnetised NdFeB blocks by surface-charge integration (B_r = 1.3 T, UNVERIFIED), bead moment
m = 1.15e-13 A m^2 (M-280, saturated, UNVERIFIED), Stokes drag 6 pi eta r = 2.35e-8 N s/m, wall factor 3 (UNVERIFIED).
Outputs: (1) point checks (reproduce docs/13 / docs/15 numbers), (2) capture half-width of a moving M_d for a raster
gather with friction coefficients 0 / 0.2 / 0.4, (3) forces from lowered or neighbouring magnets on incubating beads."""
import numpy as np
Br = 1.3; m = 1.15e-13; drag = 2.35e-8; wall = 3.0; mm = 1e-3

def Bfield(P, a, b, c, N=80):
    """P: (...,3) points in m; block |x|<a/2, |y|<b/2, -c<z<0, magnetised +z."""
    xs = (np.arange(N) + 0.5) / N * a - a / 2; ys = (np.arange(N) + 0.5) / N * b - b / 2
    X, Y = np.meshgrid(xs, ys); X = X.ravel(); Y = Y.ravel(); dA = (a / N) * (b / N)
    P = np.asarray(P, float); sh = P.shape[:-1]; P = P.reshape(-1, 3); out = np.zeros_like(P)
    for i0 in range(0, len(P), 400):
        p = P[i0:i0 + 400]
        for zf, s in ((0.0, 1.0), (-c, -1.0)):
            R = np.stack([p[:, 0, None] - X[None], p[:, 1, None] - Y[None], np.broadcast_to(p[:, 2, None] - zf, (len(p), len(X)))], -1)
            r3 = np.sum(R ** 2, -1) ** 1.5
            out[i0:i0 + 400] += s * np.sum(R / r3[..., None], 1) * dA
    return (Br / (4 * np.pi) * out).reshape(sh + (3,))

def absB(P, blk): return np.linalg.norm(Bfield(P, *blk), axis=-1)
def grad(pt, blk, h=2e-5):
    pt = np.asarray(pt, float); g = []
    for i in range(3):
        d = np.zeros(3); d[i] = h
        g.append((absB(pt + d, blk) - absB(pt - d, blk)) / (2 * h))
    return np.array(g)

Mc = (10 * mm, 10 * mm, 5 * mm); Md = (2 * mm, 2 * mm, 4 * mm)
zb = 0.30 * mm   # bead plane above the magnet face (gap 0.16 + foil 0.14)

def rep(lbl, pt, blk):
    Bv = absB(np.array(pt), blk); g = grad(pt, blk)
    print(f"  {lbl:52s} |B| {Bv:.3f} T  grad (x,y,z) ({g[0]:7.0f},{g[1]:7.0f},{g[2]:7.0f}) T/m  F_lat {m*np.hypot(g[0],g[1])*1e12:6.2f} pN  F_z {m*abs(g[2])*1e12:6.2f} pN")

print("== (1) point checks")
rep("M_c centre, 3.7 mm (fill top)", (0, 0, 3.7 * mm), Mc)
rep("M_d edge x=1.0 mm, bead plane", (1.0 * mm, 0, zb), Md)
rep("M_d x=1.1 mm, bead plane", (1.1 * mm, 0, zb), Md)
rep("M_d x=1.5 mm, bead plane", (1.5 * mm, 0, zb), Md)
rep("M_d x=2.0 mm, bead plane", (2.0 * mm, 0, zb), Md)
rep("M_d x=2.5 mm, bead plane", (2.5 * mm, 0, zb), Md)

print("== (2) raster gather with M_d: capture half-width (bead on the floor, magnet moving +x)")
# precompute |B| on a grid at the bead plane and at +-dz, magnet frame
h = 0.025 * mm
xs = np.arange(-4.0, 4.0001, 0.025) * mm; ys = np.arange(0, 3.5001, 0.025) * mm
XX, YY = np.meshgrid(xs, ys, indexing="ij")
P0 = np.stack([XX, YY, np.full_like(XX, zb)], -1)
import os
if os.path.exists("md_grid.npz"):
    _z = np.load("md_grid.npz"); B0, Bup, Bdn = _z["B0"], _z["Bup"], _z["Bdn"]
else:
    B0 = absB(P0, Md); Bup = absB(P0 + np.array([0, 0, h]), Md); Bdn = absB(P0 + np.array([0, 0, -h]), Md)
    np.savez("md_grid.npz", B0=B0, Bup=Bup, Bdn=Bdn)
gx = np.gradient(B0, xs, axis=0); gy = np.gradient(B0, ys, axis=1); gz = (Bup - Bdn) / (2 * h)
from scipy.interpolate import RegularGridInterpolator as RGI
Ix = RGI((xs, ys), gx, bounds_error=False, fill_value=0.0); Iy = RGI((xs, ys), gy, bounds_error=False, fill_value=0.0)
Iz = RGI((xs, ys), gz, bounds_error=False, fill_value=0.0)
def captured(y0, v, mu, L=7.0 * mm):
    """bead starts at x = +4 mm ahead of the magnet centre (magnet frame), lateral y0; the magnet moves +x at v,
    i.e. in the magnet frame the bead drifts -x at v unless magnetic force exceeds friction. Integrate 2 L / v."""
    x, y = 3.9 * mm, y0; dt = 0.02; t = 0.0
    while t < L / v:
        p = [(x, abs(y))]; fx = m * float(Ix(p)[0]); fy = m * float(Iy(p)[0]) * (1.0 if y >= 0 else -1.0); fz = m * abs(float(Iz(p)[0]))
        fl = np.hypot(fx, fy); vx = vy = 0.0
        if fl > mu * fz and fl > 0:
            s = (fl - mu * fz) / (wall * drag); vx, vy = s * fx / fl, s * fy / fl
        x += (vx - v) * dt; y += vy * dt; t += dt
        if x < -3.9 * mm: return False, x, y
    return (abs(x) < 1.6 * mm and abs(y) < 1.6 * mm), x, y
for v in (0.2, 0.3):
    for mu in (0.0, 0.2, 0.4):
        cap = [y0 for y0 in np.arange(0.0, 3.01, 0.1) * mm if captured(y0, v * mm, mu)[0]]
        w = max(cap) / mm if cap else float("nan")
        print(f"  v {v:.1f} mm/s mu {mu:.1f}: captured for |y0| <= {w:.1f} mm  (stripe {2*w:.1f} mm)")

print("== (3) lowered / neighbouring magnets: force on a bead in an incubating chamber (saturated m: upper bound)")
for dz in (5, 10, 15, 20, 25, 30):
    for lbl, pt in (("floor centre", (0, 0, (0.30 + dz) * mm)), ("floor, 4 mm off-axis", (4 * mm, 0, (0.30 + dz) * mm))):
        g = grad(pt, Mc); print(f"  M_c lowered {dz:2d} mm, {lbl:22s}: |B| {absB(np.array(pt), Mc):.4f} T  F {m*np.linalg.norm(g)*1e12:7.3f} pN")
for lbl, pt in (("M_c,k up; other chamber near edge (lateral 12 mm)", (12 * mm, 0, zb)),
                ("M_c,k up; other chamber near edge, fill top", (12 * mm, 0, 3.2 * mm)),
                ("M_d up at chamber-k wall; other chamber edge (8 mm)", (8 * mm, 0, zb)),
                ("M_d up; 6 mm away", (6 * mm, 0, zb))):
    blk = Mc if "M_c" in lbl else Md
    g = grad(pt, blk); print(f"  {lbl:55s}: F {m*np.linalg.norm(g)*1e12:7.3f} pN")
for dz in (4, 6, 8):
    pt = (0, 0, (0.30 + dz) * mm); g = grad(pt, Md)
    print(f"  M_d lowered {dz} mm (transit under the anvil), bead plane directly above: F {m*np.linalg.norm(g)*1e12:7.3f} pN")
print("  reference: buoyant weight of a bead 0.046 pN (docs/13 s3.3.2)")
