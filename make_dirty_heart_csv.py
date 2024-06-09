import pandas as pd
import numpy as np
import random

df_with_nan = pd.read_csv("data/heart.csv")

nb_cells = df_with_nan.shape[0] * df_with_nan.shape[1]
nb_nan = int(nb_cells * 0.05)

print(f"{nb_nan = }")
for _ in range(nb_nan):
    index = random.randint(0, df_with_nan.shape[0] - 1)
    column = random.randint(0, df_with_nan.shape[1] - 1)
    # print(f"Setting NaN on {index = } & {column = }")
    df_with_nan.iloc[index, column] = np.nan

df_with_nan.to_csv("./data/heart_with_nan.csv", index=False)


new_data = {
    "age": [
        70,
        67,
        43,
        pd.Timestamp("2023-01-01"),
    ],  
    "sexe": [
        "masculin",
        "femme",
        "masculin",
        "feminin",
    ],  # La deuxieme valeur est hors categorie
    "type_douleur": ["D", "C", "BCS", "A"],  # La troisieme valeur est hors categorie
    "pression": [130.0, 115.0, 140.0, 120.0],
    "cholester": [34322.0, 564.0, 256.0, 230.0],  # La premiere valeur est absurde
    "sucre": ["A", "B", "A", "A"],
    "electro": ["C", "C", "B", "A"],
    "taux_max": [109.0, 160.0, 150.0, 170.0],
    "angine": ["non", "non", "oui", "non"],
    "depression": [8.0, 16.0, 5.0, 2.0],
    "pic": [2.0, 2.0, 1.0, 1.0],
    "vaisseau": ["D", "A", "C", "B"],
    "coeur": ["presence", "abscence", "presence", "absence"],
}
new_df = pd.DataFrame(new_data)

records = [
    {
        "age": 70,
        "sexe": "masculin",
        "type_douleur": "D",
        "pression": 130.0,
        "cholester": 34329252.0,	 			# Absurd value
        "sucre": "A",
        "electro": "C",
        "taux_max": 109.0,
        "angine": "non",
        "depression": 8.0,
        "pic": 2.0,
        "vaisseau": "D",
        "coeur": "presence",
    },
    {
        "age": 67,
        "sexe": "femme", 						# Not in category
        "type_douleur": "C",
        "pression": 115.0,
        "cholester": 564.0,
        "sucre": "B",
        "electro": "C",
        "taux_max": 160.0,
        "angine": "non",
        "depression": 16.0,
        "pic": 2.0,
        "vaisseau": "A",
        "coeur": "abscence",
    },
    {
        "age": 43,
        "sexe": "masculin",
        "type_douleur": "BCS",					# Not in category
        "pression": 140.0,
        "cholester": 256.0,
        "sucre": "A",
        "electro": "B",
        "taux_max": 150.0,
        "angine": "oui",
        "depression": 5.0,
        "pic": 1.0,
        "vaisseau": "C",
        "coeur": "presence",
    },
    {
        "age": pd.Timestamp("2023-01-01"),  	# Date instead of age
        "sexe": "feminin",
        "type_douleur": "A",
        "pression": 120.0,
        "cholester": 230.0,
        "sucre": "A",
        "electro": "A",
        "taux_max": 170.0,
        "angine": "non",
        "depression": 2.0,
        "pic": 1.0,
        "vaisseau": "B",
        "coeur": "absence",
    },
]
new_df = pd.DataFrame(records)
df_to_clean = pd.concat([df_with_nan, new_df], ignore_index=True)

df_to_clean = df_to_clean.sample(frac=1).reset_index(drop=True)
df_to_clean.to_csv("./data/heart_dirty.csv", index=False)
