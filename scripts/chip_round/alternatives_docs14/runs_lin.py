# Exact additive contamination: sample CONT as rC + triangular(0, 0, 3 fM) (linear), monkeypatched in this
# scratch process only (src/ untouched). Same rng consumption as the log branch, so other draws are unchanged.
import sys, numpy as np
sys.argv = [sys.argv[0], "none"] + sys.argv[1:]
exec(open("runs.py").read())
import elisa_sim.params as EP
_orig = EP.ParameterSet.sample
def sample(self, n, rng, keys):
    log_ratio = float(self.extra.get("monte_carlo", {}).get("log_ratio_threshold", 3.0))
    ps = self.copy(); ps.n = n
    for k in self.sampleable(keys):
        p = self.params[k]
        if k == CONT and p.low != p.high:
            ps.values[k] = rng.triangular(p.low, p.value, p.high, size=n)
        else:
            ps.values[k] = EP.sample_param(p, n, rng, log_ratio)
    return ps
EP.ParameterSet.sample = sample
part = sys.argv[2]
if part == "a":
    run("C'0 baseline (lin patch, no-op check)", Cp, Cp_ps)
    for r in (1e-5, 1e-4, 3e-4, 1e-3, 1e-2, 8e-2):
        run(f"C'0 r{r} Cprev1000 LIN", Cp, Cp_ps, post=add_cont(r, 1000))
if part == "b":
    for r in (1e-5, 1e-4, 3e-4, 1e-3, 1e-2, 8e-2):
        run(f"C'0 r{r} Cprev100 LIN", Cp, Cp_ps, post=add_cont(r, 100))
if part == "c":
    for r in (1e-4, 3e-4):
        run(f"C'(x0.05) r{r} Cprev1000 LIN", Cp, Cp_ps, post=add_cont(r, 1000), f=0.05)
    run("C'0 L6+L7 r1e-4 Cprev1000 LIN", Cp, Cp_ps, scen=L67, post=add_cont(1e-4, 1000))
    run("C'0 bed2 r1e-4 Cprev1000 LIN", Cp, Cp_ps, post=lambda p: add_cont(1e-4, 1000)(bed(2)(p)))
    run("C'0 r3e-5 Cprev1000 LIN", Cp, Cp_ps, post=add_cont(3e-5, 1000))
