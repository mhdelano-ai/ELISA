import numpy as np
D=9e-10
def stub(L, A, Vend=0.0, t_fill=29.6*60, t1=38.25*60, t2=54.75*60, n=60):
    """dead-end channel, c=0 at RC mouth (sink), initial c=1; optional lumped end volume Vend (m^3).
    returns moles (in units c0*m^3) leaving into RC between t1 and t2 (after last electrolysis)."""
    dx=L/n; c=np.ones(n); cend=1.0
    dt=0.2*dx*dx/D; t=t_fill; out=0.0
    while t<t2:
        cl=np.concatenate([[0.0],c,[cend if Vend>0 else c[-1]]])
        flux_mouth=D*A*(c[0]-0)/(dx/2)  # into RC
        lap=(cl[2:]-2*cl[1:-1]+cl[:-2])/dx**2
        lap[0]=(cl[2]-c[0])/dx**2 - (c[0]-0)/(dx*dx/2)/1  # sink at half cell
        if Vend>0:
            fend=D*A*(c[-1]-cend)/dx
            cend+=fend*dt/Vend
        c=c+D*dt*lap
        if t1<=t<t2: out+=flux_mouth*dt
        t+=dt
    return out
mm=1e-3; uL=1e-9
VRC=1.04*uL
cases={
 "doc 3.5.1: 4 stubs 0.2 mm (0.5x0.2)": 4*stub(0.2*mm,0.5*mm*0.2*mm),
 "table: G3,G4 lanes 1.2 mm (0.5x0.2)": 2*stub(1.2*mm,0.5*mm*0.2*mm),
 "SF 4 mm (0.3x0.2) if V13 at tank end": stub(4*mm,0.3*mm*0.2*mm),
 "CE/RE neck 0.5 mm + pocket 0.024 uL": stub(0.5*mm,0.2*mm*0.2*mm,Vend=0.024*uL),
}
for k,v in cases.items(): print(f"{k:45s} returned after PE2 = {v/uL:.4f} uL-eq = {100*v/VRC:.2f} % of RC content")
