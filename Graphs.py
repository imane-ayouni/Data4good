import matplotlib.pyplot as plt
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

df.dropna(subset=["stade_developpement"], inplace = True)
print("Numéro d'arbres: ",len(df))



new_df.boxplot(column=['circonference_cm'])

plt.show()
new_df.boxplot(column=['hauteur_cm'])
plt.show()

import missingno as msno

msno.bar(new_df)
plt.show()

msno.heatmap(new_df)
plt.show()




import seaborn as sns
n_tree = [1 for i in range(len(new_df))]
new_df["n_tree"] = n_tree

new_df["arrondissement"].replace({"PARIS 10E ARRDT":"10E ARR","PARIS 11E ARRDT":"11E ARR","PARIS 12E ARRDT":"12E ARR",
                                  "PARIS 13E ARRDT":"13E ARR","PARIS 14E ARRDT":"14E ARR","PARIS 15E ARRDT":"15E ARR",
                                  "PARIS 16E ARRDT":"16E ARR","PARIS 17E ARRDT":"17E ARR","PARIS 18E ARRDT":"18E ARR",
                                  "PARIS 19E ARRDT":"19E ARR","PARIS 1ER ARRDT":"1ER ARR","PARIS 20E ARRDT":"20E ARR",
                                  "PARIS 2E ARRDT":"2E ARR","PARIS 3E ARRDT":"3E ARR","PARIS 4E ARRDT":"4E ARR",
                                  "PARIS 5E ARRDT":"5E ARR","PARIS 6E ARRDT":"6E ARR","PARIS 7E ARRDT":"7E ARR",
                                  "PARIS 8E ARRDT":"8E ARR","PARIS 9E ARRDT":"9E ARR","SEINE-SAINT-DENIS":"S.S.DENIS",
                                  "VAL-DE-MARNE":"V.MARNE","BOIS DE BOULOGNE":"B. BOULOGNE","BOIS DE VINCENNES":"B.VINCENNES",
                                  "HAUTS-DE-SEINE":"H.SEINE"}, inplace = True)
new_df_2 = new_df.groupby("arrondissement").sum()
new_df_2.drop("circonference_cm",axis =1, inplace = True)
new_df_2.drop("hauteur_cm",axis =1, inplace = True)
new_df_2.drop("geo_point_2d_a",axis =1, inplace = True)
new_df_2.drop("geo_point_2d_b",axis =1, inplace = True)


for_sns = pd.melt(new_df_2.reset_index(),id_vars=['arrondissement'],value_vars=new_df_2.columns)
p = sns.barplot(y="arrondissement",x="value", data = for_sns,hue = "variable")
p.set_title(" Nombre d'arbres par arroundissement")


plt.show()


selected_col = new_df[["arrondissement","circonference_cm","hauteur_cm"]]
new_df_3 = selected_col.copy()

ndf_3 = new_df_3.groupby("arrondissement").sum()
for_sns_2 = ndf_3.reset_index()
g = sns.scatterplot(data = for_sns_2,x = "circonference_cm",y = "hauteur_cm",hue = "arrondissement")
g.set_title("hauteur_cm et circonference_cm par arrondissement")
plt.show()



selected_col_2 = new_df[["stade_developpement","hauteur_cm"]]
new_df_4 = selected_col_2.copy()
ndf_4 = new_df_4.groupby("stade_developpement").sum()
for_sns_3 = ndf_4.reset_index()
gr = sns.lineplot(data = for_sns_3, x ="stade_developpement", y= "hauteur_cm")
gr.set_title("Hauteur_cm par stade de developpement")
plt.show()
