import numpy as np
mu0=4e-7*np.pi
def Bblock(x,y,z,a,b,c,Br):
    # block magnet centred at origin, half-sizes a,b,c, magnetised +z, surface charge on z=+-c; numeric integration
    n=60
    xs=np.linspace(-a,a,n); ys=np.linspace(-b,b,n); dA=(2*a/n)*(2*b/n)
    X,Y=np.meshgrid(xs,ys)
    B=np.zeros(3)
    for zc,s in ((c,1),(-c,-1)):
        rx=x-X; ry=y-Y; rz=z-zc; r3=(rx**2+ry**2+rz**2)**1.5
        B+= s*Br/(4*np.pi)*np.array([np.sum(rx/r3),np.sum(ry/r3),np.sum(rz/r3)])*dA
    return B
def report(name,a,b,c,Br,pts):
    for (x,z) in pts:
        h=2e-5
        Bm=lambda xx,zz: np.linalg.norm(Bblock(xx,0,zz,a,b,c,Br))
        B=Bm(x,z); gx=(Bm(x+h,z)-Bm(x-h,z))/(2*h); gz=(Bm(x,z+h)-Bm(x,z-h))/(2*h)
        print(f"{name} x={x*1e3:.2f}mm z_above_face={(z-c)*1e3:.2f}mm |B|={B:.3f}T d|B|/dx={gx:.0f}T/m d|B|/dz={gz:.0f}T/m")
Br=1.3
# drag magnet 2x2x4 mm (half 1,1,2 mm); bead plane 0.3 mm above face (0.14 foil + 0.16 air gap)
c=2e-3; report("drag2x2x4",1e-3,1e-3,c,Br,[(0,c+3e-4),(0.8e-3,c+3e-4),(1.0e-3,c+3e-4),(1.3e-3,c+3e-4),(1.0e-3,c+0.5e-3)])
# collection magnet 10x10x5 (half 5,5,2.5)
c=2.5e-3; report("coll10x10x5",5e-3,5e-3,c,Br,[(0,c+3e-4),(0,c+2e-3),(0,c+3.7e-3),(4e-3,c+3.7e-3),(5e-3,c+3e-4),(6e-3,c+2e-3)])
