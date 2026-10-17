import json,os,html,shutil,urllib.parse
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
VLOS="Keep the drone within visual line of sight; don\'t fly over people or moving vehicles except as Part 107 allows; respect TFRs (stadiums, VIP movement, wildfires)."
e=html.escape

# ---- visual helpers (inline SVG only; no external assets) ----
IC={
 'license':'<rect x="3" y="5" width="18" height="14" rx="2"/><circle cx="9" cy="11" r="2.2"/><path d="M5.8 16a3.4 3.4 0 0 1 6.4 0M14 10h4M14 13.5h3"/>',
 'altitude':'<path d="M12 3v14M7 8l5-5 5 5M4 21h16"/><path d="M8 17h8" stroke-dasharray="2 2"/>',
 'remoteid':'<circle cx="12" cy="12" r="2"/><path d="M8.5 15.5a5 5 0 0 1 0-7M15.5 8.5a5 5 0 0 1 0 7M5.6 18.4a9 9 0 0 1 0-12.8M18.4 5.6a9 9 0 0 1 0 12.8"/>',
 'register':'<path d="M9 4h6a1 1 0 0 1 1 1v1H8V5a1 1 0 0 1 1-1z"/><path d="M8 5H6a1 1 0 0 0-1 1v14a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V6a1 1 0 0 0-1-1h-2M9 13l2 2 4-4"/>',
 'eye':'<path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
 'gavel':'<path d="M14 4l6 6M11 7l6 6M12.5 5.5l-5 5 6 6 5-5M10 13l-7 7M3 21h9"/>',
 'tree':'<path d="M12 3l6 8h-3l4 6H5l4-6H6z"/><path d="M12 17v4"/>',
 'pin':'<path d="M12 21s-7-6.2-7-12a7 7 0 0 1 14 0c0 5.8-7 12-7 12z"/><circle cx="12" cy="9" r="2.5"/>',
 'book':'<path d="M4 4.5A1.5 1.5 0 0 1 5.5 3H19v15H6.5A2.5 2.5 0 0 0 4 20.5z"/><path d="M4 20.5A2.5 2.5 0 0 1 6.5 18H19v3H6.5M8 7.5h7M8 11h5"/>',
 'link':'<path d="M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1 1M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1-1"/>',
 'search':'<circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/>',
 'sun':'<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
 'moon':'<path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/>',
 'alert':'<path d="M12 3l9.5 17h-19z"/><path d="M12 10v4M12 17h.01"/>',
 'bell':'<path d="M6 16V11a6 6 0 0 1 12 0v5l2 2H4zM10 20a2 2 0 0 0 4 0"/>',
 'check':'<path d="M20 6L9 17l-5-5"/>',
 'clock':'<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
 'arrow':'<path d="M5 12h14M13 6l6 6-6 6"/>',
 'map':'<path d="M9 4L3 6v14l6-2 6 2 6-2V4l-6 2z"/><path d="M9 4v14M15 6v14"/>',
 'mail':'<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',
 'star':'<path d="M12 3l2.8 5.7 6.2.9-4.5 4.4 1 6.2L12 17.3 6.5 20.2l1-6.2L3 9.6l6.2-.9z"/>',
}
def ic(n,c='i'): return f'<svg class="{c}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{IC[n]}</svg>'
DRONE='<svg class="logo-mark" viewBox="0 0 32 32" aria-hidden="true" focusable="false"><defs><linearGradient id="dg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0ea5e9"/><stop offset=".6" stop-color="#22d3ee"/><stop offset="1" stop-color="#34d399"/></linearGradient></defs><rect width="32" height="32" rx="9" fill="url(#dg)"/><g fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round"><path d="M10 10l12 12M22 10L10 22"/><circle cx="9" cy="9" r="3"/><circle cx="23" cy="9" r="3"/><circle cx="9" cy="23" r="3"/><circle cx="23" cy="23" r="3"/></g><rect x="13" y="13" width="6" height="6" rx="1.6" fill="#fff"/></svg>'
FAV="data:image/svg+xml,"+urllib.parse.quote('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="9" fill="#0ea5e9"/><g fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round"><path d="M10 10l12 12M22 10L10 22"/><circle cx="9" cy="9" r="3"/><circle cx="23" cy="9" r="3"/><circle cx="9" cy="23" r="3"/><circle cx="23" cy="23" r="3"/></g><rect x="13" y="13" width="6" height="6" rx="1.6" fill="#fff"/></svg>')
FAQI=['license','altitude','remoteid','register']
ABBR=dict(zip(S,"AL AK AZ AR CA CO CT DE DC FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NV NH NJ NM NY NC ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY".split()))
# tile-grid map layout: abbr -> (row, col)
TILES={}
for r,row in enumerate(["AK0 ME11","WI6 VT10 NH11","WA1 ID2 MT3 ND4 MN5 IL6 MI7 NY9 MA10 RI11","OR1 NV2 WY3 SD4 IA5 IN6 OH7 PA8 NJ9 CT10","CA1 UT2 CO3 NE4 MO5 KY6 WV7 VA8 MD9 DE10","AZ2 NM3 KS4 AR5 TN6 NC7 SC8 DC9","OK4 LA5 MS6 AL7 GA8","HI0 TX4 FL9"]):
  for t in row.split(): TILES[t[:2]]=(r,int(t[2:]))
assert sorted(TILES)==sorted(ABBR.values()),'tile map must cover every state'
def slug_of(s): return s.replace('_',' ').lower().replace(' ','-')
CUR=' aria-current="page"'
def tilemap(current=None,small=False):
  sz,g=48,4;cells=[]
  for s in S:
    a=ABBR[s];r,c=TILES[a];n=s.replace('_',' ');sl=slug_of(s);src=sl in D['focus']
    x,y=c*(sz+g),r*(sz+g);cls='t '+('src' if src else 'faa')+(' cur' if sl==current else '')
    cells.append(f'<a href="{BASE}/states/{sl}/" class="{cls}" aria-label="{e(n)}: {"sourced state laws" if src else "FAA rules only"}"{CUR if sl==current else ""}><title>{e(n)} — {"sourced state laws" if src else "FAA baseline only"}</title><rect x="{x}" y="{y}" width="{sz}" height="{sz}" rx="10"/><text x="{x+sz/2}" y="{y+sz/2+1}">{a}</text></a>')
  w=12*(sz+g)-g;h=8*(sz+g)-g
  return f'<svg class="usmap{" sm" if small else ""}" viewBox="0 0 {w} {h}" role="img" aria-label="Map of US states colored by coverage: sourced state laws or FAA rules only"><defs><linearGradient id="tg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0ea5e9"/><stop offset="1" stop-color="#10b981"/></linearGradient></defs>{"".join(cells)}</svg>'
LEGEND=f'<div class="legend"><span><i class="sw src"></i>Sourced state laws ({NF})</span><span><i class="sw faa"></i>FAA rules only ({len(S)-NF})</span></div>'
THEME="<script>try{var t=localStorage.getItem('theme');if(t)document.documentElement.setAttribute('data-theme',t)}catch(e){}</script>"

def page(t,d,path,body,faq=False):
  ld='' if not faq else '<script type="application/ld+json">'+json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in FAQ]})+'</script>'
  form=('<h2>'+ic('bell')+'Rule change alerts</h2><form action="'+FORM+'" method="POST"><input type="email" name="email" placeholder="you@example.com" required aria-label="Email"><input type="hidden" name="list" value="alerts"><button>Subscribe</button></form>') if SHOW_FORM else '<!-- NEWSLETTER HOOK: set FORM_ID env var to enable the alerts form -->'
  return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(t)}</title><meta name="description" content="{e(d)}"><link rel="canonical" href="{BASE}{path}"><meta property="og:title" content="{e(t)}"><meta property="og:description" content="{e(d)}"><meta property="og:type" content="website"><meta property="og:url" content="{BASE}{path}"><meta name="color-scheme" content="light dark">{THEME}<link rel="icon" href="{FAV}"><link rel="stylesheet" href="{BASE}/style.css">{ld}</head><body><a class="skip" href="#main">Skip to content</a>
<header class="site-head"><div class="wrap head-in"><a class="logo" href="{BASE}/">{DRONE}<span><b>{NAME}</b><small> drone laws by state</small></span></a><nav aria-label="Main"><a href="{BASE}/#states">{ic('map')}<span>States</span></a><a href="{BASE}/#faa">{ic('book')}<span>FAA rules</span></a></nav><button class="icon-btn" id="theme" type="button" aria-label="Toggle dark mode">{ic('sun','i sun')}{ic('moon','i moon')}</button></div></header><main id="main">{body}
<div class="wrap"><section class="box">{form}<p>{ic('alert')}Spotted a rule change or error? <a href="mailto:d.bot@mail.grokbot.com?subject=Rule%20change%20report">Report it</a>.</p></section>
<p class="ad"><!-- AFFILIATE SLOT: Part 107 course (add real link here) --><!-- AFFILIATE SLOT: drone gear (add real link here) --><a href="mailto:d.bot@mail.grokbot.com?subject=Sponsorship">Advertise / sponsor this page</a></p></div>
</main><footer class="site-foot"><div class="wrap"><div class="disc">{ic('alert')}<p><b>Disclaimer:</b> Informational only, not legal advice. Laws change; verify with the FAA, state statutes and local authorities before flying. Last reviewed {R}.</p></div><p class="by">{DRONE}<span>{NAME}</span></p></div></footer><script src="{BASE}/app.js"></script></body></html>'''
def faa():
  cards=''.join(f'<li class="rule"><span class="ico">{ic(FAQI[i])}</span><div><b>{e(q)}</b> {e(a)}</div></li>' for i,(q,a) in enumerate(FAQ))
  return f'<section class="sec" id="faa"><div class="sec-h"><span class="kicker">{ic("book")}Applies everywhere</span><h2>FAA baseline (all states)</h2></div><ul class="rules">{cards}<li class="rule wide"><span class="ico">{ic("eye")}</span><div>{e(VLOS)}</div></li></ul></section>'
def dom(u): return urllib.parse.urlparse(u).netloc.replace('www.','')
def cite(u): return f'<a class="cite" href="{u}" rel="noopener">{ic("link")}<span>[source]</span><span class="dom">{e(dom(u))}</span></a>'
def L(xs,icon): return '<ul class="cards">'+''.join(f'<li class="lawcard"><span class="ico">{ic(icon)}</span><div><p>{e(t)}</p>{cite(u) if u else ""}</div></li>' for t,u in xs)+'</ul>'
def secw(icon,title,inner,id_=''):
  return f'<section class="sec"{f" id={id_}" if id_ else ""}><h2 class="h-ic">{ic(icon)}{title}</h2>{inner}</section>'

os.makedirs('docs/states',exist_ok=True);urls=['/'];items=[]
for s in S:
  n=s.replace('_',' ');slug=n.lower().replace(' ','-');f=D['focus'].get(slug)
  badge=f'<span class="cov src">{ic("check")}Sourced state review</span>' if f else f'<span class="cov faa">{ic("clock")}FAA baseline &middot; state review in progress</span>'
  b=f'<section class="hero st"><div class="glow" aria-hidden="true"></div><div class="wrap st-in"><div><nav class="crumbs" aria-label="Breadcrumb"><a href="{BASE}/">Home</a><span>/</span><a href="{BASE}/#states">States</a><span>/</span><span aria-current="page">{n}</span></nav><h1>Drone laws in {n}</h1><div class="st-meta">{badge}<p class="rev">{ic("clock")}Last reviewed {R}</p></div></div><div class="map-card mini"><p class="mini-h">Jump to another state</p>{tilemap(slug,True)}{LEGEND}</div></div></section><div class="wrap">'
  state=''
  src=list(FS)
  if f:
    if f['laws']: state+=secw('gavel','State drone statutes',L(f['laws'],'gavel'))
    else: state+=secw('gavel','State drone statutes','<div class="note"><p>No comprehensive statewide drone statute identified; general privacy, trespass and harassment laws apply.</p></div>')
    state+=secw('tree','State parks',(L(f['parks'],'tree') if f['parks'] else '<div class="note"><p>Not yet reviewed; check with the state park agency before flying.</p></div>'))
    if f['local']: state+=secw('pin','Notable local restrictions',L(f['local'],'pin'))
  else:
    state+=secw('map','State &amp; local rules',f'<div class="note pending"><p>We have not yet completed a sourced review of {n} statutes, state park rules and local ordinances. Until then, check the NCSL state law database below and the state park agency before flying. <a href="mailto:d.bot@mail.grokbot.com?subject={n}%20drone%20laws">Know a rule? Tell us.</a></p></div>')
  b+=state+faa()
  b+=secw('book','Sources','<ol class="sources">'+''.join(f'<li><a href="{u}"><span>{t}</span><small>{e(dom(u))}</small>{ic("arrow","i arr")}</a></li>' for t,u in src)+'</ol>')+'</div>'
  os.makedirs(f'docs/states/{slug}',exist_ok=True)
  open(f'docs/states/{slug}/index.html','w').write(page(f'{n} Drone Laws ({R[:4]}) – {NAME}',(f'Drone laws in {n}: FAA Part 107 & recreational rules, Remote ID, LAANC, state statutes and park rules, with sources.' if f else f'Flying a drone in {n}: FAA Part 107 & recreational rules, Remote ID and LAANC, with sources. State-law review in progress.'),f'/states/{slug}/',b,True))
  urls.append(f'/states/{slug}/');items.append(f'<li data-n="{n.lower()}" class="{"src" if f else "faa"}"><a href="{BASE}/states/{slug}/"><span class="ab">{ABBR[s]}</span><span class="nm">{n}</span>{"<span class=star> ★</span>" if f else ""}</a></li>')
home=f'''<section class="hero home"><div class="glow" aria-hidden="true"></div><div class="sky" aria-hidden="true"></div><div class="wrap home-in"><div class="home-copy"><span class="kicker">{ic("clock")}Last reviewed {R}</span><h1>Drone laws <span class="grad">by state</span></h1><p class="lead">FAA rules apply in every state and are covered on every page. Sourced state statutes, park rules and local restrictions are covered for {NF} states so far (★), with more added regularly.</p>
<div class="stats"><div><b>{len(S)}</b><span>state guides</span></div><div><b>{NF}</b><span>sourced reviews</span></div><div><b>{len(FS)}</b><span>FAA &amp; NCSL sources</span></div></div></div>
<div class="map-card" id="states">{tilemap()}{LEGEND}</div></div></section>
<div class="wrap"><section class="sec"><div class="sec-h row"><h2>All states</h2><label class="searchbox">{ic("search")}<input id="q" type="search" placeholder="Search states…" aria-label="Search states" autocomplete="off"></label></div><ul id="s" class="grid">{"".join(items)}</ul><p class="empty" id="empty" hidden>No states match.</p></section>
{faa()}</div>'''
open('docs/index.html','w').write(page(f'{NAME} – Drone Laws by State ({R[:4]})',f'US drone laws by state: FAA Part 107, TRUST, Remote ID and LAANC rules for every state, plus sourced state statutes and park rules for {NF} states so far.','/',home,True))
shutil.copy('static/style.css','docs/style.css');shutil.copy('static/app.js','docs/app.js')
open('docs/sitemap.xml','w').write('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{BASE}{u}</loc><lastmod>{R}</lastmod></url>' for u in urls)+'</urlset>')
open('docs/robots.txt','w').write(f'User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n')
open('docs/.nojekyll','w').write('')
print(len(urls),'pages')
