import streamlit as st
import pandas as pd
import os
import seaborn as sns

import matplotlib.ticker as ticker

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

def plot_sentiment_analysis(df, columna, video):
    """
    La función plot_sentiment_analysis grafica la distribución de sentimientos en un DataFrame utilizando seaborn.

    Argumentos:

        df: un DataFrame de pandas que contiene los datos de análisis de sentimiento.

    Retorno:

        No devuelve ningún valor, pero muestra el gráfico de barras generado con matplotlib y seaborn.
    """

    # Definir el orden de las categorías para el eje x
    sentimiento_order = ['Positivo', 'Neutro', 'Negativo']
    if video == 'Todos':
        df = df
    else:
        df = df[df['video_title']==video]

    # Plot a bar chart of the sentiment distribution
    fig, ax = plt.subplots(figsize=(12,5))
    sns.set_style('whitegrid')
    sns.countplot(data=df, x=columna, palette="hsv", order=sentimiento_order, ax=ax)
    ax.set_title("Distribución de sentimiento")
    ax.set_xlabel("Sentimiento")
    ax.set_ylabel("Conteo")
    plt.xticks(rotation=45, ha='right')

    # Formatea los valores del eje "Y" para que tenga separador de "miles"
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

    # Add labels to the bars
    for p in ax.patches:
        ax.annotate(
            format(p.get_height(), ','),
            (p.get_x() + p.get_width() / 2., p.get_height()),
            ha = 'center', va = 'center', xytext = (0, 10),
            textcoords = 'offset points'
            )
        
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

def show_sentiment_dist():

    st.title('Distribuición de sentimiento :smiley:')

    st.markdown(
        """
        En el análisis de sentimientos, comprender la distribución de los diferentes sentimientos en un conjunto de datos es fundamental 
        para obtener información valiosa. Una forma efectiva de visualizar esta distribución es a través de gráficos claros y concisos. 
        En esta sección, exploraremos una visualización de la distribución de sentimientos utilizando un gráfico de barras:
        """
    )

    with st.expander(
        "Instrucciones", expanded=False
    ):
        st.write("")
        st.markdown("""
            * Elije un video para ver su distribución de sentimientos.
    """)
        
    videos = comments_df['video_title'].unique().tolist()
    vide_index = videos.index('[Free Cover] Billos Caracas Boys - Rafael Pollo Brito')
    dist_video = st.selectbox('Elije el video para generar el wordcloud',  videos + ['Todos'], index=vide_index)


    fig = plot_sentiment_analysis(comments_df, columna='fine-tuned_label', video=dist_video)

    st.pyplot(
        fig,
        use_container_width=True
        )