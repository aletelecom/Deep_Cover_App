import streamlit as st
import pandas as pd
import numpy as np
import os

import matplotlib.pyplot as plt

###########################################
# Definición de funciones varias
###########################################

@st.cache_resource
def load_data(path_to_data):
    # Función que permite la carga de los datos.
    # Tiene un decorador que permite dejar los datos en cache
    df = pd.read_excel(path_to_data, index_col=0)
    df.fillna('', inplace=True)
    df['video_date'] = pd.to_datetime(df['video_date'])
    df['comment_date'] = pd.to_datetime(df['comment_date'])

    return df

@st.cache_data
def create_heatmap(df, column_name='comment_date', video='[Free Cover] Billos Caracas Boys - Rafael Pollo Brito'):

    """
    La función create_heatmap crea un mapa de calor que muestra la distribución de los comentarios de YouTube por día de la semana y hora del día en un canal determinado.

        Argumentos:

            df: un DataFrame de pandas que contiene los datos de comentarios de YouTube.
            column_name: el nombre de la columna que contiene la fecha y hora de cada comentario.

        Retorno:

            No devuelve ningún valor, pero muestra el mapa de calor generado con matplotlib.
    """

    # Convierta la columna de fecha a fecha y hora
    if video == 'Todos':
        df = df
    else:
        df = df[df['video_title']==video]

    # Crea una tabla dinámica con el número de comentarios por día de la semana y hora del día
    pivot_table = df.pivot_table(index=df[column_name].dt.dayofweek, columns=df[column_name].dt.hour, aggfunc='size', fill_value=0)

    # Defina las etiquetas para los ejes x e y
    weekdays = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
    hours = np.arange(0, 24)

    # Crear la trama del mapa de calor
    fig, ax = plt.subplots(figsize=(15, 10))  # adjust the figsize parameter to your liking
    im = ax.imshow(pivot_table, cmap='YlOrRd')

    # Establecer las etiquetas de marca para el eje x
    ax.set_xticks(hours)
    ax.set_xticklabels([f'{h:02}:00' for h in hours], rotation=45, ha='right')

    # Establecer las etiquetas de marca para el eje y
    ax.set_yticks(np.arange(len(weekdays)))
    ax.set_yticklabels(weekdays)

    # Añade la barra de colores
    cbar = ax.figure.colorbar(im, ax=ax, orientation='horizontal')
    cbar.ax.set_xlabel("Cantidad de comentarios")

    # Establecer el título y las etiquetas de la trama
    ax.set_title(f"Distribución semanal y horaria en {video}")
    ax.set_xlabel("Hora del día")
    ax.set_ylabel("Día de la semana")

    # Devuelve la visualización
    return fig

###########################################
# Instanciación de objetos
###########################################

# Carga los datos
COMENTARIOS_XL = 'Comentarios-FreeCover(date_fixed).xlsx'
CARPETA_ASSETS = 'Assets'
path = os.path.join(CARPETA_ASSETS, COMENTARIOS_XL)
comments_df = load_data(path)

###########################################
# Creación de la página
###########################################

def show_heatmap():

    st.title('Mapa de calor de comentarios :world_map:')

    st.markdown(
        """
        Los mapas de calor son una herramienta útil para visualizar la frecuencia de los comentarios en diferentes 
        momentos de la semana y del día (filas horizontales los días de la semana, y columnas verticales las horas del día), 
        dicha frecuencia se codifica en el color del mapa, siendo un color blanco o amarillo para cuando la densidad de comentarios 
        es baja, y rojo, cuando es alta. A través de estas visualizaciones, podremos entender mejor cuándo los usuarios son más 
        activos en la comunidad __Free Cover Venezuela__.
        """
    )

    with st.expander(
        "Instrucciones", expanded=False
    ):
        st.write("")
        st.markdown("""
            * Elije un video para ver su mapa de calor.
            * Puedes elegir la opción "Todos", que te permitirá incluir todos los videos.
            * También puedes escribir el nombre del artista para buscar más rápido su video.
    """)
        
    videos = comments_df['video_title'].unique().tolist()
    vide_index = videos.index('[Free Cover] Billos Caracas Boys - Rafael Pollo Brito')
    heat_video = st.selectbox('Elije el video para generar el wordcloud',  videos + ['Todos'], index=vide_index)

    fig = create_heatmap(comments_df, video=heat_video)

    st.pyplot(
        fig,
        use_container_width=True
        )