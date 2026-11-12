"""Three-window step read (Revision B, docs/13 s3.5.4): 1-D thin layer, floor z=0 (no flux, enzyme source),
WE at z=h (c=0 during E_det windows, no flux at E_rest/open circuit). Finite differences.
Sequence after accumulation: pre-rest 30 s (E_rest), a 60 s, rest 15 s, b 60 s, rest 15 s, c 60 s.
Q_net = Q_a - 2 Q_b + Q_c. Reports (1) the weight of accumulated product in Q_net, (2) the residual of a constant
enzyme turnover during the read, (3) the old docs/13 pair (90/15/90) for comparison."""
import numpy as np
def run(seq, D=9e-10, h=2.0e-4, n=80, acc=13 * 60, src=1.0):
    dz = h / n; z = (np.arange(n) + 0.5) * dz; c = np.zeros(n); dt = 0.2 * dz * dz / D
    def step(c, T, absorbing, s):
        q = 0.0; t = 0.0
        while t < T - 1e-12:
            d = min(dt, T - t)
            cl = np.concatenate([[c[0]], c, [-c[-1] if absorbing else c[-1]]])   # ghost cells
            lap = (cl[2:] - 2 * cl[1:-1] + cl[:-2]) / dz ** 2
            cn = c + D * d * lap
            cn[0] += s * d / dz                                               # source at the floor (per area)
            if absorbing: q += D * (c[-1] - (-c[-1])) / dz * d                # flux into the WE
            c = cn; t += d
        return c, q
    c, _ = step(c, acc, False, src)            # accumulation: source on, WE open
    Q = []
    for T, ab in seq:
        c, q = step(c, T, ab, src); Q.append((q, ab))
    return [q for q, ab in Q if ab], src * acc
seq3 = [(30, False), (60, True), (15, False), (60, True), (15, False), (60, True)]
seq2 = [(15, False), (90, True), (15, False), (90, True)]
for D in (9e-10, 7e-10, 1.1e-9):
    # (1)+(2): with source on during the read; separately the source-off case gives the accumulated-product weight
    qa, qb, qc = run(seq3, D=D)[0]; Nacc = 13 * 60
    qa0, qb0, qc0 = run([(30, False), (60, True), (15, False), (60, True), (15, False), (60, True)], D=D, src=1.0)[0]
    # accumulated-only: run with source switched off at read start -> emulate by subtracting a pure-read-source run
    def read_only_source(D):
        # source starts at read start (no accumulation)
        return run(seq3, D=D, acc=0.0)[0]
    ra, rb, rc = read_only_source(D)
    net_acc = (qa - ra) - 2 * (qb - rb) + (qc - rc)
    net_src = ra - 2 * rb + rc
    tot_acc = Nacc                       # product made during accumulation (per unit area)
    pre = 30.0                           # made during the pre-rest is part of 'read_only_source' (source from read start)
    print(f"D {D:.1e}: Q_net weight of accumulated product {net_acc/tot_acc:.4f}; constant turnover during the read "
          f"contributes {net_src:.2f} s-equivalents (vs {tot_acc:.0f} s accumulation: {100*net_src/tot_acc:+.2f} %); "
          f"single window a alone collects {(qa-ra)/tot_acc:.4f}")
    (pa, pb) = run(seq2, D=D)[0]; (sa, sb) = run(seq2, D=D, acc=0.0)[0]
    print(f"          docs/13 pair 90/15/90: weight {((pa-sa)-(pb-sb))/tot_acc:.4f}; turnover term {100*(sa-sb)/tot_acc:+.2f} %")
# drift and noise requirements
T, Dl = 60.0, 75.0
print(f"\nlinear drift d: pair error d*Delta*T; three-window error 0 (exact); curvature d2: error d2*Delta^2*T = d2*{Dl**2*T:.0f} s^3")
d = 5e-12 / 60
print(f"  repository drift 5 pA/min (hw.gamry.baseline_drift): docs/13 pair (105 s, 90 s) {d*105*90*1e9:.2f} nC; 60/75 pair {d*Dl*T*1e9:.2f} nC")
for budget in (0.025, 0.05):
    d2 = budget * 1e-9 / (Dl ** 2 * T)
    print(f"  curvature allowed for {budget} nC residual: {d2:.2e} A/s2 = {d2*3600*1e12:.3f} pA/min2 -> a 5 pA/min drift must keep its rate for a time constant >= {5/(d2*3600*1e12):.0f} min")
sw = np.sqrt(T / 2.0)
print(f"\nwhite noise (model form i*sqrt(T/2B), B = 1 Hz): per-window {sw:.2f} s * i; SD(Q_net) = sqrt(6) * that = {np.sqrt(6)*sw:.2f} s * i")
for sd in (0.05, 0.08):
    print(f"  SD(Q_net) <= {sd} nC needs i_rms <= {sd*1e-9/(np.sqrt(6)*sw)*1e12:.2f} pA (pair: {sd*1e-9/(np.sqrt(2)*np.sqrt(90/2))*1e12:.2f} pA at 90 s)")
print(f"model mapping (docs/15 S2): sigma_Q,model = i_ref*sqrt(60/2)*sqrt(2) = {np.sqrt(30)*np.sqrt(2):.3f} s * i_ref -> 3 pA = {3e-12*np.sqrt(60):.3e} C")
