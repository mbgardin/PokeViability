import re
import time
import json
import requests
import pandas as pd
from bs4 import BeautifulSoup

from utils import ensure_dirs, normalize_name

BASE = "https://www.smogon.com/stats/"
TIERS = ["gen4ubers", "gen4ou", "gen4uu", "gen4nu"]
CUTOFF_CANDIDATES = [1760, 1695, 1630, 1500]  # some months don't have every cutoff

OUT_CSV = "data/raw/smogon_gen4_usage_raw.csv"
META_JSON = "data/raw/smogon_metadata.json"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/122.0 Safari/537.36"
}

def get_latest_month() -> str:
    r = requests.get(BASE, headers=HEADERS, timeout=30)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    months = []
    for a in soup.select("a"):
        href = a.get("href", "")
        if re.fullmatch(r"\d{4}-\d{2}/", href):
            months.append(href.strip("/"))
    if not months:
        raise RuntimeError("Could not find month folders on Smogon stats index.")
    return sorted(months)[-1]

def fetch_json(url: str) -> dict:
    r = requests.get(url, headers=HEADERS, timeout=60)
    # If not OK, return useful error
    if r.status_code != 200:
        snippet = (r.text or "")[:200].replace("\n", " ")
        raise RuntimeError(f"HTTP {r.status_code} for {url} | {snippet}")

    ctype = r.headers.get("Content-Type", "")
    # Smogon should serve application/json; sometimes it's text/html when missing/blocked
    if "json" not in ctype.lower():
        snippet = (r.text or "")[:200].replace("\n", " ")
        raise RuntimeError(f"Non-JSON Content-Type '{ctype}' for {url} | {snippet}")

    return r.json()

def try_find_working_cutoff(month: str, tier: str) -> tuple[int, str]:
    # returns (cutoff, url) for the first cutoff that exists and returns JSON
    for cutoff in CUTOFF_CANDIDATES:
        url = f"{BASE}{month}/chaos/{tier}-{cutoff}.json"
        try:
            _ = fetch_json(url)
            return cutoff, url
        except Exception as e:
            print(f"[warn] {tier} cutoff {cutoff} failed: {e}")
            time.sleep(0.4)
    raise RuntimeError(f"No working cutoff found for {tier} in month {month}")

def main():
    ensure_dirs()

    month = get_latest_month()
    print("[info] Using month:", month)

    available = []
    tier_to_cutoff = {}
    tier_to_url = {}

    for tier in TIERS:
        try:
            cutoff, url = try_find_working_cutoff(month, tier)
            tier_to_cutoff[tier] = cutoff
            tier_to_url[tier] = url
            available.append(tier)
            print(f"[info] {tier}: cutoff={cutoff}")
        except Exception as e:
            print(f"[warn] Skipping {tier}: {e}")

    if not available:
        raise RuntimeError(f"No tiers available for month {month}. Try a different month.")

    rows = []
    for tier in available:
        url = tier_to_url[tier]
        cutoff = tier_to_cutoff[tier]

        print("[info] fetching", url)
        data = fetch_json(url)
        mons = data.get("data", {})
        print(f"[info] {tier} mons={len(mons)}")

        for smogon_name, payload in mons.items():
            rows.append({
                "name_smogon": smogon_name,
                "name_key": normalize_name(smogon_name),
                "tier": tier,
                "cutoff": cutoff,
                "usage": float(payload.get("usage", 0.0)),
                "raw_count": payload.get("Raw count", None),
            })

        time.sleep(0.8)

    df = pd.DataFrame(rows)
    df.to_csv(OUT_CSV, index=False)

    with open(META_JSON, "w") as f:
        json.dump(
            {
                "month": month,
                "tiers_requested": TIERS,
                "tiers_used": available,
                "cutoff_candidates": CUTOFF_CANDIDATES,
                "chosen_cutoffs": tier_to_cutoff
            },
            f,
            indent=2
        )

    print("[done] wrote:", OUT_CSV, "| rows:", len(df))
    print("[done] wrote:", META_JSON)

if __name__ == "__main__":
    main()