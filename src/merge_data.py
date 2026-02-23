import pandas as pd
from utils import ensure_dirs

TIERS = ["gen4ubers", "gen4ou", "gen4uu", "gen4nu"]

def main():
    ensure_dirs()

    poke = pd.read_csv("data/raw/pokeapi_gen4_raw.csv")
    smog = pd.read_csv("data/raw/smogon_gen4_usage_raw.csv")

    usage_wide = (
        smog.pivot_table(index="name_key", columns="tier", values="usage", aggfunc="max")
            .reset_index()
    )

    # ensure all desired tier columns exist even if Smogon didn't publish them
    for t in TIERS:
        if t not in usage_wide.columns:
            usage_wide[t] = 0.0

    merged = poke.merge(usage_wide, on="name_key", how="left")

    # Fill only the tier columns (numeric) with 0.0
    for t in TIERS:
        merged[t] = merged[t].fillna(0.0)

    merged.to_csv("data/raw/merged_gen4_raw.csv", index=False)
    print("Wrote: data/raw/merged_gen4_raw.csv | rows:", len(merged), "| cols:", merged.shape[1])

if __name__ == "__main__":
    main()