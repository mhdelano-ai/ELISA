exec(open("mag_b.py").read().split("print(\"== (1)")[0])
for d in (16, 18, 20, 22, 24):
    for z in (0.30, 3.2):
        pt=(d*mm,0,z*mm); g=grad(pt,Mc); print(f"M_c up, lateral {d} mm, z {z}: F {m*np.linalg.norm(g)*1e12:.3f} pN (x {m*g[0]*1e12:.3f}, z {m*g[2]*1e12:.3f})")
for d in (2.0,3.0):
    pt=(0,0,(0.30+d)*mm); g=grad(pt,Md); print(f"M_d raised under floor, bead at height {d} mm above floor: F {m*np.linalg.norm(g)*1e12:.2f} pN")
