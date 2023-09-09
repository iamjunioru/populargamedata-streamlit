import streamlit as st
import pandas as pd
from functions import *
from curr_time import current_time
from sidebar_state import sidebar_state

st.set_page_config(
    page_title="populargamesdata ",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state=sidebar_state
    # for dev active this "expanded"
    # initial_sidebar_state="expanded"
)

# load dataset
# df = pd.read_csv("games.csv") 
# or
data_url = "https://raw.githubusercontent.com/iamjunioru/populargamedata-streamlit/main/src/games.csv"
df = pd.read_csv(data_url)

st.sidebar.title("🎮 populargamedata.st")

st.sidebar.subheader("(u can choose one option below)")

# menu expander
menu_expander = st.sidebar.expander("🗺️ menu")
# menu select
menu = menu_expander.radio(
    "🔵 select a option:",
    [
        "🏰 home",
        "📊 the dataset",
        "🔎 search all by game",
        "👑 popular games by genre",
        "👑 popular games by year",
        "👑 popular games by dev",
        "📈 more rated games",
        "📈 best rated games",
        "📈 best rated games by year",
        "🚀 games released in year",
        "📉 worst by genre",
        "📉 worst by year",
        "📉 worst by developer",
        "📉 worst overral",
        "🎲 most played by year",
        "🎲 least played by year",
        "📖 wishlist but no played",
        "📖 wishlist games",
        "🎮 played games",
        "🎮 playing games"
    ],
)

with st.sidebar.expander("🕹️ about team"):
    st.subheader("> made with 💔 by:")
    st.write("[ junior - marllon - aleandro - juan ]")
    st.image("https://i.gifer.com/YTup.gif", width=100)
    st.text("* a cat spinning *")
        


with st.sidebar.expander("📝 about this project"):
    st.subheader("> repo on github:")
    st.markdown(
        '<a href="https://github.com/iamjunioru/populargames-streamlit" target="_blank">click here {populargames-streamlit}</a>',
        unsafe_allow_html=True)
    st.markdown(f'<p style="color: gray; font-weight: bold;">- isso foi feito no dia 06/09/2023 às 17:50<br>- estamos no dia {current_time}.<br><br>© 2023 Sistemas de Apoio a Decisão.</p>', unsafe_allow_html=True)
    

# menu select
if menu == "🏰 home":
    true_home()
if menu == "📊 the dataset":
    home(df)
elif menu == "🔎 search all by game":
    all_search(df)
elif menu == "👑 popular games by genre":
    game_genre(df)
elif menu == "👑 popular games by year":
    game_year_popular(df)
elif menu == "👑 popular games by dev":
    games_by_developer(df)
elif menu == "📈 more rated games":
    more_rated(df)
elif menu == "📈 best rated games":
    best_rated(df)
elif menu == "📈 best rated games by year":
    best_rated_by_year(df)
elif menu == "🚀 games released in year":
    released_by_year(df)
elif menu == "📉 worst by genre":
    worst_by_genre(df)
elif menu == "📉 worst by year":
    worst_by_year(df)
elif menu == "📉 worst by developer":
    worst_by_developer(df)
elif menu == "📉 worst overral":
    worst_overall(df)
if menu == "🎲 most played by year":
    most_played_by_year(df)
elif menu == "🎲 least played by year":
    least_played_by_year(df)
elif menu == "📖 wishlist but no played":
    wishlist_but_not_played(df)
elif menu == "📖 wishlist games":
    wishlist_games(df)
elif menu == "🎮 played games":
    played_games(df)
elif menu == "🎮 playing games":
    playing_games(df)


# footer
# st.write("© 2023 Sistema de Apoio a Decisão")
