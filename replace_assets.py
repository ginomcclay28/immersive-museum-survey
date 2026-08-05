import hashlib, html, json, re, urllib.parse, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
MANIFEST = ASSETS / "manifest.json"
UA = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36","Accept-Language":"en-US,en;q=0.9"}

PAGES = {
  7: "https://insidejeju.com/attractions/arte-museum-jeju/",
  8: "https://english.news.cn/20220208/6f3267d9ef8e4c6d9924fe4aa8c8608e/c.html",
  14: "https://renaissance.halldeslumieres.com/",
  15: "https://hongdiarytravel.com/bunker-des-lumieres-jeju-en/",
  16: "https://www.visitlondon.com/things-to-do/place/49238804-frameless",
  17: "https://www.visitlondon.com/things-to-do/place/51021303-david-hockney-bigger-and-closer",
  18: "https://www.taittowers.com/work/the-now-building",
  23: "https://www.akronlife.com/travel/columbus-otherworld/",
  26: "https://lasvegasthenandnow.com/review-of-illuminarium-at-area15-las-vegas-look-inside/",
  29: "https://www.univision.com/local/los-angeles-kmex/de-paseo-por-la-en-el-museo-de-dream-space-fotos",
  30: "https://www.davidzwirner.com/artworks/yayoi-kusama-infinity-mirrored-room-the-souls-of-millions-of-light-years-awa-ad4eb",
  34: "https://nxtmuseum.com/exhibition/still-processing",
  36: "https://www.catalannews.com/culture/item/immersive-dali-metaverse-experience-coming-to-barcelona",
  37: "https://www.flickr.com/photos/georgiou/sets/72177720298359186/",
  38: "https://www.racv.com.au/royalauto/lifestyle-home/entertainment/lume-monet-and-friends-alive-exhibition.html",
}

DIRECT = {
  19: "https://commons.wikimedia.org/wiki/Special:Redirect/file/Meow%20Wolf%20Santa%20Fe%20-%20House%20of%20Eternal%20Return.jpg?width=1920",
  20: "https://commons.wikimedia.org/wiki/Special:Redirect/file/Omega%20mart%202021.jpg?width=1920",
  31: "https://commons.wikimedia.org/wiki/Special:Redirect/file/Yayoi%20Kusama%20Obliteration%20Room.jpg?width=1920",
  32: "https://commons.wikimedia.org/wiki/Special:Redirect/file/RainRoomSharjah.jpg?width=1920",
  40: "https://commons.wikimedia.org/wiki/Special:Redirect/file/Museum%20of%20the%20Future%20inside-Dubai%20UAE-Andres%20Larin.jpg?width=1920",
}

def read_url(url, limit=None):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read(limit), r.headers.get_content_type(), r.geturl()

def page_images(page):
    raw, _, final = read_url(page, 3_000_000)
    text = raw.decode("utf-8", "ignore")
    found = []
    pats = [
      r'<meta[^>]+(?:property|name)=["\'](?:og:image|twitter:image(?::src)?)["\'][^>]+content=["\']([^"\']+)',
      r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+(?:property|name)=["\'](?:og:image|twitter:image(?::src)?)["\']',
    ]
    for pat in pats: found += re.findall(pat, text, re.I)
    for val in re.findall(r'(?:src|data-src|srcset)=["\']([^"\']+)["\']', text, re.I):
        found += [part.strip().split(' ')[0] for part in html.unescape(val).split(',')]
    out=[]
    for u in found:
        u=urllib.parse.urljoin(final,html.unescape(u))
        low=u.lower()
        if u.startswith('http') and not any(x in low for x in ('logo','icon','favicon','sprite','avatar','.svg')) and u not in out: out.append(u)
    return out

manifest=json.loads(MANIFEST.read_text(encoding='utf-8'))
DONE={7,8,14,15,16,17,19,20,23,26,29,30,31,32,38}
for idx in DONE:
    entry=next(x for x in manifest if x['index']==idx)
    payload=(ROOT/entry['file']).read_bytes()
    entry.update({"source":PAGES.get(idx,"https://commons.wikimedia.org/"),"mime":"image/jpeg","sha256":hashlib.sha256(payload).hexdigest(),"source_title":entry['work']})
used={item['sha256'] for item in manifest if item['index'] not in (set(PAGES)|set(DIRECT))-DONE}

for index in sorted(set(PAGES)|set(DIRECT)):
    item=next(x for x in manifest if x['index']==index)
    if index in DONE:
        print(f"{index:02} -> already replaced")
        continue
    candidates=[DIRECT[index]] if index in DIRECT else page_images(PAGES[index])
    if index==18: candidates=[u for u in candidates if 'outernet-og-image' not in u.lower()]
    selected=None
    for url in candidates:
        try:
            data,mime,final=read_url(url)
            digest=hashlib.sha256(data).hexdigest()
            if not mime.startswith('image/') or mime in ('image/svg+xml','image/avif') or len(data)<25000 or digest in used: continue
            selected=(data,mime,final,digest)
            break
        except Exception as exc:
            print(f"{index:02} skip {url[:70]}: {exc}")
    if not selected: raise RuntimeError(f"No replacement image for slide {index}")
    data,mime,final,digest=selected
    dest=ROOT/item['file']
    dest.write_bytes(data)
    item.update({"source":PAGES.get(index,"https://commons.wikimedia.org/"),"url":final,"mime":mime,"sha256":digest,"source_title":item['work']})
    used.add(digest)
    print(f"{index:02} -> {dest.name} {mime} {len(data):,}")

MANIFEST.write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print("Replacements complete")
