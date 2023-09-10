import streamlit as st
import pandas as pd
import os

from wordcloud import WordCloud
from nltk.corpus import stopwords

import matplotlib.pyplot as plt
import matplotlib as mpl

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
def create_wordcloud(
    df,
    column_name,
    stop_words=None,
    max_words_to_show=60,
    video='[Free Cover] Billos Caracas Boys - Rafael Pollo Brito'
    ):
    """
    La función create_wordcloud crea una nube de palabras a partir del texto de una columna de un DataFrame de pandas.

    Argumentos:

        df: un DataFrame de pandas que contiene los datos de texto.
        column_name: el nombre de la columna que contiene el texto.
        stop_words (opcional): una lista de palabras a excluir de la nube de palabras.

    Retorno:

        No devuelve ningún valor, pero muestra la nube de palabras generada con matplotlib.
    """

    # Combine all the text from the selected column into a single string
    if video == 'Todos':
        df = df
    else:
        df = df[df['video_title']==video]
    
    text = ' '.join(df[column_name].astype(str))

    # Create a wordcloud from the text
    wordcloud = WordCloud(
        background_color='black',
        width=800,
        height=600,
        colormap=mpl.colormaps['rainbow'],
        max_words=max_words_to_show,
        collocations=False,
        stopwords=stop_words
    ).generate(text)

    # Display the wordcloud
    plt.figure(figsize=(20,15))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.tight_layout(pad = 0)
    plt.savefig('image.png')

    return

###########################################
# Instanciación de objetos
###########################################

# Carga los datos
COMENTARIOS_XL = 'Comentarios-FreeCover(date_fixed).xlsx'
CARPETA_ASSETS = 'Assets'
path = os.path.join(CARPETA_ASSETS, COMENTARIOS_XL)
comments_df = load_data(path)
esp_stop = stopwords.words('spanish')
esp_stop = esp_stop + ['si','va','ahora','hace', 'cover', 'free', 'gracia']

###########################################
# Creación de la página
###########################################

def show_wordcloud():

    st.title('Wordcloud :cloud:')

    st.markdown(
        """
        Las __wordclouds__ son una visualización muy famosa que muestra las palabras más utilizadas
        en un corpus de texto.
        """
    )


    with st.expander(
        "Instrucciones", expanded=False
    ):
        st.write("")
        st.markdown("""
            * Elije un video para ver su wordcloud.
            * También puedes escribir el nombre del artista para buscar más rápido su video.
            * Elije una cantidad de palabras para mostrar deslizando el "slider".
    """)
        
    videos = comments_df['video_title'].unique().tolist()
    wordcloud_video = st.selectbox('Elije el video para generar el wordcloud',  videos + ['Todos'])

    max_words = st.slider('Elije la cantidad máxima de palabras', 20, 80)

    create_wordcloud(
        comments_df,
        'comment_text',
        stop_words=esp_stop,
        max_words_to_show=max_words,
        video=wordcloud_video,
        )
    
    st.image(
        'image.png',
        )