import os
import pandas as pd
import matplotlib.pyplot as plt

def main():
    os.makedirs("data/visuals", exist_ok=True)
    df = pd.read_csv("data/cleaned/pokemon_gen4_competitive.csv")

    # 1. Histogram of BST
    plt.figure(figsize=(8, 6))
    plt.hist(df["bst"].dropna(), bins=20, edgecolor="black")
    plt.title("Distribution of Base Stat Totals (BST)")
    plt.xlabel("Base Stat Total")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig("data/visuals/bst_histogram.png")
    plt.close()

    # 2. Boxplot: BST by is_ou
    plt.figure(figsize=(8, 6))
    ou_data = df[df["is_ou"] == 1]["bst"].dropna()
    non_ou_data = df[df["is_ou"] == 0]["bst"].dropna()
    plt.boxplot([non_ou_data, ou_data], labels=["Not OU", "OU"])
    plt.title("Base Stat Total (BST) by OU Status")
    plt.xlabel("Usage Status")
    plt.ylabel("Base Stat Total")
    plt.tight_layout()
    plt.savefig("data/visuals/bst_boxplot.png")
    plt.close()

    # 3. Bar chart of OU primary types
    plt.figure(figsize=(10, 6))
    ou_df = df[df["is_ou"] == 1]
    type_counts = ou_df["type1"].value_counts().sort_values(ascending=False)
    type_counts.plot(kind="bar", edgecolor="black")
    plt.title("Primary Types of OU Pokémon")
    plt.xlabel("Primary Type")
    plt.ylabel("Count")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("data/visuals/ou_types_bar.png")
    plt.close()

    print("Visuals generated in data/visuals/")

if __name__ == "__main__":
    main()
