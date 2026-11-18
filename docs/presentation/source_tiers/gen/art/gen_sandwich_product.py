import math, json, os
ART = os.path.dirname(os.path.abspath(__file__))
INK="#14213D"; CARD="#FFFDF8"; SAND="#ECE7DB"; STEEL="#9AA5B8"; SLATE="#5E6B85"; BLUE="#1F5A96"
ORANGE="#D9773F"; RUST="#A8481A"; TEAL="#2F8072"; GOLD="#C9A227"
J='stroke-linejoin="round" stroke-linecap="round"'
def f(v): return ("%.1f" % v).rstrip('0').rstrip('.')
def pts(p): return " ".join(f(x)+","+f(y) for x,y in p)
def markers():
    s='<defs>'
    for mid,col,sz in (("ai",INK,13),("at",TEAL,15),("ai4",INK,15),("as",SLATE,10)):
        s+=f'<marker id="{mid}" viewBox="0 0 12 12" refX="6" refY="6" markerWidth="{sz}" markerHeight="{sz}" markerUnits="userSpaceOnUse" orient="auto"><path d="M0,0 L12,6 L0,12 Z" fill="{col}"/></marker>'
    return s+'</defs>'
def fatline(path, w, fill):
    return (f'<path d="{path}" fill="none" stroke="{INK}" stroke-width="{w+6}" {J}/>'
            f'<path d="{path}" fill="none" stroke="{fill}" stroke-width="{w}" {J}/>')
def rot(px,py,cx,cy,a):
    r=math.radians(a); x,y=px-cx,py-cy
    return cx+x*math.cos(r)-y*math.sin(r), cy+x*math.sin(r)+y*math.cos(r)
def vpath(vx,vy,ang,length,spread):
    # local: vertex at origin, arms pointing down (+y), spread +-spread deg; rotated by ang
    out=[]
    for s in (-spread,spread):
        lx=length*math.sin(math.radians(s)); ly=length*math.cos(math.radians(s))
        out.append(rot(vx+lx,vy+ly,vx,vy,ang))
    a,b=out
    return f"M{f(a[0])},{f(a[1])} L{f(vx)},{f(vy)} L{f(b[0])},{f(b[1])}"
def conjugate(vx,vy,ang):
    bx,by=rot(vx,vy-36,vx,vy,ang)
    s=f'<rect x="{f(bx-32)}" y="{f(by-25)}" width="64" height="50" rx="23" ry="22" fill="{RUST}" stroke="{INK}" stroke-width="3" {J} transform="rotate({f(ang)} {f(bx)} {f(by)})"/>'
    s+=fatline(vpath(vx,vy,ang,40,32),12,ORANGE)
    return s, (bx,by)
def hexa(cx,cy,r,fill,stroke,sw):
    p=[(cx+r*math.cos(math.radians(-90+60*k)),cy+r*math.sin(math.radians(-90+60*k))) for k in range(6)]
    return f'<polygon points="{pts(p)}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {J}/>'
def lead(x1,y1,x2,y2):
    return f'<line x1="{f(x1)}" y1="{f(y1)}" x2="{f(x2)}" y2="{f(y2)}" stroke="{SLATE}" stroke-width="2" {J}/>'
def write(name,W,H,aria,body,labels):
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{aria}">'+markers()+body+'</svg>'
    open(os.path.join(ART,name+".svg"),"w").write(svg)
    json.dump(labels,open(os.path.join(ART,name+".labels.json"),"w"),indent=1)
def L(key,text,x,y,w,align="left",size=24,weight=400):
    return dict(key=key,text=text,x=x,y=y,w=w,align=align,size=size,weight=weight)

# ---------------- sandwich ----------------
b=''
# leaders first (under artwork)
b+=lead(163,248,286,388)          # capture -> unit 1 right arm
b+=lead(345,276,320,52)           # IgG -> left arm tip
b+=lead(470,184,470,80)           # conjugate -> enzyme
b+=lead(582,125,604,124)          # substrate
b+=lead(592,312,604,312)          # product
b+=lead(162,440,180,440)          # blank
b+=f'<rect x="180" y="470" width="420" height="50" fill="{SAND}" stroke="{INK}" stroke-width="3" {J}/>'
b+=f'<rect x="180" y="458" width="420" height="12" fill="{GOLD}" stroke="{INK}" stroke-width="3" {J}/>'
# IgG stem + arms (middle unit), drawn before capture V so the V grips it
igg="M390,404 L390,346 M390,346 L345.7,289.3 M390,346 L434.3,289.3"
b+=fatline(igg,14,BLUE)
for x in (270,390,510):
    b+=fatline(vpath(x,432,180,46,30),12,SLATE)
    b+=f'<rect x="{x-13}" y="432" width="26" height="26" rx="6" fill="{STEEL}" stroke="{INK}" stroke-width="3" {J}/>'
# redraw IgG stem top part over V so it reads as sitting inside
b+=fatline("M390,398 L390,346",14,BLUE)
# conjugate on right arm tip
d=(math.sin(math.radians(38)),-math.cos(math.radians(38)))
tip=(434.3,289.3); vx,vy=tip[0]+24*d[0],tip[1]+24*d[1]
c,_=conjugate(vx,vy,38); b+=c
# stuck conjugate, upside down, tilted
c,_=conjugate(210.1,388.6,170); b+=c
# substrate
sx,sy=560,125
b+=f'<line x1="{sx}" y1="{sy-20}" x2="{sx}" y2="{sy-28}" stroke="{INK}" stroke-width="2"/>'
b+=f'<line x1="{sx}" y1="{sy+20}" x2="{sx}" y2="{sy+28}" stroke="{INK}" stroke-width="2"/>'
b+=hexa(sx,sy,20,CARD,TEAL,3)
b+=f'<circle cx="{sx}" cy="{sy-30}" r="8" fill="{ORANGE}" stroke="{INK}" stroke-width="2"/>'
b+=f'<circle cx="{sx}" cy="{sy+30}" r="8" fill="{ORANGE}" stroke="{INK}" stroke-width="2"/>'
# curved arrow substrate -> product passing the enzyme
b+=f'<path d="M541,160 C508,190 510,255 547,292" fill="none" stroke="{INK}" stroke-width="3" {J} marker-end="url(#ai)"/>'
px,py=570,312
b+=hexa(px,py,20,TEAL,INK,2)
b+=f'<line x1="{px}" y1="{py+26}" x2="{px}" y2="{424}" stroke="{TEAL}" stroke-width="4" {J} marker-end="url(#at)"/>'
for ex in (553,587):
    b+=f'<line x1="{ex}" y1="438" x2="{ex}" y2="456" stroke="{INK}" stroke-width="3" {J} marker-end="url(#ai)"/>'
labs=[L("capture","capture antibody fragment on streptavidin",5,138,150,"right"),
      L("igg","human IgG: the analyte",30,12,300,"left"),
      L("conjugate","detection antibody carrying the enzyme (the conjugate)",380,10,375,"left"),
      L("substrate","substrate",612,108,140,"left"),
      L("product","product, oxidised at the electrode",612,252,145,"left"),
      L("blank","conjugate stuck to the surface without analyte: this is the blank",5,330,150,"right")]
write("sandwich",760,560,"Sandwich immunoassay cartoon: capture fragments on streptavidin stand on a gold surface, the middle one holds a human IgG that carries an enzyme-labelled detection fragment, the enzyme turns substrate into a product that is oxidised at the gold, and one conjugate stuck on the surface without analyte makes the blank.",b,labs)

# ---------------- product ----------------
b=''
def ring(cx,cy):
    return hexa(cx,cy,46,CARD,INK,3)+f'<circle cx="{cx}" cy="{cy}" r="26" fill="none" stroke="{INK}" stroke-width="2"/>'
def group(cx,cy,top,kind):
    s=''
    if top:
        s+=f'<line x1="{cx}" y1="{cy-46}" x2="{cx}" y2="{cy-70}" stroke="{INK}" stroke-width="3" {J}/>'
        r=18 if kind=="P" else 10; col=ORANGE if kind=="P" else TEAL
        s+=f'<circle cx="{cx}" cy="{cy-70-r}" r="{r}" fill="{col}" stroke="{INK}" stroke-width="3"/>'
    else:
        s+=f'<line x1="{cx}" y1="{cy+46}" x2="{cx}" y2="{cy+70}" stroke="{INK}" stroke-width="3" {J}/>'
        r=18 if kind=="P" else 10; col=ORANGE if kind=="P" else TEAL
        s+=f'<circle cx="{cx}" cy="{cy+70+r}" r="{r}" fill="{col}" stroke="{INK}" stroke-width="3"/>'
    return s
for cx,t,bt in ((230,"P","P"),(760,"P","H"),(1290,"H","H")):
    b+=group(cx,150,True,t)+group(cx,150,False,bt)+ring(cx,150)
for x1,x2,dash in ((340,650,""),(870,1180,' stroke-dasharray="14 12"')):
    m=(x1+x2)/2
    b+=f'<line x1="{x1}" y1="150" x2="{x2-6}" y2="150" stroke="{INK}" stroke-width="4"{dash} stroke-linecap="butt" marker-end="url(#ai4)"/>'
    b+=f'<rect x="{m-48}" y="68" width="96" height="56" rx="26" ry="24" fill="{RUST}" stroke="{INK}" stroke-width="3" {J}/>'
    b+=f'<path d="M{m-22},153 Q{m-20},203 {m+2},206" fill="none" stroke="{INK}" stroke-width="3" {J} marker-end="url(#ai)"/>'
    b+=f'<circle cx="{m+24}" cy="207" r="14" fill="{ORANGE}" stroke="{INK}" stroke-width="3"/>'
b+=f'<line x1="1350" y1="150" x2="1470" y2="150" stroke="{INK}" stroke-width="4" stroke-linecap="butt" marker-end="url(#ai4)"/>'
b+=f'<rect x="1483" y="65" width="34" height="170" fill="{GOLD}" stroke="{INK}" stroke-width="3" {J}/>'
for ey in (118,182):
    b+=f'<line x1="1489" y1="{ey}" x2="1502" y2="{ey}" stroke="{INK}" stroke-width="3" stroke-linecap="butt" marker-end="url(#ai)"/>'
labs=[L("substrate","hydroquinone diphosphate, the substrate",80,268,300,"center"),
      L("mono","monophosphate: what the enzyme makes first",560,268,400,"center"),
      L("hq","hydroquinone",1180,268,220,"center"),
      L("fast","one phosphate off per turnover",295,14,400,"center"),
      L("slow","the second phosphate comes off slowly",795,14,460,"center"),
      L("electrode","2 electrons at the electrode",1404,244,192,"center")]
write("product",1600,330,"Reaction scheme: the enzyme removes one phosphate from hydroquinone diphosphate quickly, the second phosphate slowly, and the hydroquinone formed gives two electrons to a gold electrode.",b,labs)
