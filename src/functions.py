import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from curr_time import current_time
from sidebar_state import toggle_sidebar_state
from time import sleep

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
            st.subheader(f"hey, {user_name}, good day! welcome to popular games data.")
            
        elif 12 <= current_hour < 18:
            st.subheader(f"hey, {user_name}, good afternoon! welcome to popular games data.")
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
                
             st.image("https://i.gifer.com/GE2a.gif", width=500)

def home(df):
    st.title("popular video games 1980 - 2023 🎮")
    st.markdown(
        """
this dataset contains a list of video games dating from 1980 to 2023, it also provides things such as release dates, user review rating, and critic review rating.
"""
    )
    st.dataframe(df)

def all_search(df):
    st.subheader("search all by game")

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
    st.write("the value is convert(string to numeric)")

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

def worst_by_genre(df):
    st.subheader("the 10 worst games by genre")
    search_genre = st.text_input("search by genre:", key="worst_genre_input")

    if not search_genre:
        st.warning("please, insert something.")
        return

    genre_data = df[df["Genres"].str.lower().str.contains(search_genre.lower())]
    
    if genre_data.empty:
        st.warning("no games found for this genre.")
        return

    worst_10_genre = genre_data.nsmallest(10, "Rating")

    st.table(worst_10_genre[["Title", "Rating"]])

def worst_by_year(df):
    st.subheader("top 10 worst games by year")
    selected_year = st.slider("select year:", 1980, 2023, 2001)

    year_data = df[df['Release Date'].str.contains(str(selected_year))]

    if year_data.empty:
        st.warning("no games found for this year.")
        return

    worst_10_year = year_data.nsmallest(10, "Rating")

    st.table(worst_10_year[["Title", "Rating"]])

# to fix ValueError: Cannot mask with non-boolean array containing NA / NaN values
def worst_by_developer(df):
    st.subheader("top 10 most worst games by developer")
    search_developer = (
        st.text_input("search developer:", key="developer_input").strip().lower()
    )

    developers = df["Team"].unique()

    developers_filtrados = [
        dev for dev in developers if search_developer in str(dev).lower()
    ]

    if not developers_filtrados and search_developer:
        st.warning("no developers found. Displaying all available developers.")
        developers_filtrados = developers

    selected_developer = st.selectbox("select a developer:", developers_filtrados)

    bottom_10_developer_games = df[
        df["Team"].str.lower() == str(selected_developer).lower()
    ].nsmallest(10, "Rating")

    st.table(bottom_10_developer_games[["Title", "Rating"]])

def worst_overall(df):
    st.subheader("top 10 worst games overall")
    
    worst_10_overall = df.nsmallest(10, "Rating")

    st.table(worst_10_overall[["Title", "Rating"]])

def worst_by_year(df):
    st.subheader("top 10 worst by year")
    selected_year = st.slider("select year:", 1980, 2023, 2001)

    year_data = df[df['Release Date'].str.contains(str(selected_year))]

    if year_data.empty:
        st.warning("no games found for this year.")
        return

    worst_10_year = year_data.nsmallest(10, "Rating")

    st.table(worst_10_year[["Title", "Rating"]])

def most_played_by_year(df):
    st.subheader("most played by year")
    year = st.slider("select year:", 1980, 2023, 2001)
    
    df = df[df["Release Date"].str.match(r'^[A-Za-z]{3} \d{1,2}, \d{4}$', na=False, case=False)]
    
    df["Release Date"] = pd.to_datetime(df["Release Date"], format='%b %d, %Y', errors='coerce')
    
    year_data = df[df["Release Date"].dt.year == year]
    top_played_games = year_data.sort_values(by="Plays", ascending=False).head(10)
    
    st.table(top_played_games[["Title", "Plays"]])

def least_played_by_year(df):
    st.subheader("least played games by year")
    year = st.slider("select year:", 1980, 2023, 2001)
    
    df = df[df["Release Date"].str.match(r'^[A-Za-z]{3} \d{1,2}, \d{4}$', na=False, case=False)]
    
    df["Release Date"] = pd.to_datetime(df["Release Date"], format='%b %d, %Y', errors='coerce')
    
    year_data = df[df["Release Date"].dt.year == year]
    
    year_data = year_data.dropna(subset=["Plays"])
    
    bottom_played_games = year_data.sort_values(by="Plays").head(10)
    
    st.table(bottom_played_games[["Title", "Plays"]])

def wishlist_but_not_played(df):
    st.subheader("games in backlog but not played")
    
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
    st.subheader("top 10 games in wishlist")
    
    search_term = st.text_input("search game:", "")
    
    df["Wishlist"] = pd.to_numeric(df["Wishlist"], errors="coerce")
    
    if search_term:
        wishlist = df[df["Title"].str.contains(search_term, case=False) & (df["Wishlist"] > 0)]
    else:
        wishlist = df[df["Wishlist"] > 0]
    
    top_10_wishlist = wishlist.nlargest(10, "Wishlist")
    
    st.table(top_10_wishlist[["Title", "Wishlist"]])

def played_games(df):
    st.subheader("games played (6 months ago)")
    
    search_term = st.text_input("search game:", "")
    
    df["Plays"] = pd.to_numeric(df["Plays"], errors="coerce")
    
    if search_term:
        played = df[df["Title"].str.contains(search_term, case=False) & (df["Plays"] > 0)]
    else:
        played = df[df["Plays"] > 0]
    
    top_10_played = played.nlargest(10, "Plays")
    
    st.table(top_10_played[["Title", "Plays"]])

def playing_games(df):
    st.subheader("games playing now (6 months ago)")
    
    search_term = st.text_input("search game:", "")
    
    df["Playing"] = pd.to_numeric(df["Playing"], errors="coerce")
    
    if search_term:
        playing = df[df["Title"].str.contains(search_term, case=False) & (df["Playing"] > 0)]
    else:
        playing = df[df["Playing"] > 0]
    
    top_10_playing = playing.nlargest(10, "Playing")
    
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
