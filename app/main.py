#importamos librerias a utilizar
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from datasets_etl import get_max_duration, get_count_platform, get_listedin, get_actor

#creamos FastApi
app = FastAPI()

#mensaje de bienvenida con instrucciones para iniciar /docs
@app.get('/', response_class=HTMLResponse)
async def index():
    return '''
    <html>
    <head>
    </head>
    <body>
    <h1> Proyecto Data engineer </h1>
    <h2> ingrese a "/docs" para ver la documentación </h2>
    </body>
    </html>'''

#retorna la maxima duración en minutos o temporadas de una pelicula/serie
@app.get('/get_max_duration({año}_{plataforma}_{Movie_o_TV_Show})')
async def duracion_maxima(año:int, plataforma:str, Movie_o_TV_Show:str):
    return get_max_duration(año, plataforma, Movie_o_TV_Show)

#cuenta la cantidad de series y peliculas de una plataforma
@app.get('/get_count_plataform({plataforma})')
async def cantidad_plataforma(plataforma:str):
    return get_count_platform(plataforma)

# Cantidad de veces que se repite un género y plataforma con mayor frecuencia del mismo.
@app.get('/get_listedin({genero})')
async def genero_plataforma(genero:str):
    return get_listedin(genero)

#busca el actor mas frecuente
@app.get('/get_actor({plataforma}_{anio})')
async def actor_repetido(plataforma:str, anio:int):
    return get_actor(plataforma, anio)
