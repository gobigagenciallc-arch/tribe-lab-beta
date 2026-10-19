#!/usr/bin/env python3
"""Arma la beta pública de TRIBE LAB a partir de los originales del vault.
Uso: python3 build.py   (regenera index.html y tribebet/index.html)
Fuente de verdad: el vault. Esto solo copia + agrega la capa beta."""
import pathlib, re, sys
V = pathlib.Path.home()/"Documents/GoBig Vault/EFFORT/Proyectos/Tribe Club/02 Outputs"
LANDING = V/"(C) Landing Tribe Lab/index.html"
DEMO = V/"(C) TribeBet/(C) tribebet-demo.html"
OUT = pathlib.Path(__file__).parent

def rep(s, old, new, count=1):
    if s.count(old) < 1: sys.exit(f"no encontrado: {old[:70]!r}")
    return s.replace(old, new, count)

# ── 1. Landing TRIBE LAB · BETA ──
l = LANDING.read_text(encoding="utf-8")
l = rep(l, "<title>TRIBE LAB</title>", "")
beta_css = """<style>
#tl .tl-betabar{background:var(--gold);color:#140f02;font:800 11px/1.3 var(--display);letter-spacing:.06em;text-transform:uppercase;text-align:center;padding:8px 16px}
#tl .tl-betabar a{color:inherit;text-decoration:underline}
#tl .tl-tbb{background:linear-gradient(180deg,#0c0610,#170c1d 60%,#0c0610)}
#tl .tl-tbb-card{border:1px solid #3a2443;border-radius:14px;padding:clamp(20px,5vw,40px);background:#170c1d;max-width:760px}
#tl .tl-tbb-card ul{margin:16px 0 20px;padding-left:20px}
#tl .tl-tbb-card li{margin:6px 0}
#tl .tl-tbb-legal{margin-top:16px;font-size:13px;color:var(--mute,#b9a7c1)}
#tl .tl-tbb-sello{display:inline-block;border:1px solid var(--gold);color:var(--gold);border-radius:999px;padding:2px 10px;font-size:12px;margin-right:6px}
</style>
"""
l = rep(l, '<div id="tl" data-v="3">',
  beta_css + '<div id="tl" data-v="3-beta">\n  <div class="tl-betabar">Beta pública · <a href="#tl-tribebet">Prueba TribeBet</a> · créditos de juego sin valor · 18+</div>')
l = rep(l, '<a href="#tl-discord">Discord</a>', '<a href="#tl-discord">Discord</a>\n        <a href="#tl-tribebet">Beta</a>')
bloque = """    <section class="tl-sec tl-tbb" id="tl-tribebet" aria-labelledby="tl-tbb-h">
      <div class="tl-wrap">
        <div class="tl-tbb-card">
          <p class="tl-lab"><span class="tl-tbb-sello">BETA</span><span class="tl-tbb-sello">18+</span> Casino digital de la tribu</p>
          <h2 class="tl-h2" id="tl-tbb-h">Prueba la beta de TribeBet. <em>Gratis, con créditos de juego.</em></h2>
          <p>Estamos probando las mesas de TribeBet con la tribu antes de lanzarlo. Entra, juega y dinos qué te pareció.</p>
          <ul>
            <li><b>Pantera</b>: el juego insignia. Cruza la selva saltando entre tótems.</li>
            <li><b>Póker, blackjack y ruleta</b> con 1,000 créditos de práctica.</li>
          </ul>
          <a class="tl-cta tl-cta-gold" href="tribebet/">Entrar a la beta</a>
          <p class="tl-tbb-legal">Solo mayores de 18 años. Los créditos de la beta son de juego: no tienen valor monetario, no se compran, no se cambian por dinero y no dan premios. TribeBet hoy no recibe pagos.</p>
        </div>
      </div>
    </section>

"""
l = rep(l, '    <section class="tl-sec tl-game" id="tl-codigo"', bloque + '    <section class="tl-sec tl-game" id="tl-codigo"')
l = rep(l, '<a class="tl-link js-tb" href="https://ig.me/m/tribe.lab.ec" target="_blank" rel="noopener">Ver qué viene</a>',
           '<a class="tl-link" href="tribebet/">Probar la beta</a>')
head = """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#0c0610">
<meta name="robots" content="noindex, nofollow">
<title>TRIBE LAB · BETA</title>
<style>html,body{margin:0;padding:0;background:#0c0610}</style>
</head>
<body>
"""
(OUT/"index.html").write_text(head + l + "\n</body>\n</html>\n", encoding="utf-8")

# ── 2. TribeBet demo (sin Cajero ni Club: nada que parezca cobro) ──
d = DEMO.read_text(encoding="utf-8")
d = rep(d, "<title>Mesas TribeBet</title>", "<title>TribeBet · Beta</title>")
d = re.sub(r'\s*<button class="tab" id="tab-club"[^\n]*</button>', "", d)
d = re.sub(r'\s*<button class="tab" id="tab-cajero"[^\n]*</button>', "", d)
d = re.sub(r'\s*<button class="tb-btn tb-btn--compacto" id="btn-cajero"[^\n]*</button>', "", d)
d = rep(d, ",['tab-club','mesa-club'],['tab-cajero','mesa-cajero']]", "]")
d = rep(d, "$('btn-cajero').addEventListener('click',()=>{ abrirTab('tab-cajero'); $('tab-cajero').focus({preventScroll:true}); $('mesa-cajero').scrollIntoView({block:'start'}); });", "/* beta pública: sin Cajero ni Club */")
def quitar_mesa(d, id_):
    i = d.index(f'<div class="mesa" id="{id_}"'); depth = 0
    for m in re.finditer(r'<div\b|</div>', d[i:]):
        depth += 1 if m.group() == '<div' else -1
        if depth == 0: return d[:i] + d[i+m.end():]
d = quitar_mesa(d, "mesa-club")
i = d.index("/* ═══════════ CLUB (simulado) ═══════════ */"); j = d.index("/* ═══════════", i + 10)
d = d[:i] + "/* beta pública: Club quitado */\n" + d[j:]
i = d.index("/* ═══════════ CAJERO (sandbox)"); j = d.index("/* ═══════════ PANTERA", i)
d = d[:i] + "/* beta pública: Cajero quitado (TribeBet no recibe pagos) */\n" + d[j:]
d = quitar_mesa(d, "mesa-cajero")
d = d.replace("Carga créditos en el Cajero o baja el valor.", "Baja el valor o toca Reiniciar saldo.")
d = d.replace("pista: 'Recarga en el Cajero'", "pista: 'Toca Reiniciar saldo'")
d = d.replace("No te alcanzan los créditos. Recarga en el Cajero.", "No te alcanzan los créditos. Toca Reiniciar saldo.")
d = d.replace("<!-- ═══ CAJERO ═══ -->", "")
d = d.replace("Carga créditos en el Cajero.", "Toca Reiniciar saldo para volver a 1,000 créditos.")
d = re.sub(r'<footer class="pie">.*?</footer>', '''<footer class="pie">
  <p class="nota">TribeBet · Beta · Solo mayores de 18 años. Se juega con créditos de juego sin valor monetario: no se compran, no se cambian por dinero, no hay premios ni retiros. TribeBet hoy no recibe pagos.</p>
  <p class="nota nota--resp">Juega por entretenimiento y pon tu límite antes de empezar.</p>
  <p class="nota">El azar de las mesas sale del generador del navegador: sirve para una demo. Reglas simplificadas. <a href="../" style="color:#e8cf7a">← Volver a TRIBE LAB</a></p>
</footer>''', d, count=1, flags=re.S)
for x in ("tab-club", "tab-cajero", "btn-cajero", "USDT\"", "Cajero USDT"):
    if f'id="{x}"' in d: sys.exit(f"quedó {x}")
gate = """<style>
.beta-bar{position:sticky;top:0;z-index:50;background:#e8cf7a;color:#1a1202;font:700 12px/1.35 "JetBrains Mono",ui-monospace,monospace;text-align:center;padding:8px 12px}
.beta-bar a{color:inherit}
#mesa-club,#mesa-cajero{display:none!important}
.gate{position:fixed;inset:0;z-index:100;background:rgba(8,4,11,.96);display:flex;align-items:center;justify-content:center;padding:16px}
.gate-card{max-width:440px;width:100%;background:#170c1d;border:1px solid #3a2443;border-radius:14px;padding:24px;color:#f4ecf7;font:400 15px/1.6 "JetBrains Mono",ui-monospace,monospace}
.gate-card h2{font:900 22px/1.2 "Unbounded","Arial Black",sans-serif;margin:0 0 12px}
.gate-card ul{margin:12px 0 18px;padding-left:18px}
.gate-btns{display:flex;flex-direction:column;gap:10px}
.gate-btns button,.gate-btns a{min-height:48px;border-radius:999px;font:800 14px/1 "Unbounded","Arial Black",sans-serif;display:flex;align-items:center;justify-content:center;text-decoration:none;border:0}
.gate-si{background:#e8cf7a;color:#1a1202}
.gate-no{background:transparent;color:#f4ecf7;border:1px solid #7d6789!important}
</style>
<div class="beta-bar" role="note">BETA · Créditos de juego sin valor monetario · Sin premios · Sin pagos · Solo 18+ · <a href="../">← TRIBE LAB</a></div>
<div class="gate" id="gate" role="dialog" aria-modal="true" aria-labelledby="gate-h">
  <div class="gate-card">
    <h2 id="gate-h">¿Tienes 18 años o más?</h2>
    <p>TribeBet es una beta de juegos de casino para mayores de edad. Antes de entrar:</p>
    <ul>
      <li>Se juega con <b>créditos de juego sin valor monetario</b>.</li>
      <li>No se compran créditos, no hay premios y no se retira nada.</li>
      <li>Es una versión de prueba: puede cambiar o fallar.</li>
    </ul>
    <div class="gate-btns">
      <button class="gate-si" id="gate-si" type="button">Sí, tengo 18 o más</button>
      <a class="gate-no" href="../">No, volver a TRIBE LAB</a>
    </div>
  </div>
</div>
<script>
(function(){
  var g=document.getElementById('gate'), ok=false;
  try{ ok=sessionStorage.getItem('tribebet-18')==='si'; }catch(e){}
  if(ok){ g.remove(); return; }
  document.documentElement.style.overflow='hidden';
  document.getElementById('gate-si').addEventListener('click',function(){
    try{ sessionStorage.setItem('tribebet-18','si'); }catch(e){}
    document.documentElement.style.overflow=''; g.remove();
  });
  document.getElementById('gate-si').focus();
})();
</script>
"""
d = rep(d, "<body>\n", "<body>\n" + gate)
(OUT/"tribebet").mkdir(exist_ok=True)
(OUT/"tribebet/index.html").write_text(d, encoding="utf-8")
print("ok", len(l), len(d))
