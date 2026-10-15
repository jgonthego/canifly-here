import json,os,html
D=json.load(open('data/states.json'));R=D['reviewed'];BASE=os.environ.get('BASE','https://jgonthego.github.io/canifly-here')
S="Alabama Alaska Arizona Arkansas California Colorado Connecticut Delaware District_of_Columbia Florida Georgia Hawaii Idaho Illinois Indiana Iowa Kansas Kentucky Louisiana Maine Maryland Massachusetts Michigan Minnesota Mississippi Missouri Montana Nebraska Nevada New_Hampshire New_Jersey New_Mexico New_York North_Carolina North_Dakota Ohio Oklahoma Oregon Pennsylvania Rhode_Island South_Carolina South_Dakota Tennessee Texas Utah Vermont Virginia Washington West_Virginia Wisconsin Wyoming".split()
NAME="Can I Fly Here?"
# Newsletter flag: set FORM_ID (Formspree form ID) to show the alerts signup form; off until a real ID exists.
FORM_ID=os.environ.get("FORM_ID","").strip();FORM=f"https://formspree.io/f/{FORM_ID}";SHOW_FORM=bool(FORM_ID) and FORM_ID!="YOUR_FORM_ID"
NF=len(D["focus"])
FAQ=[("Do I need a license to fly a drone recreationally?","Recreational flyers must pass the free FAA TRUST test and follow FAA recreational rules; commercial work requires an FAA Part 107 Remote Pilot Certificate."),
("How high can I fly?","Generally no higher than 400 feet above ground level in uncontrolled airspace; controlled airspace requires authorization, e.g. via LAANC."),
("Does my drone need Remote ID?","Drones required to be registered must broadcast Remote ID (built-in or a module) unless flown at an FAA-Recognized Identification Area."),
("Do drones need to be registered?","Drones over 250 g (and all Part 107 drones) must be registered with the FAA via FAADroneZone.")]
FS=[("FAA Recreational flyers & TRUST","https://www.faa.gov/uas/recreational_flyers"),("FAA Part 107","https://www.faa.gov/uas/commercial_operators"),("FAA Remote ID","https://www.faa.gov/uas/getting_started/remote_id"),("FAA LAANC","https://www.faa.gov/uas/getting_started/laanc"),("FAA B4UFLY","https://www.faa.gov/uas/getting_started/b4ufly"),("NCSL state UAS law landscape","https://www.ncsl.org/transportation/current-unmanned-aircraft-state-law-landscape")]
e=html.escape
def page(t,d,path,body,faq=False):
  ld='' if not faq else '<script type="application/ld+json">'+json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in FAQ]})+'</script>'
  return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(t)}</title><meta name="description" content="{e(d)}"><link rel="canonical" href="{BASE}{path}"><meta property="og:title" content="{e(t)}"><meta property="og:description" content="{e(d)}"><meta property="og:type" content="website"><meta property="og:url" content="{BASE}{path}"><link rel="stylesheet" href="{BASE}/style.css">{ld}</head><body><header><a href="{BASE}/"><b>✈ {NAME}</b></a> drone laws by state</header><main>{body}
<section class="box">{('<h2>Rule change alerts</h2><form action="'+FORM+'" method="POST"><input type="email" name="email" placeholder="you@example.com" required><input type="hidden" name="list" value="alerts"><button>Subscribe</button></form>') if SHOW_FORM else '<!-- NEWSLETTER HOOK: set FORM_ID env var to enable the alerts form -->'}<p>Spotted a rule change or error? <a href="mailto:d.bot@mail.grokbot.com?subject=Rule%20change%20report">Report it</a>.</p></section>
<p class="ad"><!-- AFFILIATE SLOT: Part 107 course (add real link here) --><!-- AFFILIATE SLOT: drone gear (add real link here) --><a href="mailto:d.bot@mail.grokbot.com?subject=Sponsorship">Advertise / sponsor this page</a></p>
</main><footer><p><b>Disclaimer:</b> Informational only, not legal advice. Laws change; verify with the FAA, state statutes and local authorities before flying. Last reviewed {R}.</p><p>Can I Fly Here?</p></footer></body></html>'''
def faa():
  return '<h2>FAA baseline (all states)</h2><ul>'+''.join(f'<li><b>{e(q)}</b> {e(a)}</li>' for q,a in FAQ)+'<li>Keep the drone within visual line of sight; don\'t fly over people or moving vehicles except as Part 107 allows; respect TFRs (stadiums, VIP movement, wildfires).</li></ul>'
os.makedirs('docs/states',exist_ok=True);urls=['/'];items=[]
for s in S:
  n=s.replace('_',' ');slug=n.lower().replace(' ','-');f=D['focus'].get(slug)
  b=f'<h1>Drone laws in {n}</h1><p class="rev">Last reviewed {R}</p>'+faa()
  src=list(FS)
  if f:
    L=lambda xs:'<ul>'+''.join(f'<li>{e(t)} <a href="{u}">[source]</a></li>' for t,u in xs)+'</ul>'
    if f['laws']: b+='<h2>State drone statutes</h2>'+L(f['laws'])
    else: b+='<h2>State drone statutes</h2><p>No comprehensive statewide drone statute identified; general privacy, trespass and harassment laws apply.</p>'
    b+='<h2>State parks</h2>'+(L(f['parks']) if f['parks'] else '<p>Not yet reviewed; check with the state park agency before flying.</p>')
    if f['local']: b+='<h2>Notable local restrictions</h2>'+L(f['local'])
  else:
    b+=f'<h2>State &amp; local rules</h2><p>We have not yet completed a sourced review of {n} statutes, state park rules and local ordinances. Until then, check the NCSL state law database below and the state park agency before flying. <a href="mailto:d.bot@mail.grokbot.com?subject={n}%20drone%20laws">Know a rule? Tell us.</a></p>'
  b+='<h2>Sources</h2><ul>'+''.join(f'<li><a href="{u}">{t}</a></li>' for t,u in src)+'</ul>'
  os.makedirs(f'docs/states/{slug}',exist_ok=True)
  open(f'docs/states/{slug}/index.html','w').write(page(f'{n} Drone Laws ({R[:4]}) – {NAME}',(f'Drone laws in {n}: FAA Part 107 & recreational rules, Remote ID, LAANC, state statutes and park rules, with sources.' if f else f'Flying a drone in {n}: FAA Part 107 & recreational rules, Remote ID and LAANC, with sources. State-law review in progress.'),f'/states/{slug}/',b,True))
  urls.append(f'/states/{slug}/');items.append(f'<li data-n="{n.lower()}"><a href="{BASE}/states/{slug}/">{n}</a>{" ★" if f else ""}</li>')
home=f'<h1>Drone laws by state</h1><p>FAA rules apply in every state and are covered on every page. Sourced state statutes, park rules and local restrictions are covered for {NF} states so far (★), with more added regularly.</p><input id="q" placeholder="Search states…" oninput="for(l of document.querySelectorAll(\'#s li\'))l.hidden=!l.dataset.n.includes(this.value.toLowerCase())"><ul id="s" class="grid">'+''.join(items)+'</ul>'+faa()
open('docs/index.html','w').write(page(f'{NAME} – Drone Laws by State ({R[:4]})',f'US drone laws by state: FAA Part 107, TRUST, Remote ID and LAANC rules for every state, plus sourced state statutes and park rules for {NF} states so far.','/',home,True))
open('docs/style.css','w').write('body{font:16px/1.5 system-ui;max-width:860px;margin:auto;padding:1em;color:#222}header{border-bottom:2px solid #0a5;padding:.5em 0}a{color:#06c}.grid{columns:3;list-style:none;padding:0}#q{width:100%;padding:.6em;font-size:1em}.box,.ad{background:#f3f7f5;padding:1em;margin:1.5em 0;border-radius:8px}.ad{background:none;padding:0;font-size:.85em;text-align:right}footer{font-size:.85em;color:#555;border-top:1px solid #ddd}@media(max-width:600px){.grid{columns:2}}')
open('docs/sitemap.xml','w').write('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{BASE}{u}</loc><lastmod>{R}</lastmod></url>' for u in urls)+'</urlset>')
open('docs/robots.txt','w').write(f'User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n')
open('docs/.nojekyll','w').write('')
print(len(urls),'pages')
