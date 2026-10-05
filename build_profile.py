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
<title>{escape(title)}</title><style>text{{font-family:Consolas,'Liberation Mono',monospace}}.dots{{fill:{TEAL}}}@media(prefers-reduced-motion:reduce){{.moving{{display:none}}.still{{display:inline!important}}}}</style>
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
b = rect(1,1,998,438,BG,18)
b += '<path d="M20 1H980" stroke="#62daca" stroke-opacity=".6"/>'
b += ''.join(f'<circle cx="{x}" cy="27" r="4" fill="{c}"/>' for x,c in [(26,'#ee8796'),(42,'#e9c384'),(58,TEAL)])
b += txt(81,31,'wendoski07 / profile.yml',11,MUTED)
b += txt(968,31,'BACKEND  /  APIs  /  DATA',11,TEAL,'text-anchor="end"')
b += '<path d="M1 49H999" stroke="#293b50"/>'
b += rect(24,72,300,326)
b += txt(42,99,'VISUAL / W07',11,TEAL)
b += '<path d="M24 114H324" stroke="#293b50"/>'
b += '<g class="dots moving">'
for i,(a,c,d) in enumerate(zip(monogram,code,chart)):
    b += f'<circle cx="{a[0]}" cy="{a[1]}" r="1.65" opacity="{.6+(i%5)*.08}">'
    for attr,j in [('cx',0),('cy',1)]:
        values = ';'.join(str(p[j]) for p in [a,a,c,c,d,d,a])
        b += f'<animate attributeName="{attr}" values="{values}" keyTimes="0;.19;.31;.50;.62;.81;1" dur="16s" repeatCount="indefinite" calcMode="spline" keySplines=".4 0 .2 1;.4 0 .2 1;.4 0 .2 1;.4 0 .2 1;.4 0 .2 1;.4 0 .2 1"/>'
    b += '</circle>'
b += '</g><g class="dots still" style="display:none">'+''.join(f'<circle cx="{p[0]}" cy="{p[1]}" r="1.65"/>' for p in monogram)+'</g>'
b += txt(174,335,'IDENTITY → CODE → DATA',11,MUTED,'text-anchor="middle"')
b += txt(174,374,'APRENDER / CONSTRUIR / MEJORAR',9,MUTED,'text-anchor="middle"')
b += rect(343,72,633,326)
b += txt(365,111,'Oscar Ricaurte',30,TEXT,'font-weight="700"')
b += txt(367,137,'Backend Developer · APIs',17,TEAL)
b += '<path d="M365 155H954" stroke="#293b50"/>'
rows=[('profile:',None),('  handle:','WENDOSKI07'),('  focus:','Backend · APIs REST'),('  stack:','Node.js · Redis · SQL'),('  learning:','Ingeniería en Analítica de Datos')]
for i,(key,val) in enumerate(rows):
    y=187+i*31
    b += txt(367,y,str(i+1).zfill(2),11,'#526780')
    b += txt(401,y,key,15,BLUE)
    if val: b += txt(545,y,val,14,TEAL if i==4 else TEXT)
b += '<path d="M343 355H976" stroke="#293b50"/>'
b += rect(359,368,65,19,TEAL,3,TEAL)+txt(392,382,'NORMAL',10,BG,'text-anchor="middle" font-weight="700"')
b += txt(437,382,'profile.yml',11,TEXT)+txt(954,382,'UTF-8 / MAIN',10,MUTED,'text-anchor="end"')
b += txt(26,425,'OSCAR RICAURTE',10,MUTED)+txt(971,425,'BUILD WITH INTENT.',10,TEAL,'text-anchor="end"')
write('terminal.svg',1000,440,'Oscar Ricaurte. Backend y APIs. Aprendiendo analítica de datos. Animación de partículas W07, código y gráfico.',b)

for name,title,number,category,lines,tag in [
    ('messaging.svg','Mensajería & APIs','01','AXIONA / BACKEND',['WhatsApp, CRM y bots.','Servicios, campañas e integraciones.'],'NODE.JS · MARIADB · REDIS'),
    ('management.svg','Gestión & soporte','02','GIT COLOMBIA / DESARROLLO',['Aplicación para gestión de personal','y soporte técnico en equipo.'],'NODE.JS · REACT · GIT')]:
    b=rect(1,1,478,208,BG,14)
    b+=txt(22,31,number+' / '+category,10,TEAL,'letter-spacing="1"')
    b+=txt(22,77,title,25,TEXT,'font-weight="700"')
    b+=txt(22,112,lines[0],14,MUTED)+txt(22,134,lines[1],14,MUTED)
    b+='<path d="M22 158H458" stroke="#293b50"/>'
    b+=txt(22,187,tag,10,BLUE)
    write(name,480,210,title+'. '+ ' '.join(lines),b)

def icon(name, x, y):
    root=ET.fromstring((ASSETS/'icons'/f'{name}.svg').read_text(encoding='utf-8'))
    root.set('x',str(x)); root.set('y',str(y)); root.set('width','37'); root.set('height','37')
    return ET.tostring(root,encoding='unicode')

b=rect(1,1,998,410,BG,16)
b+=txt(26,34,'$ cat tech-stack.yml',15,TEAL)+txt(974,34,'TOOLS / TECHNOLOGIES',10,MUTED,'text-anchor="end"')
b+='<path d="M1 53H999" stroke="#293b50"/>'
groups=[(20,72,'BACKEND & APIs',[('nodejs','Node.js'),('javascript','JavaScript'),('java','Java')],'APIs REST · Integraciones · Debugging'),(510,72,'DATOS & CACHE',[('mariadb','MariaDB'),('postgresql','PostgreSQL'),('redis','Redis')],'SQL · Bases relacionales · Redis'),(20,234,'INFRAESTRUCTURA',[('docker','Docker'),('linux','Linux'),('git','Git')],'Contenedores · Despliegue · Versionado'),(510,234,'LENGUAJES & WEB',[('python','Python'),('react','React'),('nextjs','Next.js')],'Herramientas complementarias')]
for x,y,title,icons,caption in groups:
    b+=rect(x,y,470,148)
    b+=txt(x+17,y+26,title,12,TEAL,'letter-spacing="1"')
    for i,(name,label) in enumerate(icons):
        ix=x+17+i*145
        b+=rect(ix,y+41,42,42,'#c6d2df' if name=='mariadb' else '#182739',8,'#293b50')+icon(name,ix+2.5,y+43.5)
        b+=txt(ix+51,y+66,label,12,TEXT)
    b+=txt(x+17,y+124,caption,12,MUTED)
write('stack.svg',1000,412,'Tecnologías: Node.js, JavaScript, Java, MariaDB, PostgreSQL, Redis, Docker, Linux, Git, Python, React y Next.js.',b)
print('Generated profile SVG assets.')
