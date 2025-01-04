import streamlit as st
import pandas as pd

st.set_page_config (

layout= "wide",
page_title= "spotify songs"

)

# Carregar o arquivo CSV
df = pd.read_csv("01 Spotify.csv")

df.set_index ("Track", inplace=True)

artists = df["Artist"].value_counts().index


artists= st.selectbox ("Artista",artists)

df_filtered = df[df["Artist"] == artists]


display = st.checkbox("Display")

if display:
    
    st.bar_chart(df_filtered["Stream"])
    
    st.write("Engineer IA- Francisco Ferreira de Araújo")



# Exibir o DataFrame no Streamlit
st.write(df)

# Adicionar um botão para download
@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

csv = convert_df(df)

st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name='spotify_data.csv',
    mime='text/csv',
)
