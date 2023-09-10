import streamlit as st

import nltk
nltk.download('stopwords')


st.set_page_config(
    page_title='Deep Cover',
    page_icon=':musical_score:',
)

from new_pages.Top_5_videos import show_top_5
from new_pages.Word_cloud import show_wordcloud
from new_pages.Heatmap_video import show_heatmap
from new_pages.Datos_crudos import show_datos_crudos
from new_pages.Sentiment_analysis import show_sentiment_dist
from new_pages.Pos_vs_Neg import show_pos_vs_neg


###########################################
# Creación de la página
###########################################

st.write("# !Bienvenidos a Deep Cover Venezuela! :flag-ve:")

st.write('Algunos gráficos pueden tardar un poco en mostrarse.')

pages = [
    'Home',
    'Top 5 videos',
    'Wordcloud',
    'Mapa de calor',
    'Distribución de sentimientos',
    'Relación POS vs NEG',
    'Datos crudos',
    # 'Información',
    ]
page_to_show = st.selectbox('Seleccione la página a mostrar', pages)

def home_page():
    st.markdown(
        """
        Deep Cover busca mostrar de forma interactiva varios datos intereantes sobre los comentarios hechos en los videos del canal
        de Youtube __Free Cover Venezuela__.

        Estos datos interesantes van desde curiosidades como:

        * ¿Cuales son las horas preferidas por los usuarios para comentar?
        * ¿Cuales son los videos con la peor relación de comentarios buenos vs comentarios malos?
        * ¿Cuales son las palabras más utilizadas en un video especifico?

        Y varios otros...
        
        !Así que los invito a explorar esta app!
        """
    )
    
def info_page():
    st.markdown(
            """
            ## Tecnicalidades


            Deep Cover fue un estudio con el que busqué analizar los comentarios de los videos del canal __Free Cover Venezuela__ en YouTube para 
            obtener información valiosa que ayude a entender mejor la interacción de la audiencia en la sección de comentarios de Youtube.

            Si deseas conocer las técnicas, pasos, y procesos de como se realizó el estudio puedes visitar el repositorio Github del mismo:

            [Free Cover Venezuela repo](https://github.com/aletelecom/FreeCover-Project/tree/master)

            ## Los datos

            Los datos utilizados en el proyecto son los comentarios publicados por las personas en los videos del canal de Youtube de Free Cover, 
            los cuales fueron extraidos utilizando la API de Google para este propósito.
            Son poco más de 85 mil comentarios sin filtrar los que fueron extraídos, y los que utilizaremos.

            ## Free Cover Venezuela

            Free Cover Venezuela son un grupo de jovenes músicos que tienen un canal de Youtube de videos musicales. Son muy famosos, y 
            queridos en Venezuela. 
            
            Puedes visitar su canal de Youtube:

            [Free Cover Venezueña](https://www.youtube.com/@FreeCoverVenezuela) 

            ## Mi relación con FCV

            Este estudio es un homenaje de mi parte hacia los chicos(as) de FCV. No tengo ningún tipo de relación con ellos.

            ## Contacto

            Si deseas colaborar en esta tarea no dudes en contactarme:

            aletelecom.medina@gmail.com
        """
    )


if page_to_show == 'Home':
    home_page()

elif page_to_show == 'Top 5 videos':
    show_top_5()

elif page_to_show == 'Wordcloud':
    show_wordcloud()

elif page_to_show == 'Mapa de calor':
    show_heatmap()

elif page_to_show == 'Distribución de sentimientos':
    show_sentiment_dist()

elif page_to_show == 'Relación POS vs NEG':
    show_pos_vs_neg()

elif page_to_show == 'Datos crudos':
    show_datos_crudos()

elif page_to_show == 'Información':
    info_page()

else:
    home_page()