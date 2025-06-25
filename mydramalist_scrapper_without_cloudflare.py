import cloudscraper
from bs4 import BeautifulSoup
import json
import os
import time

scraper = cloudscraper.create_scraper()

urls = [
    ("https://mydramalist.com/search?adv=titles&th=18113&so=relevance&page=", 116),
    ("https://mydramalist.com/search?adv=titles&th=15263&so=relevance&page=", 103),
    ("https://mydramalist.com/search?adv=titles&th=1452&so=relevance&page=", 79),
    ("https://mydramalist.com/search?adv=titles&th=15265&so=relevance&page=", 37),
    ("https://mydramalist.com/search?adv=titles&th=1453&so=relevance&page=", 26),
    ("https://mydramalist.com/search?adv=titles&th=18115&so=relevance&page=", 34),
    ("https://mydramalist.com/search?adv=titles&th=2769&so=relevance&page=", 6),
]

filename = "hasil.json"

if os.path.exists(filename):
    with open(filename, "r", encoding="utf-8") as f:
        all_results = json.load(f)
    print(f"[INFO] Memuat data lama: {len(all_results)} item.")
else:
    all_results = []
    print(f"[INFO] File hasil.json tidak ditemukan, mulai baru.")

existing_ids = set(item["id"] for item in all_results)

def save_to_file(data):
    all_results.append(data)
    existing_ids.add(data["id"])
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)
    print(f"[SAVED] ID={data['id']} disimpan.")

def validate(data):
    for key in ['id', 'slug', 'title']:
        if not data.get(key) or data[key].strip() == "":
            print(f"[INVALID] Kosong pada {key}, ulangi halaman.")
            return False
    return True

def extract_from_box(div):
    try:
        box_id = div.get("id", "")
        if not box_id.startswith("mdl-"):
            print(f"[SKIP] Div id tidak valid: {box_id}")
            return None
        box_id = box_id.replace("mdl-", "")
        if box_id in existing_ids:
            print(f"[SKIP] ID {box_id} sudah ada, dilewati.")
            return None

        a_link = div.select_one("h6.text-primary.title a")
        if not a_link:
            print(f"[ERROR] Tidak ditemukan link judul untuk ID {box_id}")
            return None
        slug = a_link.get("href", "").strip("/")
        title = a_link.text.strip()

        img_tag = div.select_one("div.film-cover img")
        img_url = ""
        if img_tag:
            img_url = img_tag.get("src", "").strip()
            if not img_url:
                img_url = img_tag.get("data-src", "").strip()

        return {
            "id": box_id,
            "slug": slug,
            "title": title,
            "gambar": img_url
        }
    except Exception as e:
        print(f"[ERROR] Gagal ekstrak box: {e}")
        return None

def fetch_page(url, retry=30):
    for attempt in range(retry):
        print(f"[FETCH] {url} (Percobaan {attempt+1})")
        try:
            res = scraper.get(url)
            if 200 <= res.status_code < 300:
                return res
            elif 400 <= res.status_code < 500:
                print(f"[SKIP] Error client {res.status_code}, lewati halaman.")
                return None
            elif 500 <= res.status_code < 600:
                print(f"[RETRY] Error server {res.status_code}, coba ulang...")
                time.sleep(2)
        except Exception as e:
            print(f"[ERROR] Request gagal: {e}")
            time.sleep(2)
    return None

for base_url, max_page in urls:
    print(f"\n[START] URL base: {base_url} sampai halaman {max_page}")
    for page in range(1, max_page + 1):
        full_url = f"{base_url}{page}"
        print(f"\n[PROCESS] Halaman {page}/{max_page}")

        while True:
            response = fetch_page(full_url)
            if response is None:
                print(f"[SKIP] Lewati halaman {page} karena gagal fetch.")
                break

            soup = BeautifulSoup(response.text, "html.parser")
            boxes = soup.select("div.box[id^=mdl-]")
            print(f"[INFO] Halaman {page} ditemukan {len(boxes)} box.")

            halaman_valid = True
            for div in boxes:
                data = extract_from_box(div)
                if data:
                    if not validate(data):
                        halaman_valid = False
                        print(f"[RELOAD] Data tidak valid pada ID {data.get('id')}, ulangi halaman.")
                        break
                    save_to_file(data)

            if halaman_valid:
                print(f"[OK] Halaman {page} selesai diproses.")
                break
            else:
                print(f"[RELOAD] Ulangi halaman {page} karena data tidak valid.")
                time.sleep(1)

        time.sleep(0.5)

print(f"\n[SELESAI] Total data unik disimpan: {len(all_results)} item.")
