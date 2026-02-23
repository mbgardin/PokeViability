import pandas as pd

# tiers you WANT in the final dataset, even if Smogon didn't publish some this month
TIER_ORDER = {
    "gen4ubers": 4,
    "gen4ou": 3,
    "gen4uu": 2,
    "gen4nu": 1
}

INFILE = "data/raw/merged_gen4_raw.csv"
OUTFILE = "data/cleaned/pokemon_gen4_competitive.csv"

def main():
    df = pd.read_csv(INFILE)

    tier_cols = list(TIER_ORDER.keys())

    # --- critical fix: ensure missing tier columns exist ---
    for t in tier_cols:
        if t not in df.columns:
            df[t] = 0.0

    # stats engineering
    df["bst"] = df[["hp","attack","defense","sp_attack","sp_defense","speed"]].sum(axis=1)
    df["has_two_types"] = df["type2"].notna().astype(int)

    # usage engineering
    df["max_usage"] = df[tier_cols].max(axis=1)
    df["formats_used_count"] = (df[tier_cols] > 0).sum(axis=1)
    df["is_ou"] = (df["gen4ou"] > 0).astype(int)
    
    def best_tier(row):
        candidates = [t for t in tier_cols if row[t] > 0]
        if not candidates:
            return None
        return sorted(candidates, key=lambda x: TIER_ORDER[x], reverse=True)[0]

    df["best_tier"] = df.apply(best_tier, axis=1)

    # nicer column names for the final CSV
    df = df.rename(columns={
        "gen4ubers": "usage_ubers",
        "gen4ou": "usage_ou",
        "gen4uu": "usage_uu",
        "gen4nu": "usage_nu"
    })

    df.to_csv(OUTFILE, index=False)
    print("Wrote:", OUTFILE)
    print("Rows:", len(df), "Cols:", df.shape[1])

if __name__ == "__main__":
    main()