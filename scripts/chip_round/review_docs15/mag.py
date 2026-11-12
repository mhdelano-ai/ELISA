import numpy as np
Br=1.3
def B(pt, a, b, c, N=300):
    # block |x|<a/2,|y|<b/2, -c<z<0, magnetised +z; top face z=0 (+), bottom z=-c (-)
    xs=(np.arange(N)+0.5)/N*a-a/2; ys=(np.arange(N)+0.5)/N*b-b/2
    X,Y=np.meshgrid(xs,ys); dA=(a/N)*(b/N)
    out=np.zeros(3)
    for zf,s in ((0,1),(-c,-1)):
        R=np.stack([pt[0]-X,pt[1]-Y,np.full_like(X,pt[2]-zf)])
        r3=np.sum(R**2,0)**1.5
        out+=s*np.sum(R/r3,axis=(1,2))*dA
    return Br/(4*np.pi)*out
def grad(pt,a,b,c,h=2e-5):
    g=[]
    for i in range(3):
        d=np.zeros(3);d[i]=h
        g.append((np.linalg.norm(B(pt+d,a,b,c))-np.linalg.norm(B(pt-d,a,b,c)))/(2*h))
    return np.array(g)
m=1.15e-13; f=2.35e-8
def rep(lbl,pt,a,b,c):
    Bv=B(np.array(pt),a,b,c); g=grad(np.array(pt),a,b,c)
    print(f"{lbl:45s} |B|={np.linalg.norm(Bv):.3f} T grad(x,y,z)=({g[0]:.0f},{g[1]:.0f},{g[2]:.0f}) T/m  Flat={m*abs(g[0])*1e12:.1f} pN Fz={m*abs(g[2])*1e12:.1f} pN")
mm=1e-3
Mc=(10*mm,10*mm,5*mm); Md=(2*mm,2*mm,4*mm)
rep("Mc centre z=3.7",(0,0,3.7*mm),*Mc)
rep("Mc x=4 z=3.7",(4*mm,0,3.7*mm),*Mc)
for x in (0,2,3,4,4.5,4.9,5.0,5.2,5.5,6):
    rep(f"Mc floor z=0.3 x={x}",(x*mm,0,0.3*mm),*Mc)
for z in (5.3,8.8):
    rep(f"Mc lowered: centre z={z}",(0,0,z*mm),*Mc)
    rep(f"Mc lowered: x=5 z={z}",(5*mm,0,z*mm),*Mc)
for x in (0.6,0.8,0.9,1.0,1.1,1.2,1.5,2.0):
    rep(f"Md z=0.3 x={x}",(x*mm,0,0.3*mm),*Md)
for x in (0.9,1.0,1.1,1.3):
    rep(f"Md z=0.5 x={x}",(x*mm,0,0.5*mm),*Md)
