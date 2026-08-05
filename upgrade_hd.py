import hashlib
import json
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "assets" / "manifest.json"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

# Exact higher-resolution variants of the same, already-verified photographs.
URLS = {
    1: "https://assets.team-lab.com/b5EBo9Uo-OK6SM09ZTkEZQ/Yt5eET5oZzm6FBicauQUSY/width=2560,format=jpeg",
    2: "https://assets.team-lab.com/b5EBo9Uo-OK6SM09ZTkEZQ/89JNH3JuCgHZcGbACeD2vU/width=2560,format=jpeg",
    3: "https://assets.team-lab.com/b5EBo9Uo-OK6SM09ZTkEZQ/9cf18fad-ce15-4688-c57a-4c886f573f00/width=2560,format=jpeg",
    4: "https://assets.team-lab.com/b5EBo9Uo-OK6SM09ZTkEZQ/pB8gTFEYFSxgnMpJsrjxHU/width=2560,format=jpeg",
    5: "https://image.team-lab.cn/unsafe/w:2560/plain/s3%3A%2F%2Fimagewave-sites-prd-imageproxy-bucket%2FbLiVDKcWwFSUGbBggaqkS7@jpeg",
    9: "https://www.atelier-lumieres.com/sites/default/files/inline-images/van%20gogh%20atelier.JPG",
    10: "https://www.bassins-lumieres.com/sites/default/files/2026-01/frida_kahlo_en_plein_coeur-81823-1600px_1.jpg",
    11: "https://www.carrieres-lumieres.com/sites/default/files/2025-12/cdlpicasso_044_vpinson.jpg",
    12: "https://www.fabrique-lumieres.com/sites/default/files/2026-06/klimt_fabrique_des_lumieres_projections_immersive.jpg",
    13: "https://www.phoenix-lumieres.com/sites/default/files/2026-06/klimt4_bildnachweis_culturespaces_vincent_pinson_3_0.jpg",
    24: "https://cdn.prod.website-files.com/650ba1c41a78874c2e6faac3/65c2e30c9e7183cdd1515f29_superblue-miami-immersive-art-experiences-11.jpg?w=2400&q=95",
    37: "https://live.staticflickr.com/65535/52027669613_aec72fc895_k.jpg",
}

VERIFY = {
    1: ["https://www.teamlab.art/e/tokyo/", "https://www.azabudai-hills.com/en/azabudaihillsgallery/teamlab-borderless/"],
    2: ["https://www.teamlab.art/e/planets/", "https://www.gotokyo.org/en/spot/1742/index.html"],
    3: ["https://www.teamlab.art/e/botanicalgarden/", "https://www.nagai-park.jp/teamlab-botanical-garden/"],
    4: ["https://www.teamlab.art/e/macao/", "https://www.venetianmacao.com/entertainment/teamlab.html"],
    5: ["https://art.team-lab.cn/en/e/masslessbeijing/", "https://www.pacegallery.com/exhibitions/teamlab-massless-beijing/"],
    9: ["https://www.atelier-lumieres.com/en", "https://www.culturespaces.com/en/sites/atelier-des-lumieres"],
    10: ["https://www.bassins-lumieres.com/en", "https://www.culturespaces.com/en/sites/bassins-des-lumieres"],
    11: ["https://www.carrieres-lumieres.com/en", "https://www.culturespaces.com/en/sites/carrieres-des-lumieres"],
    12: ["https://www.fabrique-lumieres.com/en", "https://www.culturespaces.com/en/sites/fabrique-des-lumieres"],
    13: ["https://www.phoenix-lumieres.com/en", "https://www.culturespaces.com/en/sites/phoenix-des-lumieres"],
    24: ["https://www.superblue.com/miami/", "https://www.miamiandbeaches.com/l/arts-culture/superblue-miami/21175"],
    37: ["https://thelumemelbourne.com/experience/van-gogh-alive/", "https://www.flickr.com/photos/georgiou/sets/72177720298359186/"],
}


def download(url: str):
    request = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(request, timeout=90) as response:
        payload = response.read()
        mime = response.headers.get_content_type()
        final_url = response.geturl()
    if not mime.startswith("image/") or len(payload) < 25_000:
        raise RuntimeError(f"Not a usable image: {mime}, {len(payload):,} bytes")
    return payload, mime, final_url


manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
for index, url in URLS.items():
    item = next(entry for entry in manifest if entry["index"] == index)
    payload, mime, final_url = download(url)
    destination = ROOT / item["file"]
    destination.write_bytes(payload)
    item.update(
        url=final_url,
        mime=mime,
        sha256=hashlib.sha256(payload).hexdigest(),
        verification_sources=VERIFY[index],
        quality_status="candidate-hd",
    )
    print(f"{index:02}: {destination.name} {len(payload):,} bytes")

MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
