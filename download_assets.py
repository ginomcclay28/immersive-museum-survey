import json
import os
import re
import html
import time
import hashlib
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
ASSETS.mkdir(exist_ok=True)

WORKS = [
    ("01-teamlab-borderless", "teamLab Borderless Azabudai Hills"),
    ("02-teamlab-planets", "teamLab Planets Tokyo"),
    ("03-teamlab-botanical-osaka", "teamLab Botanical Garden Osaka"),
    ("04-teamlab-supernature-macao", "teamLab SuperNature Macao"),
    ("05-teamlab-massless-beijing", "teamLab Massless Beijing"),
    ("06-teamlab-phenomena-abu-dhabi", "teamLab Phenomena Abu Dhabi"),
    ("07-arte-museum-jeju", "ARTE MUSEUM Jeju immersive"),
    ("08-arte-museum-gangneung", "ARTE MUSEUM Gangneung immersive"),
    ("09-atelier-des-lumieres", "Atelier des Lumières Paris interior"),
    ("10-bassins-des-lumieres", "Bassins des Lumières Bordeaux interior"),
    ("11-carrieres-des-lumieres", "Carrières des Lumières exhibition"),
    ("12-fabrique-des-lumieres", "Fabrique des Lumières Amsterdam interior"),
    ("13-phoenix-des-lumieres", "Phoenix des Lumières Dortmund"),
    ("14-hall-des-lumieres", "Hall des Lumières New York interior"),
    ("15-bunker-des-lumieres", "Bunker des Lumières Jeju"),
    ("16-frameless-london", "Frameless London immersive art"),
    ("17-lightroom-hockney", "David Hockney Bigger and Closer Lightroom London"),
    ("18-outernet-london", "Outernet London Now Building interior"),
    ("19-house-of-eternal-return", "Meow Wolf House of Eternal Return interior"),
    ("20-omega-mart", "Meow Wolf Omega Mart interior"),
    ("21-convergence-station", "Meow Wolf Convergence Station interior"),
    ("22-the-real-unreal", "Meow Wolf The Real Unreal interior"),
    ("23-otherworld-columbus", "Otherworld Columbus immersive art"),
    ("24-superblue-miami", "Superblue Miami immersive art"),
    ("25-artechouse-dc", "ARTECHOUSE DC immersive exhibition"),
    ("26-illuminarium-las-vegas", "Illuminarium Las Vegas interior"),
    ("27-wonderspaces-arizona", "Wonderspaces Arizona installation"),
    ("28-wndr-museum", "WNDR Museum Chicago interior"),
    ("29-museum-of-dream-space", "Museum of Dream Space Los Angeles"),
    ("30-kusama-infinity-room", "Yayoi Kusama Infinity Mirrored Room Broad"),
    ("31-obliteration-room", "Yayoi Kusama Obliteration Room"),
    ("32-rain-room", "Random International Rain Room Sharjah"),
    ("33-deep-space-8k", "Deep Space 8K Ars Electronica Center"),
    ("34-nxt-museum", "Nxt Museum Amsterdam immersive"),
    ("35-moco-digital", "Moco Museum Amsterdam Studio Irma digital immersive"),
    ("36-dali-cybernetics", "Dalí Cybernetics IDEAL Barcelona"),
    ("37-van-gogh-alive", "Van Gogh Alive The Lume Melbourne"),
    ("38-monet-friends", "Monet and Friends Alive The Lume Melbourne"),
    ("39-miraikan-geocosmos", "Miraikan Geo-Cosmos interior"),
    ("40-museum-of-the-future", "Museum of the Future Dubai interior"),
]

DOMAINS = [
    "teamlab.art", "teamlab.art", "teamlab.art", "teamlab.art", "teamlab.art", "teamlab.art",
    "artemuseum.com", "artemuseum.com", "atelier-lumieres.com", "bassins-lumieres.com",
    "carrieres-lumieres.com", "fabrique-lumieres.com", "phoenix-lumieres.com", "halldeslumieres.com",
    "culturespaces.com", "frameless.com", "lightroom.uk", "outernet.com", "meowwolf.com", "meowwolf.com",
    "meowwolf.com", "meowwolf.com", "otherworld.com", "superblue.com", "artechouse.com", "illuminarium.com",
    "wonderspaces.com", "wndrmuseum.com", "modsmuseum.com", "thebroad.org", "qagoma.qld.gov.au",
    "sharjahart.org", "ars.electronica.art", "nxtmuseum.com", "mocomuseum.com", "idealbarcelona.com",
    "thelumemelbourne.com", "thelumemelbourne.com", "miraikan.jst.go.jp", "museumofthefuture.ae"
]

OFFICIAL_PAGES = [
    "https://www.teamlab.art/e/tokyo/", "https://www.teamlab.art/e/planets/", "https://www.teamlab.art/e/botanicalgarden/",
    "https://www.teamlab.art/e/macao/", "https://art.team-lab.cn/en/e/masslessbeijing/", "https://www.teamlababudhabi.com/",
    "https://artemuseum.com/JEJU", "https://artemuseum.com/GANGNEUNG", "https://www.atelier-lumieres.com/en",
    "https://www.bassins-lumieres.com/en", "https://www.carrieres-lumieres.com/en", "https://www.fabrique-lumieres.com/en",
    "https://www.phoenix-lumieres.com/en", "https://www.halldeslumieres.com/", "https://www.deslumieres.co.kr/bunker/en",
    "https://frameless.com/", "https://lightroom.uk/whats-on/david-hockney-bigger-closer", "https://www.outernet.com/",
    "https://meowwolf.com/visit/santa-fe", "https://meowwolf.com/visit/las-vegas", "https://meowwolf.com/visit/denver",
    "https://meowwolf.com/visit/grapevine", "https://otherworld.com/columbus/", "https://www.superblue.com/miami/",
    "https://www.artechouse.com/location/dc/", "https://illuminarium.com/las-vegas/", "https://www.wonderspaces.com/venues/arizona",
    "https://wndrmuseum.com/location/chicago/", "https://www.xinhuanet.com/english/2019-05/27/c_138094252_9.htm", "https://www.thebroad.org/art/yayoi-kusama/",
    "https://www.qagoma.qld.gov.au/exhibition/yayoi-kusama", "https://www.sharjahart.org/sharjah-art-foundation/projects/rain-room",
    "https://ars.electronica.art/center/en/deep-space-8k/", "https://nxtmuseum.com/", "https://mocomuseum.com/exhibitions/studio-irma-reflecting-forward/",
    "https://idealbarcelona.com/en/agenda/dali-cybernetics/", "https://thelumemelbourne.com/experience/van-gogh-alive/",
    "https://thelumemelbourne.com/experience/monet-friends-alive/", "https://www.miraikan.jst.go.jp/en/exhibitions/tsunagari/",
    "https://museumofthefuture.ae/en"
]

COMMONS_API = "https://commons.wikimedia.org/w/api.php"
HEADERS = {"User-Agent": "ImmersiveMuseumClassDeck/1.0 (educational project)"}

def fetch_json(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=40) as response:
        return json.load(response)

def commons_candidates(query):
    params = {
        "action": "query",
        "format": "json",
        "generator": "search",
        "gsrsearch": f'{query} filetype:bitmap',
        "gsrnamespace": 6,
        "gsrlimit": 18,
        "prop": "imageinfo",
        "iiprop": "url|mime|size",
        "iiurlwidth": 1920,
        "origin": "*",
    }
    url = COMMONS_API + "?" + urllib.parse.urlencode(params)
    data = fetch_json(url)
    pages = list(data.get("query", {}).get("pages", {}).values())
    candidates = []
    for page in pages:
        info = (page.get("imageinfo") or [{}])[0]
        mime = info.get("mime", "")
        width, height = info.get("width", 0), info.get("height", 0)
        url = info.get("thumburl") or info.get("url")
        if url and mime.startswith("image/") and width >= 800 and height >= 500:
            candidates.append({
                "title": page.get("title", ""),
                "url": url,
                "page": "https://commons.wikimedia.org/wiki/" + urllib.parse.quote(page.get("title", "").replace(" ", "_")),
                "width": width,
                "height": height,
            })
    return candidates

def bing_candidates(query, domain):
    exact_query = f'{query} site:{domain}'
    params = urllib.parse.urlencode({"q": exact_query, "form": "HDRSC2", "first": 1})
    req = urllib.request.Request(
        "https://www.bing.com/images/search?" + params,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
        },
    )
    with urllib.request.urlopen(req, timeout=45) as response:
        raw = response.read().decode("utf-8", "ignore")
    results = []
    for attrs in re.findall(r'<a[^>]+class="[^"]*iusc[^"]*"[^>]+m="([^"]+)"', raw):
        try:
            metadata = json.loads(html.unescape(attrs))
        except Exception:
            continue
        url = metadata.get("murl")
        thumb = metadata.get("turl")
        page = metadata.get("purl") or "https://www.bing.com/images/search?" + params
        if url and url.startswith("http"):
            results.append({"title": metadata.get("t", query), "url": url, "page": page, "width": 1920, "height": 1080, "priority": 60})
        if thumb and thumb.startswith("http"):
            results.append({"title": metadata.get("t", query) + " (search preview)", "url": thumb, "page": page, "width": 1280, "height": 720, "priority": 50})
    return results

def official_page_candidates(query, page_url):
    candidates = []
    pages = [page_url]
    parsed = urllib.parse.urlparse(page_url)
    root_url = f"{parsed.scheme}://{parsed.netloc}/"
    if root_url != page_url:
        pages.append(root_url)
    for page_url in pages:
        try:
            page_req = urllib.request.Request(page_url, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36",
                "Accept-Language": "en-US,en;q=0.9",
            })
            with urllib.request.urlopen(page_req, timeout=40) as response:
                page_html = response.read(2_500_000).decode("utf-8", "ignore")
            meta_urls = []
            patterns = [
                r'<meta[^>]+(?:property|name)=["\'](?:og:image|twitter:image(?::src)?)["\'][^>]+content=["\']([^"\']+)',
                r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+(?:property|name)=["\'](?:og:image|twitter:image(?::src)?)["\']',
            ]
            for pattern in patterns:
                meta_urls.extend(re.findall(pattern, page_html, flags=re.I))
            for image_url in meta_urls:
                image_url = urllib.parse.urljoin(page_url, html.unescape(image_url))
                if image_url.startswith("http"):
                    candidates.append({"title": query, "url": image_url, "page": page_url, "width": 1920, "height": 1080, "priority": 120})
            inline_urls = []
            for raw_value in re.findall(r'(?:src|data-src|srcset)=["\']([^"\']+)["\']', page_html, flags=re.I):
                for part in html.unescape(raw_value).split(','):
                    inline_urls.append(part.strip().split(' ')[0])
            for image_url in inline_urls:
                low = image_url.lower()
                if any(word in low for word in ("logo", "icon", "favicon", "sprite", "avatar")):
                    continue
                image_url = urllib.parse.urljoin(page_url, image_url)
                if image_url.startswith("http") and image_url not in {c["url"] for c in candidates}:
                    candidates.append({"title": query, "url": image_url, "page": page_url, "width": 1600, "height": 900, "priority": 75})
        except Exception as exc:
            print(f"  page warning: {urllib.parse.urlparse(page_url).netloc}: {exc}", flush=True)
    return candidates

def score(candidate, query):
    stop = {"the", "and", "museum", "interior", "immersive", "exhibition", "art"}
    q = {w for w in re.findall(r"[a-z0-9]+", query.lower()) if len(w) > 2 and w not in stop}
    title = candidate["title"].lower()
    hits = sum(1 for word in q if word in title)
    landscape = 1 if candidate["width"] >= candidate["height"] else 0
    return candidate.get("priority", 0) + hits * 10 + landscape

def download(url, destination):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=60) as response:
        data = response.read()
        content_type = response.headers.get_content_type()
    if len(data) < 20000:
        raise RuntimeError(f"download too small: {len(data)} bytes")
    destination.write_bytes(data)
    return content_type, hashlib.sha256(data).hexdigest()

PARTIAL = ASSETS / "manifest.partial.json"
manifest = json.loads(PARTIAL.read_text(encoding="utf-8")) if PARTIAL.exists() else []
completed = {item["index"]: item for item in manifest if (ROOT / item["file"]).exists()}
used_urls = {item.get("url") for item in manifest if item.get("url")}
used_hashes = {item["sha256"] for item in manifest}

for position, (slug, query) in enumerate(WORKS, 1):
    safe_query = query.encode('ascii', 'replace').decode('ascii')
    print(f"[{position:02}/40] {safe_query}", flush=True)
    if position in completed:
        print(f"  -> already downloaded: {Path(completed[position]['file']).name}", flush=True)
        continue
    candidates = []
    try:
        candidates.extend(official_page_candidates(query, OFFICIAL_PAGES[position - 1]))
    except Exception as exc:
        print(f"  official-page warning: {exc}", flush=True)
    try:
        candidates.extend(commons_candidates(query))
    except Exception as exc:
        print(f"  commons-search warning: {exc}", flush=True)
    by_url = {item["url"]: item for item in candidates}
    ranked = sorted(by_url.values(), key=lambda item: score(item, query), reverse=True)
    selected = None
    last_error = None
    for candidate in ranked:
        if candidate["url"] in used_urls:
            continue
        lower_url = candidate["url"].lower().split("?")[0]
        ext = ".png" if lower_url.endswith(".png") else ".webp" if lower_url.endswith(".webp") else ".jpg"
        destination = ASSETS / f"{slug}{ext}"
        try:
            mime, digest = download(candidate["url"], destination)
            if digest in used_hashes:
                destination.unlink(missing_ok=True)
                continue
            selected = (candidate, destination, mime, digest)
            break
        except Exception as exc:
            last_error = exc
            destination.unlink(missing_ok=True)
    if not selected:
        raise RuntimeError(f"No usable unique image for {query}: {last_error}")
    candidate, destination, mime, digest = selected
    used_urls.add(candidate["url"])
    used_hashes.add(digest)
    manifest.append({
        "index": position,
        "work": query,
        "file": f"assets/{destination.name}",
        "source": candidate["page"],
        "source_title": candidate["title"],
        "url": candidate["url"],
        "sha256": digest,
        "mime": mime,
    })
    safe_title = candidate['title'].encode('ascii', 'replace').decode('ascii')
    print(f"  -> {destination.name} | {safe_title}", flush=True)
    PARTIAL.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    time.sleep(0.35)

(ASSETS / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
PARTIAL.unlink(missing_ok=True)
keep = {Path(item["file"]).name for item in manifest} | {"manifest.json"}
for old_file in ASSETS.iterdir():
    if old_file.is_file() and old_file.name not in keep:
        old_file.unlink()
print(f"Downloaded {len(manifest)} unique images to {ASSETS}")
