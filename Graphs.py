import pandas as pd

df = pd.read_csv(r'C:\Users\imane\OneDrive\Desktop\Data4good\p2-arbres-fr.csv', sep =";", encoding = "utf-8")
df.drop('id', axis = 1, inplace= True)
df.drop("complement_addresse",axis =1, inplace = True)
df.drop("numero",axis =1, inplace = True)
df.drop("id_emplacement",axis =1, inplace = True)
df.drop("genre",axis =1, inplace = True)
df.drop("variete",axis =1, inplace = True)
df.drop("remarquable",axis =1, inplace = True)
df.drop("type_emplacement",axis =1, inplace = True)
print(df)
print("Numéro d'arbres: ",len(df))

df.drop(df.index[(df["circonference_cm"] == 0)], axis = 0, inplace=True)
df.drop(df.index[(df["hauteur_m"] == 0)], axis = 0, inplace=True)
df.drop(df.index[(df["circonference_cm"] > 470)], axis = 0, inplace=True)
df.drop(df.index[(df["hauteur_m"] > 35 )], axis = 0, inplace=True)
df.dropna(subset=["circonference_cm"],inplace=True)
df.dropna(subset=["hauteur_m"],inplace=True)

print("Numéro d'arbres: ",len(df))

df["hauteur_m"] = 100 * df["hauteur_m"]

new_df = df.rename(columns={"hauteur_m":"hauteur_cm"})

print(new_df)
