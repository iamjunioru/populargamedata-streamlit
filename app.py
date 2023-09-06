import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
# import seaborn as sns

# load dataset
df = pd.read_csv("games.csv")
# or 
# data_url = "csvurl"
# df = pd.read_csv(data_url)

menu = st.sidebar.radio("navigation menu:", ["home sweet home", "top 10 most popular game (by genre)", "top 10 most popular game (by year)", "content 3"])

def home():
    st.title("popular video games 1980 - 2023 🎮")
    st.dataframe(df)

def game_genre():
    st.subheader("top 10 most popular games (by genre)")
    search_genre = st.text_input("search by gender:", key="genre_input")

    #  list genre sugest
    generos_sugeridos = df["Genres"].unique()
    
    # filter
    sugestoes_filtradas = [genero for genero in generos_sugeridos if search_genre.lower() in genero.lower()]

    if not sugestoes_filtradas:
        sugestoes_filtradas = generos_sugeridos

    genero_selecionado = st.selectbox("select gender:", sugestoes_filtradas)

    top_10_genero = df[df["Genres"] == genero_selecionado].nlargest(10, "Rating")
    
    fig, ax = plt.subplots()
    ax.barh(top_10_genero["Title"], top_10_genero["Rating"],  color='black')
    ax.set_xlabel("rating")
    ax.set_ylabel("game(s)")
    ax.set_title(f"top 10 most popular games by genre {genero_selecionado}")
    
    st.pyplot(fig)
    
def game_year_popular():
    selected_year = st.slider("select year:", 1980, 2023, 2023)
    year_data = df[df['Release Date'].str.contains(str(selected_year))]
    year_data = year_data.sort_values(by='Times Listed', ascending=False).head(10)
    
    st.write(f"top 10 most popular game in {selected_year}:")
    st.table(year_data[['Title', 'Times Listed']])

def content3():
    st.write("esse marllo é bom mesmo")
    
# menu select
if menu == "home sweet home":
    home()
elif menu == "top 10 most popular game (by genre)":
    game_genre()
elif menu == "top 10 most popular game (by year)":
    game_year_popular()
  
    
# footer
# st.write("© 2023 Sistema de Apoio a Decisão")