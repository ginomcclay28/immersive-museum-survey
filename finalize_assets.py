import hashlib
import json
import shutil
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
MANIFEST = ASSETS / "manifest.json"
CANDIDATES = ASSETS / "hd-candidates"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36"}

SELECTED = {
    6: "06-1.jpg",
    14: "14-7.jpg",
    15: "15-1.jpg",
    18: "18-4.jpg",
    21: "21-2.jpg",
    22: "22-8.jpg",
    23: "23-2.png",
    24: "24-8.webp",
    25: "25-3.jpg",
    28: "28-1.webp",
    31: "31-7.jpg",
    35: "35-1.webp",
    36: "36-3.jpg",
    37: "37-3.webp",
    38: "38-3.jpg",
    39: "39-1.jpg",
}

VERIFY_SELECTED = {
    6: ["https://www.teamlababudhabi.com/en/explore/artworks", "https://art.team-lab.cn/en/e/phenomena/"],
    14: ["https://www.halldeslumieres.com/", "https://www.culturespaces.com/en/sites/hall-des-lumieres"],
    15: ["https://www.deslumieres.co.kr/en/bunker", "https://www.modulo-pi.com/showcase/bunker-de-lumieres/"],
    18: ["https://www.outernet.com/b2b/spaces/the-now-building", "https://www.taittowers.com/work/the-now-building"],
    21: ["https://meowwolf.com/visit/denver", "https://www.denver.org/listing/meow-wolf-denver-%7C-convergence-station/28653/"],
    22: ["https://meowwolf.com/visit/grapevine", "https://www.grapevinetexasusa.com/listing/meow-wolf-grapevine/4978/"],
    23: ["https://www.otherworld.com/", "https://www.experiencecolumbus.com/blog/post/qa-john-umland-operations-director-at-otherworld/"],
    24: ["https://www.superblue.com/miami/", "https://www.miamiandbeaches.com/l/arts-culture/superblue-miami/21175"],
    25: ["https://www.artechouse.com/location/dc/", "https://washington.org/find-dc-listings/artechouse"],
    28: ["https://app.wndrmuseum.com/", "https://www.axios.com/local/chicago/2024/06/17/yayoi-kusama-chicago-wndr-museum"],
    31: ["https://www.qagoma.qld.gov.au/stories/the-obliteration-room-by-yayoi-kusama-is-transformed/", "https://collection.qagoma.qld.gov.au/index.php/objects/18336"],
    35: ["https://www.mocomuseum.com/artists/amsterdam/studio-irma-in-amsterdam/", "https://www.iamsterdam.com/en/whats-on/calendar/museums-and-galleries/museums/moco-museum"],
    36: ["https://idealbarcelona.com/en/agenda/cybernetic-dali/", "https://www.salvador-dali.org/es/fundacion-dali/noticia/dali-cibernetico-en-el-ideal-barcelona/"],
    37: ["https://www.timeout.com/melbourne/art/van-gogh", "https://www.thelume.com/"],
    38: ["https://www.timeout.com/melbourne/art/monet-and-friends", "https://www.racv.com.au/royalauto/lifestyle-home/entertainment/lume-monet-and-friends-alive-exhibition.html"],
    39: ["https://commons.wikimedia.org/wiki/File:Main_hall_and_Geo-Cosmos_in_the_Miraikan_(9409476063).jpg", "https://www.miraikan.jst.go.jp/en/exhibitions/tsunagari/"],
}

DIRECT = {
    8: {
        "url": "https://res.klook.com/image/upload/w_1920,h_1200,c_fill,q_90/w_80,x_15,y_15,g_south_west,l_Klook_water_br_trans_yhcmh3/activities/uasmgph3xrhyzzvz2rvo.webp",
        "source": "https://www.klook.com/ko/activity/67029-arte-museum-gangneung-admission/",
        "verification_sources": [
            "https://www.artemuseum.com/GANGNEUNG",
            "https://www.gn.go.kr/eng/sub06_03_01_08.do",
            "https://www.klook.com/ko/activity/67029-arte-museum-gangneung-admission/",
        ],
    },
    29: {
        "url": "https://images.squarespace-cdn.com/content/v1/5c81f8d10b77bd7cfa2c6904/1562824867538-XX3TMRG3O13XT2UXVMOX/IMG_9492.JPG?format=2500w",
        "source": "https://www.californiabychoice.com/home/museum-of-dream-space",
        "verification_sources": [
            "https://www.discoverlosangeles.com/things-to-do/museum-of-dream-space",
            "https://www.californiabychoice.com/home/museum-of-dream-space",
            "https://www.univision.com/local/los-angeles-kmex/de-paseo-por-la-en-el-museo-de-dream-space-fotos",
        ],
    },
    30: {
        "url": "https://live.staticflickr.com/709/33277394365_b7f804f576_o.jpg",
        "source": "https://www.flickr.com/photos/22711505@N05/33277394365/sizes/o/",
        "verification_sources": [
            "https://hirshhorn.si.edu/kusama/infinity-rooms/",
            "https://www.flickr.com/photos/22711505@N05/33277394365/",
            "https://www.thebroad.org/art/yayoi-kusama/infinity-mirrored-room-souls-millions-light-years-away",
        ],
    },
}

UPGRADED_EXISTING = {
    1: ("https://assets.team-lab.com/b5EBo9Uo-OK6SM09ZTkEZQ/Yt5eET5oZzm6FBicauQUSY/width=2560,format=jpeg", ["https://www.teamlab.art/e/tokyo/", "https://www.azabudai-hills.com/en/azabudaihillsgallery/teamlab-borderless/"]),
    2: ("https://assets.team-lab.com/b5EBo9Uo-OK6SM09ZTkEZQ/89JNH3JuCgHZcGbACeD2vU/width=2560,format=jpeg", ["https://www.teamlab.art/e/planets/", "https://www.gotokyo.org/en/spot/1742/index.html"]),
    3: ("https://assets.team-lab.com/b5EBo9Uo-OK6SM09ZTkEZQ/9cf18fad-ce15-4688-c57a-4c886f573f00/width=2560,format=jpeg", ["https://www.teamlab.art/e/botanicalgarden/", "https://www.nagai-park.jp/teamlab-botanical-garden/"]),
    4: ("https://assets.team-lab.com/b5EBo9Uo-OK6SM09ZTkEZQ/pB8gTFEYFSxgnMpJsrjxHU/width=2560,format=jpeg", ["https://www.teamlab.art/e/macao/", "https://www.venetianmacao.com/entertainment/teamlab.html"]),
    5: ("https://image.team-lab.cn/unsafe/w:2560/plain/s3%3A%2F%2Fimagewave-sites-prd-imageproxy-bucket%2FbLiVDKcWwFSUGbBggaqkS7@jpeg", ["https://art.team-lab.cn/en/e/masslessbeijing/", "https://www.pacegallery.com/exhibitions/teamlab-massless-beijing/"]),
    9: ("https://www.atelier-lumieres.com/sites/default/files/inline-images/van%20gogh%20atelier.JPG", ["https://www.atelier-lumieres.com/en", "https://www.culturespaces.com/en/sites/atelier-des-lumieres"]),
    10: ("https://www.bassins-lumieres.com/sites/default/files/2026-01/frida_kahlo_en_plein_coeur-81823-1600px_1.jpg", ["https://www.bassins-lumieres.com/en", "https://www.culturespaces.com/en/sites/bassins-des-lumieres"]),
    11: ("https://www.carrieres-lumieres.com/sites/default/files/2025-12/cdlpicasso_044_vpinson.jpg", ["https://www.carrieres-lumieres.com/en", "https://www.culturespaces.com/en/sites/carrieres-des-lumieres"]),
    12: ("https://www.fabrique-lumieres.com/sites/default/files/2026-06/klimt_fabrique_des_lumieres_projections_immersive.jpg", ["https://www.fabrique-lumieres.com/en", "https://www.culturespaces.com/en/sites/fabrique-des-lumieres"]),
    13: ("https://www.phoenix-lumieres.com/sites/default/files/2026-06/klimt4_bildnachweis_culturespaces_vincent_pinson_3_0.jpg", ["https://www.phoenix-lumieres.com/en", "https://www.culturespaces.com/en/sites/phoenix-des-lumieres"]),
}


def download(url, destination):
    request = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(request, timeout=90) as response:
        payload = response.read()
        mime = response.headers.get_content_type()
        final_url = response.geturl()
    if not mime.startswith("image/") or len(payload) < 80_000:
        raise RuntimeError(f"Unusable image: {mime} {len(payload)}")
    destination.write_bytes(payload)
    return final_url, mime


manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
candidate_records = json.loads((CANDIDATES / "candidates.json").read_text(encoding="utf-8"))

for index, candidate_name in SELECTED.items():
    item = next(entry for entry in manifest if entry["index"] == index)
    source_file = CANDIDATES / candidate_name
    shutil.copyfile(source_file, ROOT / item["file"])
    record = next(entry for entry in candidate_records if entry["index"] == index and Path(entry["file"]).name == candidate_name)
    item.update(
        source=record["page"],
        url=record["url"],
        verification_sources=VERIFY_SELECTED[index],
        quality_status="verified-hd",
    )

for index, details in DIRECT.items():
    item = next(entry for entry in manifest if entry["index"] == index)
    final_url, mime = download(details["url"], ROOT / item["file"])
    item.update(source=details["source"], url=final_url, mime=mime, verification_sources=details["verification_sources"], quality_status="verified-hd")

for index, (url, verification_sources) in UPGRADED_EXISTING.items():
    item = next(entry for entry in manifest if entry["index"] == index)
    item.update(url=url, verification_sources=verification_sources, quality_status="verified-hd")

for item in manifest:
    payload = (ROOT / item["file"]).read_bytes()
    item["sha256"] = hashlib.sha256(payload).hexdigest()
    item.setdefault("quality_status", "verified-hd")

MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
print("Final HD assets copied and manifest updated")
