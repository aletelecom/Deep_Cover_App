import streamlit as st
import pandas as pd
import numpy as np
import os

import matplotlib.cm as cm
# import plotly.graph_objects as go
# from plotly.graph_objs import Figure

###########################################
# Definición de funciones varias
###########################################

@st.cache_resource
def load_data(path_to_data):
    # Función que permite la carga de los datos.
    # Tiene un decorador que permite dejar los datos en cache
    df = pd.read_csv(path_to_data, index_col=0, encoding='latin1', sep=';')
    df.fillna('', inplace=True)

    return df


###########################################
# Instanciación de objetos
###########################################

# Carga los datos
COMENTARIOS_CSV = 'Comentarios_clasificados_fine-tuned-FreeCover(v2).csv'
CARPETA_ASSETS = 'Assets'
path = os.path.join(CARPETA_ASSETS, COMENTARIOS_CSV)
comments_df = load_data(path)

###########################################
# Creación de la página
###########################################

def show_datos_crudos():

    st.title('Datos "crudos" :floppy_disk:')

    st.markdown(
        """
        Los datos fueron obtenidos directamente desde las secciones de comentarios de cada video de Youtube. Esto lo hice a través
        de la API de Youtube, lo que me ayudó a recolectar más de 70 mil comentarios individuales de varios videos (hasta febrero 2023).
        
        Para más tecnicalidades puedes ir a la sección de información de la app.

        Los datos fueron guardados en un archivo MS CSV, con las siguientes caracteristicas:

        * Cada fila es una agrupación gaitera.
        * Hay seis columnas:
            - __video_id__, que contiene el identificador único asignado por Youtube a cada video.
            - __video_title__, que contiene el título de cada video como aparece en Youtube.
            - __video_date__, que contiene la fecha, y la hora en la que fue subido cada video a Youtube.
            - __comment_text__, que contiene el texto de cada comentario como fue escrito por el usuario.
            - __comment_date__, que contiene la fecha y la hora del comentario.
            - Tres columnas con las etiquetas de clasifiación del comentario asignadas por diferentes modelos de 
            lenguaje natural, o manuales.

            Para más detalle sobre los datos consultar la sección de Información.
        """
    )

    with st.expander(
        "Instrucciones", expanded=False
    ):
        st.write("")
        st.markdown("""
            * Puedes mover la tabla, y expandir las columnas que quieras para ver su contenido.
    """)


    st.dataframe(comments_df)

