# PokeViability: Gen 4 Competitive Pokémon Analysis

## 1. Project Overview
This project explores the relationship between a Pokémon's base stats, typing, and its viability in the competitive Gen 4 (Diamond/Pearl/Platinum) metagame. By combining data from PokéAPI and Smogon usage statistics, we construct a comprehensive dataset to analyze what makes a Pokémon successful in competitive play.

## 2. Motivating Question
**How do base stats and typing relate to competitive viability in the Gen 4 metagame?** 

Are higher Base Stat Totals (BST) always indicative of OverUsed (OU) status, and what role do secondary typings play in determining a Pokémon's tier?

## 3. Data Sources
This project relies on two public data sources:
*   [**PokéAPI**](https://pokeapi.co/): A comprehensive, RESTful API providing baseline Pokémon statistics, typings, and physical characteristics.
*   [**Smogon Usage Stats**](https://www.smogon.com/stats/): Publicly available JSON endpoints detailing the usage frequency of Pokémon across different competitive tiers and formats.

## 4. How to Reproduce
To reproduce the dataset from scratch, ensure you have Python 3 installed, then run the following commands:

```bash
# Clone the repository and navigate to the project directory
git clone <your-repo-url>
cd PokeViability

# Create and activate a virtual environment (optional but recommended)
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the data collection pipeline in order
python src/pull_pokeapi.py
python src/scrape_smogon.py
python src/merge_data.py
python src/clean_transform.py
```
This will fetch the raw data, merge it, apply transformations, and output the final cleaned dataset to `data/cleaned/pokemon_gen4_competitive.csv`.

## 5. Dataset Description
The final dataset (`data/cleaned/pokemon_gen4_competitive.csv`) contains **493 rows** (one for each Gen 4 Pokémon) and **21 columns**.

### Short Data Dictionary
*   `id`: National Pokédex number (1-493)
*   `name_pokeapi` / `name_key`: Pokémon name (standardized for merging)
*   `type1` / `type2`: Primary and secondary elemental typings
*   `hp`, `attack`, `defense`, `sp_attack`, `sp_defense`, `speed`: Individual base stats
*   `bst`: Base Stat Total (sum of all six core stats)
*   `is_legendary` / `is_mythical`: Boolean flags for special categorization
*   `usage_ubers`, `usage_ou`, `usage_uu`, `usage_nu`: Usage percentages in respective Smogon tiers
*   `best_tier`: The highest competitive tier the Pokémon is used in
*   `max_usage`: The maximum usage percentage across all evaluated tiers
*   `is_ou`: Boolean flag indicating if the Pokémon has >0 usage in the OU tier
*   `formats_used_count`: The number of different Gen 4 formats the Pokémon appeared in
*   `has_two_types`: Boolean flag indicating if the Pokémon has a secondary typing

## 6. Notes on Cleaning & Transformations
*   **Name Normalization**: Pokémon names from PokéAPI and Smogon were standardized (lowercased, punctuation removed) to ensure accurate cross-referencing during the merge.
*   **Missing Tiers**: If Smogon did not publish a specific tier for the queried month, the pipeline safely defaults the usage for that tier to `0.0` for all Pokémon.
*   **Engineered Features**: Features such as `bst`, `is_ou`, `max_usage`, and `has_two_types` were engineered from the raw data to directly assist in answering the motivating question.

## 7. Link to Blog Post
A detailed blog post discussing the exploratory findings and methodology can be found here: [Link to Blog Post](#) *(Replace with actual URL upon deployment)*
