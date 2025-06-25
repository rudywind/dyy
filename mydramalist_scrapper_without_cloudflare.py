import cloudscraper
from bs4 import BeautifulSoup
import json
import re
import os
import time

scraper = cloudscraper.create_scraper()

# URL dan jumlah halaman maksimal
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

# Muat data lama
if os.path.exists(filename):
    with open(filename, "r", encoding="utf-8") as f:
        all_results = json.load(f)
        print(f"[INFO] Memuat data lama: {len(all_results)} item ditemukan.")
else:
    all_results = []
    print(f"[INFO] Tidak ada file hasil.json, membuat data baru.")

existing_ids = set(item["id"] for item in all_results)

def extract_info(div):
    try:
        a_tag = div.select_one("a.block")
        href = a_tag["href"].strip("/")
        img_tag = div.select_one("img")
        title = img_tag.get("alt", "").strip()
        img_url = img_tag.get("src") or img_tag.get("data-src") or img_tag.get("data-lazy") or ""

        if not href or not img_url:
            print(f"[SKIP] Data tidak lengkap, dilewati.")
            return None

        id_match = re.match(r"(\d+)-", href)
        if not id_match:
            print(f"[SKIP] ID tidak ditemukan di slug: {href}")
            return None

        id_ = id_match.group(1)

        if id_ in existing_ids:
            print(f"[SKIP] ID {id_} sudah ada, dilewati.")
            return None

        print(f"[OK] Data ditemukan: ID={id_}, Title={title}")
        return {
            "id": id_,
            "slug": href,
            "title": title,
            "gambar": img_url.strip()
        }

    except Exception as e:
        print(f"[ERROR] Gagal extract info div: {e}")
        return None

# Fungsi fetch halaman dengan retry untuk error 5xx
def fetch_page_with_retry(url, max_retries=30):
    attempt = 0
    while attempt < max_retries:
        print(f"[FETCH] Mencoba akses: {url} (Percobaan {attempt + 1})")
        try:
            res = scraper.get(url)
            status = res.status_code

            if 200 <= status < 300:
                return res
            elif 400 <= status < 500:
                print(f"[SKIP] Halaman error client {status}, dilewati.")
                return None
            elif 500 <= status < 600:
                print(f"[RETRY] Server error {status}, coba lagi...")
                attempt += 1
                time.sleep(2)
        except Exception as e:
            print(f"[ERROR] Gagal ambil {url}: {e}")
            attempt += 1
            time.sleep(2)

    print(f"[FAIL] Gagal ambil {url} setelah {max_retries} percobaan.")
    return None

# Loop semua halaman
for base_url, max_page in urls:
    for page in range(1, max_page + 1):
        full_url = f"{base_url}{page}"
        response = fetch_page_with_retry(full_url)

        if not response:
            continue  # skip kalau gagal total

        soup = BeautifulSoup(response.text, "html.parser")
        divs = soup.select("div.film-cover")
        print(f"[INFO] {len(divs)} item ditemukan pada halaman ini.")

        for div in divs:
            info = extract_info(div)
            if info:
                all_results.append(info)
                existing_ids.add(info["id"])

        time.sleep(0.5)

# Simpan hasil
try:
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)
        print(f"\n[SAVED] Total item unik disimpan: {len(all_results)} ke file {filename}")
except Exception as e:
    print(f"[ERROR] Gagal simpan file: {e}")
