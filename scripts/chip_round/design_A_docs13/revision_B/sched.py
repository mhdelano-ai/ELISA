"""Revision B step table of cartridge A and a periodic overlap check over ALL run offsets (scratch, not in the repo).
Times in min from the run's own Inject Start. Chamber k alternates. Every dock actuation (card valve plunger, any
syringe pump, pressure channel, magnet carriage, magnet Z lift, M_h, relay) is an 'activity'. Read windows (PE2, READ)
must not overlap any activity of ANY run (own or others, offsets k*C for k = -3..3) widened by the jitter guard g.
Allowed during reads: static magnets, Peltier/heater control, the BSM's steady flow and SM-FL-internal events that
switch no card valve (Loop Offline), sensor polling.  Exclusive resources are checked separately."""
import sys, itertools
P = dict(T_inc=26.5, T_acc=13.0, C=31.0, g=0.25, G=2.0, R=3.3, D=2.25, read=4.0, pe2=4.0)
for a in sys.argv[1:]:
    k, v = a.split("="); P[k] = float(v)
T_inc, T_acc, C, g, G, R, D, RD, PE = (P[k] for k in ("T_inc", "T_acc", "C", "g", "G", "R", "D", "read", "pe2"))

tc = 1.5 + T_inc                      # incubation end = collection start (M_c,k lift)
P.setdefault("opt", 0.0)
if P["opt"] == 0.0:
    pe2 = (tc + 0.1, tc + 0.1 + PE)   # option A: PE2 during the static collection
    mc_down = pe2[1]
else:
    pe2 = (tc - 0.1 - PE, tc - 0.1)   # option B: PE2 in the last minutes of the incubation (own tidal paused)
    mc_down = tc + 1.5
g0 = mc_down + 0.1                    # gather start
r0 = g0 + G                           # rinses
d0 = r0 + R                           # drag start
a0 = d0 + D                           # accumulation start
rd = (a0 + T_acc, a0 + T_acc + RD)    # READ
res = rd[1]
bo = (res, res + 0.4)                 # bead-out RC -> BW
fl0 = (bo[1], bo[1] + 0.5)            # flush with fresh substrate: RS -> V15 -> CE/RE pocket -> RC -> G4 -> BW -> V16 (S_RC pull)
pe0 = (fl0[1], fl0[1] + 1.0)          # PE1: removal step on the fresh fill (15 s E_rest + 45 s E_det), not a read
pr = (pe0[1], pe0[1])
fl = (fl0[0], pe0[1])
# post-drag chamber work (movable): placed after the drag, must avoid other runs' read windows
post = dict(wl_ref=None, clean=None)

quiet = [("PE2", *pe2), ("READ", *rd)]
def overlap(a, b): return a[0] < b[1] and b[0] < a[1]
def conflicts(s, e, own_ok=False):
    out = []
    for (qn, qs, qe) in quiet:
        for k in range(-4, 5):
            if k == 0 and own_ok: continue
            sh = k * C; gg = 0.0 if k == 0 else g
            if overlap((s + sh, e + sh), (qs - gg, qe + gg)): out.append((qn, k))
    return out
acts = []   # (name, start, end, resources)
def A(name, s, e, res=()): acts.append((name, s, e, tuple(res)))
# pre-injection dosing (movable, executed against the predicted t0)
P.setdefault("dose", -5.0); P.setdefault("cfill", -10.0); P.setdefault("pre", -3.45)
A("conjugate meter fill (P_c, V8)", P["cfill"], P["cfill"] + 0.5, ["P_c"])
A("bead dose S_b + V(4/5)k", P["dose"], P["dose"] + 1.0, ["S_b", "chamber"])
A("conjugate push (P_mv, V(6/7)k)", P["dose"] + 1.0, P["dose"] + 1.5, ["P_mv", "chamber"])
A("V(1/2)k open, V3 closed (pre-switch; BSM 1 uL/min into IC_k)", P["pre"], P["pre"] + 0.05, ["inlet"])
_t = 1.5
while conflicts(_t, _t + 0.05): _t = round(_t + 0.05, 3)
P["trans_end"] = _t
A("V(1/2)k closed, V3 open (end transfer; BSM 1 uL/min 1.5->switch, then 2-min flush to bypass)", _t, _t + 0.05, ["inlet"])
A("C_k chase 3 uL A1 (S_A, V17/18) after the transfer", _t + 0.05, _t + 0.2, ["S_A", "chamber"])
A("M_c,k lift (collection start)", tc, tc + 0.1, ["Mc_k"])
A("M_c,k lower", mc_down, mc_down + 0.1, ["Mc_k"])
A("gather (M_d raster, carriage)", g0, g0 + G, ["carriage"])
A("rinses (S_ICk drain, S_A fill, V9/10, V17/18)", r0, r0 + R, ["carriage", "S_A", "S_IC_k", "chamber"])
A("drag + M_h up + gates", d0, d0 + D, ["carriage", "RC", "WLc"])
A("bead-out (M_h down, M_d, G4)", *bo, ["carriage", "RC"])
A("RC + BW flush (S_RC, V13, G4, V16)", *fl0, ["S_RC", "RC"])
A("PE1 removal step (Gamry, not a read)", *pe0, ["RC", "Gamry"])
# post-drag chamber side (movable); first fit after the drag
P.setdefault("clean", 4.5)
POST = [("WL_k refresh J->IC_k + WLc to waste (S_A, V11, V12, G_k)", 0.6, ["S_A", "WLc"]),
        ("chamber cleaning: drain + 3x(150 uL, 2 tidal, drain) + port chases", P["clean"], ["S_A", "S_IC_k", "chamber", "S_b"])]

# place post-drag steps greedily (0.05-min grid), after a0 (accumulation start) and avoiding all quiet windows
t = d0 + D
for name, dur, rres in POST:
    while conflicts(t, t + dur): t = round(t + 0.05, 3)
    A(name, t, t + dur, rres); t += dur
clean_end = t

print("parameters:", P)
print(f"end-of-transfer valve switch at {P['trans_end']:.2f} min; extra BSM A1 into IC_k {(P['trans_end']-1.5)*1.0 + (-P['pre'])*1.0:.2f} uL")
print(f"t_c {tc:.2f}; PE2 {pe2[0]:.2f}-{pe2[1]:.2f}; gather {g0:.2f}; rinses {r0:.2f}; drag {d0:.2f}-{a0:.2f}; "
      f"accumulation {a0:.2f}-{rd[0]:.2f}; READ {rd[0]:.2f}-{rd[1]:.2f}; RESULT {res:.2f} (margin {60-res:.2f}; "
      f"from aspiration start {res+1:.2f}); flush end {fl[1]:.2f}; chamber clean end {clean_end:.2f}")
print("\nactivity table (own frame):")
for n, s, e, r in sorted(acts, key=lambda x: x[1]): print(f"  {s:7.2f} - {e:7.2f}  {n:60s} {','.join(r)}")
print(f"  {pe2[0]:7.2f} - {pe2[1]:7.2f}  PE2 (quiet window)\n  {rd[0]:7.2f} - {rd[1]:7.2f}  READ (quiet window)")

bad = 0
print("\n(1) activities vs read windows, all offsets k*C (k=-4..4), guard +-%.2f min:" % g)
for n, s, e, r in acts:
    c = conflicts(s, e)
    if c: bad += 1; print(f"  CONFLICT {n} [{s:.2f},{e:.2f}] with {c}")
for (q1, s1, e1), (q2, s2, e2) in itertools.product(quiet, quiet):
    for k in range(-4, 5):
        if k == 0 and q1 == q2: continue
        if overlap((s1 + k * C, e1 + k * C), (s2, e2)): bad += 1; print(f"  CONFLICT Gamry {q1} (k={k}) with {q2}")
print("  none" if not bad else f"  {bad} conflicts")

print("\n(2) exclusive resources across runs (incl. same chamber two runs apart):")
bad2 = 0
for (n1, s1, e1, r1), (n2, s2, e2, r2) in itertools.product(acts, acts):
    for k in range(-4, 5):
        if k == 0: continue
        common = set(r1) & set(r2)
        if "chamber" in common or "S_IC_k" in common or "Mc_k" in common:
            if k % 2: common -= {"chamber", "S_IC_k", "Mc_k"}       # other chamber: no clash
        if common and overlap((s1 + k * C, e1 + k * C), (s2, e2)):
            bad2 += 1; print(f"  CLASH {sorted(common)}: '{n1}' of run n{k:+d} with '{n2}' of run n")
# RC sequence: previous run's flush must end before this run's PE2, and RC ops must not overlap
rc_ops = [(pe2[0], pe2[1]), (d0, rd[1]), bo, fl0, pe0]
for k in (-1, 1):
    for a in rc_ops:
        for b in rc_ops:
            if overlap((a[0] + k * C, a[1] + k * C), b): bad2 += 1; print(f"  RC CLASH offset {k}: {a} vs {b}")
# chamber cycle: same chamber reused at 2C: its first activity (bead dose) must follow clean_end - 2C
first = min(s for n, s, e, r in acts if "chamber" in r)
if clean_end - 2 * C > first: bad2 += 1; print(f"  CHAMBER CLASH: cleaning ends {clean_end:.2f} > next dose {first + 2*C:.2f}")
print("  none" if not bad2 else f"  {bad2} clashes")
print(f"  chamber idle reserve before next dose: {first + 2*C - clean_end:.2f} min (room for post-high extra rinses)")
print(f"  RC slack: next PE2 starts {pe2[0]+C:.2f} vs flush end {fl[1]:.2f} -> {pe2[0]+C-fl[1]:.2f} min")

# (3) tidal pauses in own incubation [1.5, tc]: all quiet windows of all runs (incl. guard)
pause = []
for (qn, qs, qe) in quiet:
    for k in range(-4, 5):
        gg = 0.0 if k == 0 else g
        s, e = max(1.5, qs - gg + k * C), min(tc, qe + gg + k * C)
        if s < e: pause.append((s, e, qn, k))
# also own activities that need the chamber? none during incubation
tot = sum(e - s for s, e, *_ in pause)
print(f"\n(3) tidal pauses in own incubation 1.5-{tc:.2f}: {[(round(s,2),round(e,2),q,k) for s,e,q,k in pause]} total {tot:.2f} min;"
      f" stirred {T_inc - tot:.2f} of {T_inc} min")
# (4) card budget: 14 determinations
dock = 15.0
for N in (12, 13, 14, 16):
    last = dock + (N - 1) * C + res
    print(f"(4) {N} determinations: last result {last:.0f} min after insertion = {last/60:.2f} h (docking {dock} min)")
hold = pe2[0] + 0.5 - (pe0[1] - C)
print(f"(6) PE2 monitor: open-circuit hold PE1 end -> PE2 window a start = {hold:.2f} min; 5700 residual enzymes x 968/s x hold -> {5700*968*hold*60*2*1.602e-19*1e9:.3f} nC")
print(f"(5) escape timeline: stubs filled at previous flush end {fl[1]-C:.2f}; PE2 end {pe2[1]:.2f}; READ start {rd[0]:.2f}")
