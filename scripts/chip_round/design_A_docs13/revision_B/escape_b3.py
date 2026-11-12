exec(open("escape_b.py").read().split("V_cell = ")[0])
V_cell = 1.34 * uL; h = 0.175 * mm
for D in (9e-10, 7e-10):
    kw = dict(D=D, t_fill=26.65 * 60, t1=34.10 * 60, t2=52.75 * 60)
    c = {"G3 stub 0.5 mm (0.5 wide)": stub(0.5 * mm, 0.5 * mm * h, **kw),
         "G4 stub 0.5 mm (0.5 wide)": stub(0.5 * mm, 0.5 * mm * h, **kw),
         "V14 stub 0.5 mm (0.3 wide) behind WE2": stub(0.5 * mm, 0.3 * mm * h, **kw),
         "neck 0.15 mm (0.4x0.2) + pocket 0.4x0.4x0.2 (0.032) + V15 stub 0.3 mm (0.016 uL)":
             stub(0.15 * mm, 0.4 * mm * 0.2 * mm, Vend=0.048 * uL, **kw)}
    print(f"D = {D:.0e}"); tot = 0
    for k, v in c.items(): tot += v; print(f"  {k:78s} {100*v/V_cell:5.2f} %")
    print(f"  TOTAL {100*tot/V_cell:.2f} %")
    old = stub(0.5 * mm, 0.2 * mm * 0.2 * mm, Vend=0.074 * uL, **kw)
    print(f"  (docs/13-type slow pocket: neck 0.5 mm 0.2x0.2, 0.074 uL: {100*old/V_cell:.2f} %)")
    s1 = sum(stub(1.0 * mm, a * mm * h, **kw) for a in (0.5, 0.5, 0.3)) + list(c.values())[-1]
    print(f"  sensitivity: stubs 1.0 mm: {100*s1/V_cell:.2f} %")
# neck exchange rate and R_u
k = 9e-10 * 0.4e-3 * 0.2e-3 / (0.15e-3 * 0.048e-9)
print(f"pocket exchange rate D*A/(L*V) = {k:.4f} 1/s (time constant {1/k:.0f} s)")
for kap in (0.15, 0.6, 1.6):
    print(f"kappa {kap} S/m: neck R = {0.15e-3/(kap*0.4e-3*0.2e-3)/1e3:.1f} kOhm")
