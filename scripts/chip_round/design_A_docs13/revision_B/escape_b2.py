exec(open("escape_b.py").read().split("V_cell = ")[0])
V_cell = 1.34 * uL; h = 0.175 * mm
F45 = 1 - 0.811 * np.exp(-45 / 18.0)    # PE0 45-s step, tau 18 s (docs/13 s3.5.2 series, first term)
print(f"PE0 removal F(45 s) = {F45:.3f}; residual in the electrolysed RC liquid {1-F45:.3f}")
for D in (9e-10, 7e-10):
    tau = 4 * (2e-4) ** 2 / (np.pi ** 2 * D); res = 0.811 * np.exp(-45 / tau)
    kw = dict(D=D, t_fill=26.65 * 60)
    c = {"G3 stub 0.5 mm (conservative c=1; holds drag A1)": stub(0.5 * mm, 0.5 * mm * h, **kw),
         "G4 stub 0.5 mm (fresh flush)": stub(0.5 * mm, 0.5 * mm * h, **kw),
         "V13 feed stub 0.5 mm (0.3 wide, fresh)": stub(0.5 * mm, 0.3 * mm * h, **kw),
         "V14 stub 0.5 mm behind WE2 (conservative c=1)": stub(0.5 * mm, 0.3 * mm * h, **kw),
         f"CE/RE neck+pocket+V15 stub, refreshed with PE0 liquid (c={res:.3f})":
             res * stub(0.3 * mm, 0.2 * mm * 0.2 * mm, Vend=0.074 * uL, D=D, t_fill=27.8 * 60)}
    tot = sum(c.values())
    print(f"D = {D:.0e}")
    for k, v in c.items(): print(f"  {k:70s} {100*v/V_cell:5.2f} %")
    print(f"  TOTAL {100*tot/V_cell:.2f} %   (without the pocket refresh the pocket alone gives ~3.3 %)")
    s1 = sum(stub(1.0 * mm, a * mm * h, **kw) for a in (0.5, 0.5, 0.3, 0.3)) + list(c.values())[-1]
    print(f"  sensitivity: all four stubs 1.0 mm instead of 0.5 mm: {100*s1/V_cell:.2f} %")
