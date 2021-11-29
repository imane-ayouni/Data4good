import pandas as pd
import dash
from dash import html
from dash import dcc
import plotly.express as px
import folium

df = pd.read_csv(r'C:\Users\imane\OneDrive\Desktop\Data4good\p2-arbres-fr.csv', sep =";", encoding = "utf-8")
df.drop('id', axis = 1, inplace= True)
df.drop("complement_addresse",axis =1, inplace = True)
df.drop("numero",axis =1, inplace = True)
df.drop("id_emplacement",axis =1, inplace = True)
df.drop("genre",axis =1, inplace = True)
df.drop("variete",axis =1, inplace = True)
df.drop("remarquable",axis =1, inplace = True)
df.drop("type_emplacement",axis =1, inplace = True)

df.drop(df.index[(df["circonference_cm"] == 0)], axis = 0, inplace=True)
df.drop(df.index[(df["hauteur_m"] == 0)], axis = 0, inplace=True)
df.drop(df.index[(df["circonference_cm"] > 470)], axis = 0, inplace=True)
df.drop(df.index[(df["hauteur_m"] > 35 )], axis = 0, inplace=True)
df.dropna(subset=["circonference_cm"],inplace=True)
df.dropna(subset=["hauteur_m"],inplace=True)
df.dropna(subset=["stade_developpement"], inplace = True)

df["hauteur_m"] = 100 * df["hauteur_m"]

new_df = df.rename(columns={"hauteur_m":"hauteur_cm"})


boxplot_cir = px.box(new_df, y = "circonference_cm")
boxplot_hau = px.box(new_df, y = "hauteur_cm")


heatmap = px.imshow(new_df.isnull())

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

selected_bar = new_df[["arrondissement","n_tree"]]
df_bar = selected_bar.copy()
new_df_2 = df_bar.groupby("arrondissement").sum().reset_index()
bar_plot = px.bar(new_df_2, x="n_tree", y="arrondissement")


selected_scatter = new_df[["arrondissement","circonference_cm","hauteur_cm"]]
df_scatter = selected_scatter.copy()
new_df_3 = df_scatter.groupby("arrondissement").mean().reset_index()
scatter_plot = px.scatter(new_df_3, x = "circonference_cm", y = "hauteur_cm", color = "arrondissement" )


selected_line = new_df[["stade_developpement","hauteur_cm","circonference_cm"]]
df_line = selected_line.copy()
new_df_4 = df_line.groupby("stade_developpement").mean().reset_index()
line_plot = px.line(new_df_4, x = "stade_developpement", y = ["hauteur_cm","circonference_cm"] )


selected_stacked = new_df[["stade_developpement","n_tree","arrondissement"]]
df_stacked = selected_stacked.copy()
new_df_5 = df_stacked.groupby(["arrondissement","stade_developpement"]).sum().reset_index()
stacked_plot = px.bar(new_df_5, x ="arrondissement", y = "n_tree", color="stade_developpement", barmode="stack")


selected_treemap = new_df[["n_tree","domanialite","arrondissement"]]
df_treemap = selected_treemap.copy()
new_df_6 = df_treemap.groupby(["domanialite","arrondissement"]).sum().reset_index()
treemap = px.treemap(new_df_6,path = ["domanialite","arrondissement"], values="n_tree")


selected_map = new_df[["arrondissement", "n_tree", "geo_point_2d_a", "geo_point_2d_b"]]
df_map = selected_map.copy()
new_df_7 = df_map.groupby("arrondissement").sum().reset_index()
new_df_7.drop('geo_point_2d_a', axis=1, inplace=True)
new_df_7.drop('geo_point_2d_b', axis=1, inplace=True)
positions = df_map.groupby(["arrondissement"]).nth(0).reset_index()
a = positions["geo_point_2d_a"]
b = positions["geo_point_2d_b"]
new_df_7 = new_df_7.join(a)
new_df_7 = new_df_7.join(b)

map = folium.Map(location=[48.856614, 2.3522219], zoom_start=14, control_scale=True, tiles="Stamen Terrain")
for i in range(0, len(new_df_7)):
    folium.Circle(
        location=[new_df_7.iloc[i]["geo_point_2d_a"], new_df_7.iloc[i]["geo_point_2d_b"]],
        tooltip=(new_df_7.iloc[i]["arrondissement"], new_df_7.iloc[i]["n_tree"]),
        radius=int(new_df_7.iloc[i]["n_tree"]) / len(new_df_7), fill=True,

    ).add_to(map)

map.save("Paris_map.html")


app = dash.Dash(__name__)
app.layout = html.Div(children=[html.H1(children="Distribution des arbres à Paris"),
                                html.Div(children="Circonference_cm Boxplot"),
                                dcc.Graph(
                                    id = "cir boxplot",
                                    figure= boxplot_cir
                                ),
                                html.Div(children="Hauteur_cm Boxplot"),
                                dcc.Graph(
                                    id = "hau boxplot",
                                    figure= boxplot_hau
                                ),
                                html.Div(children="Valeures manquantes"),
                                dcc.Graph(
                                    id = "empty value",
                                    figure= heatmap
                                ),
                                html.Div(children="Nombre d'arbres par arrondissement"),
                                dcc.Graph(
                                    id = "arbres/arr",
                                    figure= bar_plot
                                ),
                                html.Div(children="Hauteur et circonference moyenne par arrondissement"),
                                dcc.Graph(
                                    id = "hauteur-circ/arr",
                                    figure= scatter_plot
                                ),
                                html.Div(children="Hauteur et circonference moyenne par stade de developpement"),
                                dcc.Graph(
                                    id = "hauteur-circ/stade_dev",
                                    figure= line_plot
                                ),
                                html.Div(children="Nombre d'arbres par arrondissement et stade de developpement"),
                                dcc.Graph(
                                    id = "arbres/arr/stade_dev",
                                    figure= stacked_plot
                                ),
                                html.Div(children="Nombre d'arbres par arrondissement et domanialite"),
                                dcc.Graph(
                                    id = "arbres/arr/domanialite",
                                    figure= treemap
                                ),
                                html.Div(children="Carte : nombre d'arbres par arrondissement"),
                                html.Iframe(
                                    id = "Paris_map",
                                srcDoc=open("Paris_map.html", 'r').read(),
                                width='75%',
                                height='500'
                                ),

                                ])
if __name__ == '__main__':
    app.run_server(debug=True)

