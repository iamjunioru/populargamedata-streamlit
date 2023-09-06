import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
# import seaborn as sns

# load dataset
df = pd.read_csv("games.csv")
# or 
# data_url = "csvurl"
# df = pd.read_csv(data_url)

menu = st.sidebar.radio("navigation menu", ["home", "top 10 most popular (game genre)", "content 2"])

def home():
    st.title("popular video games 1980 - 2023 🎮")
    st.dataframe(df)

def game_genre():
    st.subheader("top 10 most popular (game genre)")

    genero_selecionado = st.selectbox("game genre:", df["Genres"].unique())
    top_10_genero = df[df["Genres"] == genero_selecionado].nlargest(10, "Rating")
    
    fig, ax = plt.subplots()
    ax.barh(top_10_genero["Title"], top_10_genero["Rating"])
    ax.set_xlabel("rating")
    ax.set_ylabel("games")
    ax.set_title(f"the 10 most popular {genero_selecionado}")
    
    st.pyplot(fig)
    
def content2():
    st.write("esse marllo é bom mesmo")
    
# menu select
if menu == "home":
    home()
elif menu == "content 1":
    game_genre()
elif menu == "content 2":
    content2()
  
    
# footer
# st.write("© 2023 Sistema de Apoio a Decisão")