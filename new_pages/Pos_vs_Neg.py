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
    df = pd.read_csv(
        path_to_data,
        index_col=0,
        encoding='latin1',
        sep=';'
        )
    df.fillna('', inplace=True)
    df['video_date'] = pd.to_datetime(df['video_date'])
    
    return df

def plot_best_worst_videos(df, columna, year):
    """
    Función que grafica los dos videos con la mayor y menor proporción positiva a negativa de comentarios en un DataFrame.

    Argumentos:
        df: un DataFrame de pandas que contiene los datos de comentarios de los videos.

    Retorno:
        No devuelve ningún valor, pero muestra el gráfico de pastel generado con matplotlib.

    """

    df = df[df['video_date'].dt.year==year]

    # Filtra los videos con menos de 1000 comentarios
    # df = df.groupby('video_title').filter(lambda x: len(x) >= 1000)

    print(df.head())

    # Calcula la proporción positiva a negativa de comentarios para cada video
    video_sentiment = df.groupby('video_title')[columna].value_counts(normalize=True).unstack().fillna(0)

    print(video_sentiment.head())

    video_sentiment['ratio'] = video_sentiment['Positivo'] / video_sentiment['Negativo']
    
    # Check if any video has no negative comments
    has_no_negative = (video_sentiment['Negativo'] == 0).any()
    
    if has_no_negative:
        # Select the video with the highest positive-to-negative ratio that has at least one negative comment
        video_sentiment_filtered = video_sentiment[video_sentiment['Negativo'] > 0]
        best_video = video_sentiment_filtered['ratio'].idxmax()
        worst_video = video_sentiment_filtered['ratio'].idxmin()
    else:
        # Select the videos with the highest and lowest positive-to-negative ratios
        best_video = video_sentiment['ratio'].idxmax()
        worst_video = video_sentiment['ratio'].idxmin()
    
    best_ratio = video_sentiment.loc[best_video, 'ratio']
    worst_ratio = video_sentiment.loc[worst_video, 'ratio']

    # Filtra los comentarios de los dos videos seleccionados
    best_comments = df[df['video_title'] == best_video]
    worst_comments = df[df['video_title'] == worst_video]

    # Configuración de los colores
    colors = ['#3CB371', '#4169E1', '#FF6347']
    labels = ['Positivo', 'Neutro', 'Negativo']

    # Grafica la distribución de sentimientos de los dos videos con pastel
    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(14, 6))
    plt.suptitle(f"Mejor y peor video (proporción pos/neg: {best_ratio:.2f} / {worst_ratio:.2f})", fontsize=16)
    
    # Grafica pastel para el mejor video
    best_data = best_comments[columna].value_counts(normalize=True)
    ax1.pie(best_data, colors=colors, startangle=90, autopct='%1.1f%%', labels=labels)
    ax1.set_title(f"Mejor video: {best_video}")
    
    # Grafica pastel para el peor video
    worst_data = worst_comments[columna].value_counts(normalize=True)
    ax2.pie(worst_data, colors=colors, startangle=90, autopct='%1.1f%%', labels=labels)
    ax2.set_title(f"Peor video: {worst_video}")

    return fig

###########################################
# Instanciación de objetos
###########################################

# Carga los datos
COMENTARIOS_XL = 'Comentarios_clasificados_fine-tuned-FreeCover(v2).csv'
CARPETA_ASSETS = 'Assets'
path = os.path.join(CARPETA_ASSETS, COMENTARIOS_XL)
comments_df = load_data(path)

###########################################
# Creación de la página
###########################################

def show_pos_vs_neg():

    st.title('Relación de comentarios positivos vs negativos :smiley: vs :slightly_frowning_face:')

    st.markdown(
        """
        Una característica interesante de observar sería la relación entre la cantidad de comentarios positivos 
        a negativos, por lo que de nuevo nos vamos a apoyar en una visualización. Está vez será una gráfica de torta, 
        que nos muestre dicha relación, la cual vamos a obtener al dividir la cantidad de comentarios positivos sobre 
        los negativos de los videos, y finalmente, graficaremos el video con la mejor, y la peor relación.
        """
    )

    with st.expander(
        "Instrucciones", expanded=False
    ):
        st.write("")
        st.markdown("""
            * Elije el año para ver la relación de comentarios positivos a negativos de dicho año.
            """)
        
    years = comments_df['video_date'].dt.year.unique().tolist()
    years = sorted(years)
    year = st.selectbox('Selecciona el año', years)

    fig = plot_best_worst_videos(comments_df, columna='fine-tuned_label', year=year)

    st.pyplot(
        fig,
        use_container_width=True
        )