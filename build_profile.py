"""Generate original, dependency-free SVG assets for the GitHub profile."""
from pathlib import Path
from html import escape
import math
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / 'assets'
ASSETS.mkdir(exist_ok=True)
BG, PANEL, LINE, TEXT, MUTED, TEAL, BLUE = '#0b111b', '#101b2b', '#293b50', '#e7eff9', '#94a7bf', '#62daca', '#a6b9ee'

def txt(x, y, text, size=16, color=TEXT, extra=''):
    return f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" {extra}>{escape(text)}</text>'

def rect(x, y, w, h, fill=PANEL, radius=12, stroke=LINE):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}"/>'

def svg(w, h, title, body):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(title)}">
<title>{escape(title)}</title><style>text{{font-family:'Segoe UI',Arial,sans-serif}}.dots{{fill:{TEAL}}}@media(prefers-reduced-motion:reduce){{.moving{{display:none}}.still{{display:inline!important}}}}</style>
{body}</svg>'''

def write(name, w, h, title, body):
    (ASSETS / name).write_text(svg(w, h, title, body), encoding='utf-8')

def sample(lines, n=180):
    segments = [(a, b, math.dist(a, b)) for path in lines for a, b in zip(path, path[1:])]
    total = sum(s[2] for s in segments)
    result = []
    for i in range(n):
        distance = (i + .5) / n * total
        for a, b, length in segments:
            if distance <= length:
                t = distance / length
                result.append((round(a[0]+t*(b[0]-a[0]), 2), round(a[1]+t*(b[1]-a[1]), 2)))
                break
            distance -= length
    return result

# Original line shapes: W07 -> code brackets -> a data chart.
monogram = sample([[(80,185),(93,261),(114,211),(135,261),(148,185)],[(169,185),(205,185),(211,195),(211,251),(205,261),(169,261),(163,251),(163,195),(169,185)],[(232,185),(281,185),(249,261)]])
code = sample([[(125,176),(80,221),(125,266)],[(184,169),(156,273)],[(216,176),(261,221),(216,266)]])
chart = sample([[(80,175),(80,274),(278,274)],[(104,254),(104,228),(132,228),(132,254),(104,254)],[(157,254),(157,202),(185,202),(185,254),(157,254)],[(211,254),(211,168),(239,168),(239,254),(211,254)]])
b = rect(1,1,998,348,BG,20)
b += '<defs><radialGradient id="aura"><stop stop-color="#28525a" stop-opacity=".35"/><stop offset="1" stop-color="#0b111b" stop-opacity="0"/></radialGradient></defs>'
b += '<ellipse cx="825" cy="166" rx="174" ry="160" fill="url(#aura)"/>'
b += txt(48,49,'OSCAR RICAURTE',12,TEAL,'letter-spacing="3" font-weight="600"')
b += txt(45,119,'Backend Developer',53,TEXT,'font-weight="650" letter-spacing="-1.6"')
b += txt(48,158,'APIs e integraciones',25,TEAL)
b += txt(48,206,'Desarrollo servicios que conectan',20,MUTED)
b += txt(48,234,'aplicaciones, procesos y datos.',20,MUTED)
b += '<path d="M48 266H600" stroke="#293b50"/>'
b += txt(48,300,'Node.js  ·  SQL  ·  Redis  ·  Docker',17,TEXT)
b += txt(48,326,'En formación: Ingeniería en Analítica de Datos',14,MUTED)
b += '<g transform="translate(640,-35)">'
b += '<g class="dots moving">'
for i,(a,c,d) in enumerate(zip(monogram,code,chart)):
    b += f'<circle cx="{a[0]}" cy="{a[1]}" r="1.65" opacity="{.6+(i%5)*.08}">'
    for attr,j in [('cx',0),('cy',1)]:
        values = ';'.join(str(p[j]) for p in [a,a,c,c,d,d,a])
        b += f'<animate attributeName="{attr}" values="{values}" keyTimes="0;.19;.31;.50;.62;.81;1" dur="16s" repeatCount="indefinite" calcMode="spline" keySplines=".4 0 .2 1;.4 0 .2 1;.4 0 .2 1;.4 0 .2 1;.4 0 .2 1;.4 0 .2 1"/>'
    b += '</circle>'
b += '</g><g class="dots still" style="display:none">'+''.join(f'<circle cx="{p[0]}" cy="{p[1]}" r="1.65"/>' for p in monogram)+'</g>'
b += '</g>'
b += txt(817,269,'WENDOSKI07',12,MUTED,'text-anchor="middle" letter-spacing="2"')
write('terminal.svg',1000,350,'Oscar Ricaurte. Backend Developer. APIs e integraciones. Node.js, SQL, Redis y Docker. En formación en Ingeniería en Analítica de Datos.',b)

for name,title,number,category,lines,tag in [
    ('messaging.svg','Mensajería & APIs','01','AXIONA / BACKEND',['WhatsApp, CRM y bots.','Servicios, campañas e integraciones.'],'NODE.JS · MARIADB · REDIS'),
    ('management.svg','Gestión & soporte','02','GIT COLOMBIA / DESARROLLO',['Aplicación para gestión de personal','y soporte técnico en equipo.'],'NODE.JS · REACT · GIT')]:
    b=rect(1,1,478,208,BG,14)
    b+=txt(22,31,category.replace(' / ', ' · '),12,TEAL,'letter-spacing="1"')
    b+=txt(22,77,title,28,TEXT,'font-weight="700"')
    b+=txt(22,112,lines[0],17,MUTED)+txt(22,134,lines[1],17,MUTED)
    b+='<path d="M22 158H458" stroke="#293b50"/>'
    b+=txt(22,187,tag,12,BLUE)
    write(name,480,210,title+'. '+ ' '.join(lines),b)

def icon(name, x, y):
    root=ET.fromstring((ASSETS/'icons'/f'{name}.svg').read_text(encoding='utf-8'))
    root.set('x',str(x)); root.set('y',str(y)); root.set('width','37'); root.set('height','37')
    return ET.tostring(root,encoding='unicode')

b=rect(1,1,998,410,BG,16)
b+=txt(26,34,'Tecnologías con las que trabajo',21,TEXT)+txt(974,34,'STACK',11,MUTED,'text-anchor="end"')
b+='<path d="M1 53H999" stroke="#293b50"/>'
groups=[(20,72,'BACKEND Y APIs',[('nodejs','Node.js'),('javascript','JavaScript'),('java','Java')],'APIs REST · Integraciones · Debugging'),(510,72,'DATOS Y CACHÉ',[('mariadb','MariaDB'),('postgresql','PostgreSQL'),('redis','Redis')],'SQL · Bases relacionales · Redis'),(20,234,'INFRAESTRUCTURA',[('docker','Docker'),('linux','Linux'),('git','Git')],'Contenedores · Despliegue · Versionado'),(510,234,'LENGUAJES Y WEB',[('python','Python'),('react','React'),('nextjs','Next.js')],'Herramientas complementarias')]
for x,y,title,icons,caption in groups:
    b+=rect(x,y,470,148)
    b+=txt(x+17,y+26,title,14,TEAL,'letter-spacing="1"')
    for i,(name,label) in enumerate(icons):
        ix=x+17+i*145
        b+=rect(ix,y+41,42,42,'#c6d2df' if name=='mariadb' else '#182739',8,'#293b50')+icon(name,ix+2.5,y+43.5)
        b+=txt(ix+51,y+66,label,15,TEXT)
    b+=txt(x+17,y+124,caption,14,MUTED)
write('stack.svg',1000,412,'Tecnologías: Node.js, JavaScript, Java, MariaDB, PostgreSQL, Redis, Docker, Linux, Git, Python, React y Next.js.',b)
print('Generated profile SVG assets.')
