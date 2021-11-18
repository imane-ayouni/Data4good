import pandas as pd

df = pd.read_csv(r'C:\Users\imane\OneDrive\Desktop\Data4good\p2-arbres-fr.csv', sep =";", encoding = "utf-8")
df.drop('id', axis = 1, inplace= True)
df.drop("complement_addresse",axis =1, inplace = True)
df.drop("numero",axis =1, inplace = True)
df.drop("id_emplacement",axis =1, inplace = True)
df.drop("genre",axis =1, inplace = True)
df.drop("variete",axis =1, inplace = True)
df.drop("remarquable",axis =1, inplace = True)
print(df)



