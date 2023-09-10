import streamlit as st
import pandas as pd
import seaborn as sns
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
    return df

@st.cache_data
def plot_comments_per_video(df, year):
    df = df[df['video_date'].dt.year==year]
    grouped = df.groupby('video_title').count()['comment_text']
    # Ordene el DataFrame agrupado en orden descendente según la cantidad de comentarios
    sorted_df = grouped.sort_values(ascending=False)

    # Selecciona los 5 mejores videos con más comentarios
    top_5 = sorted_df[:5]

    # Establecer una paleta de colores personalizada para las barras
    colors = sns.color_palette('Set2', len(top_5))

    fig, ax = plt.subplots(figsize=(12,6))

    # Cree un gráfico de barras usando la biblioteca seaborn con los 5 mejores videos seleccionados y su respectivo número de comentarios
    sns.barplot(x=[i for i in range(top_5.shape[0])], y=top_5, ax=ax)
    ax.set_title(f'Top 5 Videos con más comentarios de {year}')
    ax.set_ylabel('Cantidad de comentarios')
    ax.set_xticklabels([])

    return fig, pd.DataFrame(top_5)


###########################################
# Instanciación de objetos
###########################################

# Carga los datos
COMENTARIOS_CSV = 'Comentarios-FreeCover(date_fixed).xlsx'
CARPETA_ASSETS = 'Assets'
path = os.path.join(CARPETA_ASSETS, COMENTARIOS_CSV)
comments_df = load_data(path)

###########################################
# Creación de la página
###########################################

def show_top_5():

    st.title('Top 5 videos con más comentarios :first_place_medal:')

    st.markdown(
        """
        Aquí podemos ver el top 5 de videos que contienen más comentarios.
        """
    )


    with st.expander(
        "Instrucciones", expanded=False
    ):
        st.write("")
        st.markdown("""
            * Elije el año para ver el top 5 de videos con más comentarios.
            * Puedes ver los nombres ordenados de mayor a menor de los videos debajo de la imágen.
            * También puedes escribir el nombre del artista para buscar más rápido su video.
    """)
        
    years = comments_df['video_date'].dt.year.unique().tolist()
    years = sorted(years)
    year = st.selectbox('Selecciona el año', years)

    # Publica la imágen en la app
    fig, top_5 = plot_comments_per_video(comments_df, year)
    st.pyplot(fig, use_container_width=True)
    for i, row, number in zip(range(top_5.shape[0]), top_5.index, top_5.values):
        st.markdown(f"{i+1} - {row} con: {number[0]} comentarios")