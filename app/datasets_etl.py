import pandas as pd


dfnetflix = pd.read_json("datasets/netflix_titles.json")
dfamazon = pd.read_csv("datasets/amazon_prime_titles.csv")
dfdisney = pd.read_csv("datasets/disney_plus_titles.csv")
dfhulu = pd.read_csv("datasets/hulu_titles.csv")



dfnetflix["plataforma"] = "Netflix"
dfamazon["plataforma"] = "Amazon prime"
dfdisney["plataforma"] = "Disney plus"
dfhulu["plataforma"] = "Hulu"


netflix = dfnetflix[["duration","type","plataforma","release_year","listed_in","cast"]]
amazon = dfamazon[["duration","type","plataforma","release_year","listed_in","cast"]]
disneyplus = dfdisney[["duration","type","plataforma","release_year","listed_in","cast"]]
hulu = dfhulu[["duration","type","plataforma","release_year","listed_in","cast"]]


netflix.columns = ['Duración', 'Pelicula_Serie', 'Plataforma', 'Año', 'Genero', 'Actores']
amazon.columns = ['Duración', 'Pelicula_Serie', 'Plataforma', 'Año', 'Genero', 'Actores']
disneyplus.columns = ['Duración', 'Pelicula_Serie', 'Plataforma', 'Año', 'Genero', 'Actores']
hulu.columns = ['Duración', 'Pelicula_Serie', 'Plataforma', 'Año', 'Genero', 'Actores']


movies = pd.concat([netflix, amazon, disneyplus,hulu]).reset_index()
movies = movies.drop(['index'], axis=1)


movies["Duración"] = movies["Duración"].replace({"[a-zA-Z]":""}, regex=True)
movies["Duración"] = movies["Duración"].fillna(0)
movies["Duración"] = movies["Duración"].astype("int64")



#Máxima duración según tipo de film (película/serie), por plataforma y por año:
#    El request debe ser: get_max_duration(año, plataforma, [min o season])
def get_max_duration(año, plataforma, Movie_o_TV_Show):
    if (año in movies["Año"].values) and (plataforma in movies["Plataforma"].values) and (Movie_o_TV_Show in movies["Pelicula_Serie"].values):
        if Movie_o_TV_Show == "Movie":
            resultado = movies[(movies["Plataforma"] == plataforma) & (movies["Año"] == año)]["Duración"].max()
            tiempo = "minutos"
        elif Movie_o_TV_Show == "TV Show":
            resultado = movies[(movies["Plataforma"] == plataforma) & (movies["Año"] == año)]["Duración"].max()
            tiempo = "series"
        else:
            resultado = "no se encontró resultado"
        tupla = [año, plataforma, Movie_o_TV_Show, resultado]
        return print(f"En el año {tupla[0]}, la plataforma {tupla[1]} tiene una {tupla[2]} de {tupla[3]} {tiempo}")
    else: return "No se encontró resultado"



# Cantidad de películas y series (separado) por plataforma El request debe ser: get_count_plataform(plataforma)
def get_count_platform(plataforma):
    if (plataforma in movies["Plataforma"].values):
        peli = movies[(movies["Plataforma"] == plataforma) & (movies["Pelicula_Serie"] == "Movie")]["Plataforma"].count()
        series = movies[(movies["Plataforma"] == plataforma) & (movies["Pelicula_Serie"] == "TV Show")]["Plataforma"].count()
        return peli, series
    else: return None



# Cantidad de veces que se repite un género y plataforma con mayor frecuencia del mismo. El request debe ser: get_listedin('genero')
# Como ejemplo de género pueden usar 'comedy', el cuál deberia devolverles un cunt de 2099 para la plataforma de amazon.
def get_listedin(genero):
    cantidad_por_plataforma = movies[movies.listed_in.str.contains(genero.title())].groupby(['platform']).title.count().sort_values(ascending=False)
    cantidad = cantidad_por_plataforma[0]
    plataforma = cantidad_por_plataforma.index[0]
    return f"La plataforma {plataforma} es la que más veces se repite el género {genero}. Se repite {cantidad} veces"




# Actor que más se repite según plataforma y año. El request debe ser: get_actor(plataforma, año)

def get_actor(plataforma, año):
    df_func = movies.query(f"platform == '{plataforma.capitalize()}' and release_year == {año}")
    lista_actores = []
    for lista_de_listas in df_func.cast.to_list():
        lista_de_listas = lista_de_listas.replace(', ',',').split(",")
        for actor in lista_de_listas:
            lista_actores.append(actor)
    dict_ocurrencias = pd.Series(lista_actores).value_counts().to_dict()
    dict_ocurrencias.pop('Sin Dato')
    actor_2 = max(dict_ocurrencias, key=dict_ocurrencias.get)
    apariciones = dict_ocurrencias[actor_2]
    return f"El actor con más apariciones es {actor_2} con un total de {apariciones} apariciones"