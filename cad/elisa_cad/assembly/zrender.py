"""Software z-buffer renderer for the integrated assembly (docs/23 §3.3).

Why: common.render_png sorts triangles by mean depth (painter's algorithm) and shows artefacts where large faces
overlap small bodies (reported by every module agent). This renderer rasterises every triangle into a per-pixel depth
buffer (numpy, vectorised per triangle-size class), so occlusion is exact at pixel level, and draws part outlines
from item-id and depth discontinuities. Orthographic projection, flat shading, optional translucent second pass.

render(items, path, view, ...): items = [(shape, rgba_or_material, label_or_None), ...] in one coordinate system.
Views: a named view of common._VIEW_DIRS or an explicit (eye_dir, up) tuple. Section views: pass already-cut solids
and `cut_plane=(point, normal)` to tint the cut faces.
"""
from __future__ import annotations

import math

import numpy as np

from .. import common as C

VIEWS = {  # eye direction (from target toward the viewer), up vector
    "iso_fl": ((-1.0, -1.25, 0.95), (0, 0, 1)),     # front-left, from above
    "iso_fr": ((1.0, -1.25, 0.95), (0, 0, 1)),      # front-right, from above
    "iso_fl_steep": ((-0.65, -1.15, 1.7), (0, 0, 1)),  # front-left, steeper (into the open well)
    "iso_rl": ((-1.0, 1.2, 0.9), (0, 0, 1)),
    "front": ((0, -1, 0), (0, 0, 1)), "back": ((0, 1, 0), (0, 0, 1)),
    "left": ((-1, 0, 0), (0, 0, 1)), "right": ((1, 0, 0), (0, 0, 1)),
    "top": ((0, 0, 1), (0, 1, 0)),
}


def _basis(view):
    eye, up = VIEWS[view] if isinstance(view, str) else view
    e = np.array(eye, float)
    e /= np.linalg.norm(e)
    u = np.array(up, float)
    sx = np.cross(u, e)
    if np.linalg.norm(sx) < 1e-6:
        sx = np.array([1.0, 0, 0])
    sx /= np.linalg.norm(sx)
    sy = np.cross(e, sx)
    return np.vstack([sx, sy, e])


def _rgba(m):
    return np.array(C.color(m) if isinstance(m, str) else m, float)


def tess(shape, tol):
    try:
        v, t = C.tessellate(shape, tol, 0.25)
    except Exception:  # noqa: BLE001
        return np.zeros((0, 3)), np.zeros((0, 3), int)
    return v, t


def _raster(P, depth, cols, ids, W, H, zbuf, cbuf, ibuf, alpha_pass=False, abuf=None):
    """P: (n,3,2) pixel coords, depth (n,3), cols (n,3) rgb, ids (n,). Updates buffers in place."""
    x0 = np.floor(P[:, :, 0].min(1)).astype(int)
    y0 = np.floor(P[:, :, 1].min(1)).astype(int)
    x1 = np.ceil(P[:, :, 0].max(1)).astype(int)
    y1 = np.ceil(P[:, :, 1].max(1)).astype(int)
    keep = (x1 >= 0) & (y1 >= 0) & (x0 < W) & (y0 < H)
    ext = np.maximum(x1 - x0, y1 - y0) + 1
    lo = 0
    for k in (2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192):
        sel = np.nonzero(keep & (ext <= k) & (ext > lo))[0]
        lo = k
        if len(sel) == 0:
            continue
        oy, ox = np.mgrid[0:k, 0:k]
        ox, oy = ox.ravel(), oy.ravel()
        chunk = max(1, int(3e6 // (k * k)))
        for c0 in range(0, len(sel), chunk):
            s = sel[c0:c0 + chunk]
            px = x0[s, None] + ox[None, :]
            py = y0[s, None] + oy[None, :]
            cx, cy = px + 0.5, py + 0.5
            a, b, c = P[s, 0], P[s, 1], P[s, 2]
            den = (b[:, 1] - c[:, 1]) * (a[:, 0] - c[:, 0]) + (c[:, 0] - b[:, 0]) * (a[:, 1] - c[:, 1])
            ok = np.abs(den) > 1e-12
            den = np.where(ok, den, 1.0)
            l1 = ((b[:, 1] - c[:, 1])[:, None] * (cx - c[:, 0][:, None]) +
                  (c[:, 0] - b[:, 0])[:, None] * (cy - c[:, 1][:, None])) / den[:, None]
            l2 = ((c[:, 1] - a[:, 1])[:, None] * (cx - c[:, 0][:, None]) +
                  (a[:, 0] - c[:, 0])[:, None] * (cy - c[:, 1][:, None])) / den[:, None]
            l3 = 1 - l1 - l2
            eps = -1e-4
            m = (l1 >= eps) & (l2 >= eps) & (l3 >= eps) & ok[:, None] & (px >= 0) & (py >= 0) & (px < W) & (py < H)
            if not m.any():
                continue
            d = depth[s, 0][:, None] * l1 + depth[s, 1][:, None] * l2 + depth[s, 2][:, None] * l3
            ti = np.broadcast_to(s[:, None], m.shape)[m]
            pix = (py[m] * W + px[m]).astype(np.int64)
            dd = d[m]
            if not alpha_pass:
                o = np.lexsort((dd, pix))
                pix, dd, ti = pix[o], dd[o], ti[o]
                last = np.r_[pix[1:] != pix[:-1], True]
                pix, dd, ti = pix[last], dd[last], ti[last]
                upd = dd > zbuf[pix]
                zbuf[pix[upd]] = dd[upd]
                cbuf[pix[upd]] = cols[ti[upd], :3]
                ibuf[pix[upd]] = ids[ti[upd]]
            else:
                vis = dd > zbuf[pix] + 1e-6
                pix, ti = pix[vis], ti[vis]
                # accumulate translucent layers (order-independent approximation: average colour, 1-prod(1-a))
                np.add.at(abuf[0], pix, cols[ti, :3] * cols[ti, 3:4])
                np.add.at(abuf[1], pix, cols[ti, 3])


def render(items, path, view="iso_fl", px=(1800, 1300), title=None, labels=None, bounds=None, margin=0.04,
           tol=None, light=(-0.35, -0.55, 0.85), cut_plane=None, outline=True, note=None, bg=(1, 1, 1),
           legend=None, dpi=150):
    """items: [(shape, material|rgba, name), ...]. bounds: optional (xmin, xmax, ymin, ymax) in screen mm.
    labels: [(xyz, text, (dx_px, dy_px))]. Returns path."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    M = _basis(view)
    W, H = px
    L = np.array(light, float)
    L /= np.linalg.norm(L)
    # pass 1: bounds from bounding boxes
    if bounds is None:
        pts = []
        for s, _m, _n in items:
            bb = C._shape(s).BoundingBox()
            for x in (bb.xmin, bb.xmax):
                for y in (bb.ymin, bb.ymax):
                    for z in (bb.zmin, bb.zmax):
                        pts.append((x, y, z))
        q = np.array(pts) @ M.T
        bounds = (q[:, 0].min(), q[:, 0].max(), q[:, 1].min(), q[:, 1].max())
    xmin, xmax, ymin, ymax = bounds
    dx, dy = xmax - xmin, ymax - ymin
    xmin, xmax, ymin, ymax = xmin - margin * dx, xmax + margin * dx, ymin - margin * dy, ymax + margin * dy
    scale = min(W / (xmax - xmin), H / (ymax - ymin))           # px per mm
    W = int(math.ceil((xmax - xmin) * scale))
    H = int(math.ceil((ymax - ymin) * scale))
    mmpp = 1.0 / scale
    tol = tol or max(0.002, 0.6 * mmpp)
    zbuf = np.full(W * H, -np.inf)
    cbuf = np.tile(np.array(bg, float), (W * H, 1))
    ibuf = np.full(W * H, -1, np.int64)
    abuf = (np.zeros((W * H, 3)), np.zeros(W * H))
    cn = None if cut_plane is None else (np.array(cut_plane[0], float), np.array(cut_plane[1], float) /
                                         np.linalg.norm(cut_plane[1]))
    trans = []
    for idx, (s, mat, _n) in enumerate(items):
        rgba = _rgba(mat)
        v, t = tess(C._shape(s), tol)
        if len(t) == 0:
            continue
        q = v @ M.T
        P = np.stack([(q[:, 0] - xmin) * scale, (ymax - q[:, 1]) * scale], 1)[t]
        depth = q[:, 2][t]
        tri = v[t]
        n = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0])
        nn = np.linalg.norm(n, axis=1)
        nn[nn == 0] = 1
        n /= nn[:, None]
        shade = 0.42 + 0.58 * np.abs(n @ L)
        col = np.tile(rgba, (len(t), 1))
        col[:, :3] = np.clip(col[:, :3] * shade[:, None], 0, 1)
        if cn is not None:
            cen = tri.mean(1)
            on = (np.abs((cen - cn[0]) @ cn[1]) < 0.02) & (np.abs(n @ cn[1]) > 0.999)
            col[on, :3] = np.clip(rgba[:3] * 0.80 + 0.06, 0, 1)
        ids = np.full(len(t), idx)
        if rgba[3] < 0.5:
            trans.append((P, depth, col, ids))
            continue
        _raster(P, depth, col, ids, W, H, zbuf, cbuf, ibuf)
    for P, depth, col, ids in trans:
        _raster(P, depth, col, ids, W, H, zbuf, cbuf, ibuf, alpha_pass=True, abuf=abuf)
    img = cbuf.copy()
    a = np.clip(abuf[1], 0, 0.85)
    has = abuf[1] > 0
    mean_c = np.zeros_like(img)
    mean_c[has] = abuf[0][has] / abuf[1][has][:, None]
    img[has] = img[has] * (1 - a[has, None]) + mean_c[has] * a[has, None]
    img = img.reshape(H, W, 3)
    if outline:
        ib = ibuf.reshape(H, W)
        zb = zbuf.reshape(H, W)
        edge = np.zeros((H, W), bool)
        thr = max(0.6, 3.0 * mmpp)
        for sh in ((0, 1), (1, 0)):
            a1 = ib[:-sh[0] or None, :-sh[1] or None]
            a2 = ib[sh[0]:, sh[1]:]
            z1 = zb[:-sh[0] or None, :-sh[1] or None]
            z2 = zb[sh[0]:, sh[1]:]
            e = (a1 != a2) | (np.abs(np.nan_to_num(z1 - z2, posinf=1e3, neginf=1e3)) > thr)
            edge[:e.shape[0], :e.shape[1]] |= e
        img[edge] = img[edge] * 0.35
    fig = plt.figure(figsize=(W / dpi, H / dpi + (0.45 if title else 0.1)), dpi=dpi)
    ax = fig.add_axes([0, 0, 1, H / (H + (0.45 if title else 0.1) * dpi)])
    ax.imshow(img, interpolation="antialiased")
    ax.set_xlim(0, W)
    ax.set_ylim(H, 0)
    ax.axis("off")
    if labels:
        for lab in labels:
            xyz, txt = lab[0], lab[1]
            off = lab[2] if len(lab) > 2 and lab[2] is not None else (40, -40)
            q = np.array(xyz, float) @ M.T
            u, w = (q[0] - xmin) * scale, (ymax - q[1]) * scale
            ax.annotate(txt, (u, w), xytext=(u + off[0], w + off[1]), fontsize=7.5, ha="center", va="center",
                        bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="0.4", lw=0.5, alpha=0.9),
                        arrowprops=dict(arrowstyle="-", lw=0.6, color="0.2"))
    if legend:
        from matplotlib.patches import Patch
        ax.legend(handles=[Patch(fc=_rgba(m)[:3], ec="k", lw=0.4, label=t) for t, m in legend], loc="lower left",
                  fontsize=7, framealpha=0.9)
    if note:
        ax.text(0.005, 0.995, note, transform=ax.transAxes, fontsize=7, va="top", ha="left",
                bbox=dict(fc="white", ec="none", alpha=0.8))
    if title:
        fig.suptitle(title, fontsize=10, y=0.995, va="top")
    # scale bar
    bar = 10 ** math.floor(math.log10((xmax - xmin) / 5))
    ax.plot([W * 0.02, W * 0.02 + bar * scale], [H * 0.975, H * 0.975], "k-", lw=2)
    ax.text(W * 0.02 + bar * scale / 2, H * 0.965, f"{bar:g} mm", ha="center", va="bottom", fontsize=7)
    fig.savefig(str(path), dpi=dpi)
    plt.close(fig)
    return str(path)
