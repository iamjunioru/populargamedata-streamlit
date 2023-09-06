import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from curr_time import current_time

########
# func #
########


def true_home():
    st.title("hello. :)")
    user_name = st.text_input("pls enter your nickname:", key="user_name_input")

    if st.button("⚔️"):
        st.balloons()

    if user_name:
        current_hour = int(current_time.split(" ")[-1].split(":")[0])

        if 5 <= current_hour  < 12:
            st.subheader(f"hey, {user_name}, good day! welcome to popular games data.")
            
        elif 12 <= current_hour < 18:
            st.subheader(f"hey, {user_name}, good afternoon! welcome to popular games data.")
        else:
             st.subheader(f'"hey, {user_name}! welcome and good night.')
             st.write('your journey has been a long one... rest a while before proceeding..."')
             st.image("https://i.gifer.com/43Qz.gif", width=500)

def home(df):
    st.title("popular video games 1980 - 2023 🎮")
    st.markdown(
        """
this dataset contains a list of video games dating from 1980 to 2023, it also provides things such as release dates, user review rating, and critic review rating.
"""
    )
    st.dataframe(df)


def game_genre(df):
    st.subheader("top 10 most popular games (by genre)")
    search_genre = st.text_input("search by gender:", key="genre_input")

    #  list genre sugest
    generos_sugeridos = df["Genres"].unique()

    # filter
    sugestoes_filtradas = [
        genero for genero in generos_sugeridos if search_genre.lower() in genero.lower()
    ]

    if not sugestoes_filtradas:
        sugestoes_filtradas = generos_sugeridos

    genero_selecionado = st.selectbox("select gender:", sugestoes_filtradas)

    top_10_genero = df[df["Genres"] == genero_selecionado].nlargest(10, "Rating")

    fig, ax = plt.subplots()
    ax.barh(top_10_genero["Title"], top_10_genero["Rating"], color="black")
    ax.set_xlabel("rating")
    ax.set_ylabel("game(s)")
    ax.set_title(f"top 10 most popular games by genre {genero_selecionado}")

    st.pyplot(fig)


def game_year_popular(df):
    selected_year = st.slider("select year:", 1980, 2023, 2001)
    year_data = df[df["Release Date"].str.contains(str(selected_year))]
    year_data = year_data.sort_values(by="Times Listed", ascending=False).head(10)

    st.write(f"top 10 most popular game in {selected_year}:")
    st.table(year_data[["Title", "Times Listed"]])


def games_by_developer(df):
    st.subheader("top 10 most popular games (by developer)")
    search_developer = (
        st.text_input("search by developers:", key="developer_input").strip().lower()
    )

    developers = df["Team"].unique()

    developers_filtrados = [
        dev for dev in developers if search_developer in str(dev).lower()
    ]

    if not developers_filtrados and search_developer:
        st.warning("no developers found. showing all available developers.")
        developers_filtrados = developers

    selected_developer = st.selectbox("select a developer:", developers_filtrados)

    top_10_developer_games = df[
        df["Team"].str.lower() == str(selected_developer).lower()
    ].nlargest(10, "Rating")

    st.table(top_10_developer_games[["Title", "Rating"]])


def more_rated(df):
    st.subheader("the 10 more rated games")

    # convert to numeric >
    df["Number of Reviews"] = pd.to_numeric(df["Number of Reviews"], errors="coerce")

    top_10_avaliados = df.nlargest(10, "Number of Reviews")

    st.table(top_10_avaliados[["Title", "Number of Reviews"]])


def best_rated(df):
    st.subheader("the 10 best rated games")

    top_10_avaliados = df.nlargest(10, "Rating")

    st.table(top_10_avaliados[["Title", "Rating"]])


def best_rated_by_year(df):
    st.subheader("the 10 best rated games by year")

    selected_year = st.slider("select year:", 1980, 2023, 2001)
    year_data = df[df["Release Date"].str.contains(str(selected_year))]
    top_10_avaliados_por_ano = year_data.nlargest(10, "Rating")

    st.table(top_10_avaliados_por_ano[["Title", "Rating"]])


def released_by_year(df):
    st.subheader("number of games released in year")

    # games by year count
    games_by_year = (
        df["Release Date"]
        .str.extract(r"(\d{4})")
        .rename(columns={0: "Year"})
        .groupby("Year")
        .size()
        .reset_index(name="Count")
    )

    st.bar_chart(games_by_year.set_index("Year"), use_container_width=True)


def content8():
    st.write("content 8")


def content9():
    st.write("content 9")


def content10():
    st.write("content 10")
