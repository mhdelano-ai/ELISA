import sys
sys.argv = [sys.argv[0], "none"]
exec(open("runs.py").read())
run("C' x0.1", Cp, Cp_ps, f=0.1)
run("C' S4a x0.1", Cp, Cp_ps, scen=S4a, f=0.1)
run("B S4a x0.1", B, B_ps, scen=S4a, f=0.1, scale=BS)
run("C' blankCV0.14 x0.05", Cp, Cp_ps, post=bcv, f=0.05)
