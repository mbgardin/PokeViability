# src/pull_pokeapi.py

import time
import pandas as pd
from utils import ensure_dirs, get_json, normalize_name

BASE = "https://pokeapi.co/api/v2"
MAX_ID = 493
OUTFILE = "data/raw/pokeapi_gen4_raw.csv"

def flatten_pokemon(p: dict) -> dict:
    stats_map = {s["stat"]["name"]: s["base_stat"] for s in p["stats"]}
    types = [t["type"]["name"] for t in sorted(p["types"], key=lambda x: x["slot"])]

    species = get_json(p["species"]["url"])

    return {
        "id": p["id"],
        "name_pokeapi": p["name"],
        "name_key": normalize_name(p["name"]),
        "type1": types[0] if len(types) else None,
        "type2": types[1] if len(types) > 1 else None,
        "hp": stats_map.get("hp"),
        "attack": stats_map.get("attack"),
        "defense": stats_map.get("defense"),
        "sp_attack": stats_map.get("special-attack"),
        "sp_defense": stats_map.get("special-defense"),
        "speed": stats_map.get("speed"),
        "height_dm": p.get("height"),
        "weight_hg": p.get("weight"),
        "is_legendary": bool(species.get("is_legendary")),
        "is_mythical": bool(species.get("is_mythical")),
    }

def main():
    ensure_dirs()

    rows = []

    for pid in range(1, MAX_ID + 1):
        p = get_json(f"{BASE}/pokemon/{pid}")
        rows.append(flatten_pokemon(p))
        time.sleep(0.10)

    df = pd.DataFrame(rows)
    df.to_csv(OUTFILE, index=False)
    print("Wrote:", OUTFILE, "| rows:", len(df), "| cols:", df.shape[1])

if __name__ == "__main__":
    main()