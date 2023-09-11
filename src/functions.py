import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from curr_time import current_time
from sidebar_state import toggle_sidebar_state
from time import sleep
import ast

########
# func #
########


def true_home():
    new_bg_color = "#0E042A"
    st.markdown(
            f"""
            <style>
            .stApp {{
                background-color: {new_bg_color};
            }}
            </style>
            """,
            unsafe_allow_html=True,
        )
    st.markdown("<h1 style='text-align: center; color: white; font-size: 40px; font-family: 'Courier New'>welcome. :)</h1>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: left; color: white; font-size: 20px; font-family: 'Courier New''>{populargamedata}.</h1>", unsafe_allow_html=True)
    user_name = st.text_input("please enter your nickname bellow:", key="user_name_input")

    if st.button("⚔️"):
        st.toast("✅ congratulations! you have unlocked a new achievement: welcome. ")
        new_bg_color = "#370BB4"
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-color: {new_bg_color};
                transition: background-color 1s;
            }}
            </style>
            """,
            unsafe_allow_html=True,
        )


    if user_name:
        current_hour = int(current_time.split(" ")[-1].split(":")[0])

        if 5 <= current_hour  < 12:
            toggle_sidebar_state()
            st.subheader(f"hey, {user_name}, good day! welcome to popular games data.")
            
        elif 12 <= current_hour < 18:
            toggle_sidebar_state()
            new_bg_color = "#34271F"
            st.markdown(
                    f"""
                    <style>
                    .stApp {{
                        background-color: {new_bg_color};
                        transition: background-color 3s;
                    }}
                    </style>
                    """,
                    unsafe_allow_html=True,
                )
            sleep(0.5)
            st.subheader(f"hey, {user_name}, good afternoon! welcome to popular games data.")
            st.image("https://i.pinimg.com/originals/2a/97/1c/2a971c1ccba457e4bde738c0d39e9705.gif", caption="it's raining.", width=500)
        else:
             toggle_sidebar_state()
             st.write(f'<p style="color: white; font-size: 24px;"><i>"good night, <b>{user_name}</b>. your journey has been a long one...<br> rest a while before proceeding..."</i></p>', unsafe_allow_html=True)
             # st.write('<a href="#" target="_blank" style="color: white; font-size: 20px; text-decoration: none;">[sleep]</a>', unsafe_allow_html=True)
            
             if st.button("😴"):
                st.info("[ you are sleeping... ]")
                new_bg_color = "#000000"
                st.markdown(
                    f"""
                    <style>
                    .stApp {{
                        background-color: {new_bg_color};
                        transition: background-color 3s;
                    }}
                    </style>
                    """,
                    unsafe_allow_html=True,
                )
                # st.image("https://i.gifer.com/43Qz.gif", width=500)
                
             st.image("https://i.gifer.com/GE2a.gif", caption="a noble warrior resting.", width=500)

def home(df):
    st.title("🎮 popular video games 1980 - 2023")
    st.markdown(
        """
this 📊 dataset contains a list of video games dating from 1980 to 2023, it also provides things such as release dates, user review rating, and critic review rating.
"""
    )

    st.dataframe(df)
    st.caption("⬇️ click here to download the dataset:")
    st.download_button("download", "games.csv", "click here to download the dataset.")
    st.write(
        "[link for kaggle dataset ](https://www.kaggle.com/datasets/arnabchaki/popular-video-games-1980-2023)"
    )

def all_search(df):
    st.subheader("🔎 search all by game")

    search_term = st.text_input("enter game name:", "")
    
    columns = list(df.columns)
    columns.insert(0, "📊 all dataset") 
    
    selected_column = st.selectbox("choose what you want to display:", columns)
    
    if search_term:
        search_result = df[df["Title"].str.contains(search_term, case=False)]
        
        if not search_result.empty:
            for _, row in search_result.iterrows():
                st.subheader(f"game: {row['Title']}")
                if selected_column == "📊 all dataset":
                    st.table(row)
                else:
                    st.write(f"{selected_column}: {row[selected_column]}")
        else:
            st.info("no matching games found.")

# Função para extrair valores únicos de uma coluna do DataFrame
def extract_unique_values(data, column_name):
    unique_values = set()

    for item in data[column_name]:
        try:
            if isinstance(item, str):
                item_list = ast.literal_eval(item)
                unique_values.update(item_list)
            else:
                unique_values.add(item)
        except (ValueError, SyntaxError):
            pass

    return list(unique_values)

def game_genre(df, type_of_rating):
    st.subheader("top 10 👑 most popular/worst 📉 games (by genre)")
    search_genre = st.text_input("search by gender:", key="genre_input")

    #  list genre sugest
    generos_sugeridos = df["Genres"].unique()
    generos_sugeridos = extract_unique_values(df, "Genres")

    # filter
    sugestoes_filtradas = [
        genero for genero in generos_sugeridos if search_genre.lower() in genero.lower()
    ]

    if not sugestoes_filtradas:
        sugestoes_filtradas = generos_sugeridos

    genero_selecionado = st.selectbox("select gender:", sugestoes_filtradas)

    if type_of_rating == "best":
        top_10_genero = df[df["Genres"].apply(lambda x: genero_selecionado.lower() in x.lower())].nlargest(10, "Rating").sort_values(by="Rating", ascending=False)
    else:
        top_10_genero = df[df["Genres"].apply(lambda x: genero_selecionado.lower() in x.lower())].nsmallest(10, "Rating").sort_values(by="Rating", ascending=True)

    fig, ax = plt.subplots()
    ax.barh(top_10_genero["Title"], top_10_genero["Rating"], color="black")
    ax.invert_yaxis()
    ax.set_xlabel("rating")
    ax.set_ylabel("game(s)")
    ax.set_title(f"most popular games by genre {genero_selecionado}")

    st.pyplot(fig)

    st.table(top_10_genero[["Title", "Rating"]])
    
def padronizar_valores(valor):
    if 'K' in valor:
        # Valores no formato "1.2K" ou "1.3k"
        return float(valor.replace('K', '').replace('k', '')) * 1000
    else:
        # Valores no formato "987" ou "456"
        return float(valor)

def formatar_valor(valor):
    # Verifique se o valor é um número (pode ser necessário tratar exceções)
    if isinstance(valor, (int, float)):
        # Use a função format para formatar o número com separador de milhar e sem zeros extras
        return "{:.0f}".format(valor)
    else:
        # Se não for um número, retorne o valor original
        return valor

def game_year_popular(df):
    st.subheader("👑 top 10 popular games (by year)")
    selected_year = st.slider("select year:", 1980, 2023, 2001)
    year_data = df[df["Release Date"].str.contains(str(selected_year))]
    year_data = year_data.sort_values(by="Times Listed", ascending=False).head(10)

    # se n tiver dados
    if year_data.empty:
        st.warning("no games found for this year.")
        return
    
    # Crie um gráfico de barras horizontais
    fig, ax = plt.subplots()
    ax.barh(year_data["Title"], year_data["Times Listed"], color="black")
    # Inverta a ordem dos itens
    ax.invert_yaxis()
    ax.set_xlabel("Times Listed")
    ax.set_ylabel("Game(s)")
    ax.set_title(f"most popular games in the year {selected_year}")

    # Exiba o gráfico
    st.pyplot(fig)

    st.write(f"👑 top 10 most popular game in {selected_year}:")
    st.table(year_data[["Title", "Times Listed"]])

def games_by_developer(df, type_of_rating):
    if type_of_rating == "best":
        st.subheader("👑 top 10 best games (by developer)")
    else:
        st.subheader("📉 top 10 worst games (by developer)")

    developers = df["Team"].unique()
    developers = extract_unique_values(df, "Team")
    developers = [dev for dev in developers if isinstance(dev, str) and "EA" not in dev]

    selected_developer = st.selectbox("select a developer:", developers)

    if type_of_rating == "best":
        top_10_developer_games = df[df["Team"].str.contains(selected_developer, na=False)].nlargest(10, "Rating")
    else:
        top_10_developer_games = df[df["Team"].str.contains(selected_developer, na=False)].nsmallest(10, "Rating")

    if top_10_developer_games.empty:
        st.warning("🚨 [ no games found for this developer. ]")
        return

    st.table(top_10_developer_games[["Title", "Rating"]])

def more_rated(df):
    st.subheader("📈 top 10 more rated games")

    top_10_avaliados = df.nlargest(10, "Number of Reviews")

    # Crie um gráfico de barras horizontais
    fig, ax = plt.subplots()
    ax.barh(top_10_avaliados["Title"], top_10_avaliados["Number of Reviews"], color="black")
    # Inverta a ordem dos itens
    ax.invert_yaxis()
    ax.set_xlabel("Number of Reviews")
    ax.set_ylabel("Game(s)")
    ax.set_title("top 10 more rated games")

    # Exiba o gráfico
    st.pyplot(fig)

    st.table(top_10_avaliados[["Title", "Number of Reviews"]])

def best_rated(df):
    st.subheader("📈 top 10 best rated games")

    top_10_avaliados = df.nlargest(10, "Rating")
    # Crie um gráfico de barras horizontais
    fig, ax = plt.subplots()
    ax.barh(top_10_avaliados["Title"], top_10_avaliados["Rating"], color="black")
    # Inverta a ordem dos itens
    ax.invert_yaxis()
    ax.set_xlabel("rating")
    ax.set_ylabel("game(s)")
    ax.set_title("top 10 best rated games")

    # Exiba o gráfico
    st.pyplot(fig)
    st.table(top_10_avaliados[["Title", "Rating"]])

def best_rated_by_year(df, type_of_rating):
    st.subheader("top 10 📈 best/worst 📉 rated games (by year)")

    selected_year = st.slider("select year:", 1980, 2023, 2001)
    year_data = df[df["Release Date"].str.contains(str(selected_year))]

    if type_of_rating == "best":
        top_10_avaliados_por_ano = year_data.nlargest(10, "Rating")
    else:
        top_10_avaliados_por_ano = year_data.nsmallest(10, "Rating")

    # se n tiver dados
    if top_10_avaliados_por_ano.empty:
        st.warning("🚨 [ no games found for this year. ]")
        return
    
    # Crie um gráfico de barras horizontais
    fig, ax = plt.subplots()
    ax.barh(top_10_avaliados_por_ano["Title"], top_10_avaliados_por_ano["Rating"], color="black")
    # Inverta a ordem dos itens
    ax.invert_yaxis()
    ax.set_xlabel("Rating")
    ax.set_ylabel("Game(s)")
    ax.set_title(f"The top 10 {type_of_rating} rated games in the year {selected_year}")

    # Exiba o gráfico
    st.pyplot(fig)

    st.table(top_10_avaliados_por_ano[["Title", "Rating"]])

def released_by_year(df):
    st.subheader("🚀 games released in year")

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

# def worst_by_genre(df):
#     st.subheader("the 10 worst games by genre")
#     search_genre = st.text_input("search by genre:", key="worst_genre_input")

#     if not search_genre:
#         st.warning("please, insert something.")
#         return

#     genre_data = df[df["Genres"].str.lower().str.contains(search_genre.lower())]
    
#     if genre_data.empty:
#         st.warning("no games found for this genre.")
#         return

#     worst_10_genre = genre_data.nsmallest(10, "Rating")

#     st.table(worst_10_genre[["Title", "Rating"]])

# def worst_by_year(df):
#     st.subheader("top 10 worst games by year")
#     selected_year = st.slider("select year:", 1980, 2023, 2001)

#     year_data = df[df['Release Date'].str.contains(str(selected_year))]

#     if year_data.empty:
#         st.warning("no games found for this year.")
#         return

#     worst_10_year = year_data.nsmallest(10, "Rating")

#     st.table(worst_10_year[["Title", "Rating"]])

# to fix ValueError: Cannot mask with non-boolean array containing NA / NaN values
# def worst_by_developer(df):
#     st.subheader("top 10 most worst games by developer")
#     search_developer = (
#         st.text_input("search developer:", key="developer_input").strip().lower()
#     )

#     developers = df["Team"].unique()

#     developers_filtrados = [
#         dev for dev in developers if search_developer in str(dev).lower()
#     ]

#     if not developers_filtrados and search_developer:
#         st.warning("no developers found. Displaying all available developers.")
#         developers_filtrados = developers

#     selected_developer = st.selectbox("select a developer:", developers_filtrados)

#     bottom_10_developer_games = df[
#         df["Team"].str.lower() == str(selected_developer).lower()
#     ].nsmallest(10, "Rating")

#     st.table(bottom_10_developer_games[["Title", "Rating"]])

def worst_overall(df):
    st.subheader("📉 top 10 worst games overall")
    
    worst_10_overall = df.nsmallest(10, "Rating")

    # grafico
    fig, ax = plt.subplots()
    ax.barh(worst_10_overall["Title"], worst_10_overall["Rating"], color="black")
    ax.invert_yaxis()
    ax.set_xlabel("Rating")
    ax.set_ylabel("game(s)")
    ax.set_title("top 10 worst rated games")

    st.pyplot(fig)

    st.table(worst_10_overall[["Title", "Rating"]])

# def worst_by_year(df):
#     st.subheader("top 10 worst by year")
#     selected_year = st.slider("select year:", 1980, 2023, 2001)

#     year_data = df[df['Release Date'].str.contains(str(selected_year))]

#     if year_data.empty:
#         st.warning("no games found for this year.")
#         return

#     worst_10_year = year_data.nsmallest(10, "Rating")

#     st.table(worst_10_year[["Title", "Rating"]])

def most_played_by_year(df):
    st.subheader("🎲 most played by year")
    year = st.slider("select year:", 1980, 2023, 2001)
    
    df = df[df["Release Date"].str.match(r'^[A-Za-z]{3} \d{1,2}, \d{4}$', na=False, case=False)]
    
    df["Release Date"] = pd.to_datetime(df["Release Date"], format='%b %d, %Y', errors='coerce')
    
    year_data = df[df["Release Date"].dt.year == year]
    top_played_games = year_data.sort_values(by="Plays", ascending=False).head(10)

    if top_played_games.empty:
        st.warning("🚨 [ no games found for this year. ]")
        return
    
    fig, ax = plt.subplots()
    ax.barh(top_played_games["Title"], top_played_games["Plays"], color="black")
    ax.invert_yaxis()
    ax.set_xlabel("Plays")
    ax.set_ylabel("Game(s)")
    ax.set_title(f"The top 10 most played games in the year {year}")

    st.pyplot(fig)
    
    st.table(top_played_games[["Title", "Plays"]])

def least_played_by_year(df):
    st.subheader("🎲 least played games by year")
    year = st.slider("select year:", 1980, 2023, 2001)
    
    df = df[df["Release Date"].str.match(r'^[A-Za-z]{3} \d{1,2}, \d{4}$', na=False, case=False)]
    
    df["Release Date"] = pd.to_datetime(df["Release Date"], format='%b %d, %Y', errors='coerce')
    
    year_data = df[df["Release Date"].dt.year == year]
    
    year_data = year_data.dropna(subset=["Plays"])
    
    bottom_played_games = year_data.sort_values(by="Plays").head(10)
    
    if bottom_played_games.empty:
        st.warning("🚨 [ no games found for this year. ]")
        return
    
    fig, ax = plt.subplots()
    ax.barh(bottom_played_games["Title"], bottom_played_games["Plays"], color="black")
    ax.invert_yaxis()
    ax.set_xlabel("Plays")
    ax.set_ylabel("Game(s)")
    ax.set_title(f"The top 10 most played games in the year {year}")

    st.pyplot(fig)
    
    st.table(bottom_played_games[["Title", "Plays"]])

def wishlist_but_not_played(df):
    st.subheader("📖 games in backlog but not played")
    
    df["Backlogs"] = pd.to_numeric(df["Backlogs"], errors="coerce")
    df["Plays"] = pd.to_numeric(df["Plays"], errors="coerce")
    
    backlog_not_played = df[(df["Backlogs"] > 0) & (df["Plays"] == 0)]
    
    if backlog_not_played.empty:
        st.info("no backlog but unplayed games found.")
    elif len(backlog_not_played) == 1:
        st.info("⭐ [ only 1 game(earthblade) on the backlog has never been played ]")
        st.table(backlog_not_played[["Title", "Backlogs", "Plays"]])   
    else:
        st.table(backlog_not_played[["Title", "Backlogs", "Plays"]])

def wishlist_games(df):
    st.subheader("📖 top 10 more whishlist games")
    
    search_term = st.text_input("search game:", "")
    
    df["Wishlist"] = pd.to_numeric(df["Wishlist"], errors="coerce")
    
    if search_term:
        wishlist = df[df["Title"].str.contains(search_term, case=False) & (df["Wishlist"] > 0)]
    else:
        wishlist = df[df["Wishlist"] > 0]
    
    top_10_wishlist = wishlist.nlargest(10, "Wishlist")

    fig, ax = plt.subplots()
    ax.barh(top_10_wishlist["Title"], top_10_wishlist["Wishlist"], color="black")
    ax.invert_yaxis()
    ax.set_xlabel("Wishlist")
    ax.set_ylabel("Game(s)")
    ax.set_title("The top 10 most wishlist games")

    st.pyplot(fig)
    
    st.table(top_10_wishlist[["Title", "Wishlist"]])

def played_games(df):
    st.subheader("🎮 games played (6 months ago)")
    
    search_term = st.text_input("search game:", "")
    
    df["Plays"] = pd.to_numeric(df["Plays"], errors="coerce")
    
    if search_term:
        played = df[df["Title"].str.contains(search_term, case=False) & (df["Plays"] > 0)]
    else:
        played = df[df["Plays"] > 0]
    
    top_10_played = played.nlargest(10, "Plays")

    if len(top_10_played) > 1:
        fig, ax = plt.subplots()
        ax.barh(top_10_played["Title"], top_10_played["Plays"], color="black")
        ax.invert_yaxis()
        ax.set_xlabel("Plays")
        ax.set_ylabel("Game(s)")
        ax.set_title("The top 10 most Plays games")

        st.pyplot(fig)

    
    st.table(top_10_played[["Title", "Plays"]])

def playing_games(df):
    st.subheader("🎮 games playing now (6 months ago)")
    
    search_term = st.text_input("search game:", "")
    
    df["Playing"] = pd.to_numeric(df["Playing"], errors="coerce")
    
    if search_term:
        playing = df[df["Title"].str.contains(search_term, case=False) & (df["Playing"] > 0)]
    else:
        playing = df[df["Playing"] > 0]
    
    top_10_playing = playing.nlargest(10, "Playing")

    # only show graph if there is  more than 1 game
    if len(top_10_playing) > 1:
        fig, ax = plt.subplots()
        ax.barh(top_10_playing["Title"], top_10_playing["Playing"], color="black")
        ax.invert_yaxis()
        ax.set_xlabel("Playing")
        ax.set_ylabel("Game(s)")
        ax.set_title("The top 10 most playing games")

        st.pyplot(fig)
    
    st.table(top_10_playing[["Title", "Playing"]])
    
    if st.button("?"):
        new_bg_color = "#370BB4"
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-color: {new_bg_color};
                transition: background-color 1s;
            }}
            </style>
            """,
            unsafe_allow_html=True,
        )
        st.balloons()
        sleep(1)
        st.warning("⭐ [ congratulations for getting this far ]")
        sleep(2)
        st.info("⭐ [ you win! ]")
        sleep(2)

def content8():
    st.write("content x")


def content9():
    st.write("content xx")


def content10():
    st.write("content xxx")
