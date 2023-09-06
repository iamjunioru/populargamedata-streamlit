import streamlit as st
import pandas as pd
from functions import *
from curr_time import current_time

st.set_page_config(
    page_title="populargamesdata ",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="auto",
)

# load dataset
df = pd.read_csv("games.csv")
# or
# data_url = "csvurl"
# df = pd.read_csv(data_url)

st.sidebar.title("🎮 populargamedata.st")
st.sidebar.subheader("(u can choose one option below)")

# menu expander
menu_expander = st.sidebar.expander("🗺️ menu")
# menu select
menu = menu_expander.radio(
    "select a option:",
    [
        "true home",
        "home sweet home",
        "top 10 most popular game (by genre)",
        "top 10 most popular game (by year)",
        "top 10 most popular game (by dev)",
        "the 10 more rated games",
        "the 10 best rated games",
        "the 10 best rated games by year",
        "number of games released in year",
        "content 8",
        "content 9",
        "content 10",
    ],
)

with st.sidebar.expander("🕹️ about team"):
    st.subheader("> made with 💔 by:")
    st.write("junior - marllon - aleandro - juan")

with st.sidebar.expander("📝 about this project"):
    st.subheader("> repo on github:")
    st.markdown(
        '<a href="https://github.com/iamjunioru/populargames-streamlit" target="_blank">click here {populargames-streamlit}</a>',
        unsafe_allow_html=True)
    st.markdown(f'<p style="color: gray; font-weight: bold;">- isso foi feito no dia 06/09/2023 às 17:50<br>- estamos no dia {current_time}.<br><br>© 2023 Sistemas de Apoio a Decisão.</p>', unsafe_allow_html=True)
    

# menu select
if menu == "true home":
    true_home()
if menu == "home sweet home":
    home(df)
elif menu == "top 10 most popular game (by genre)":
    game_genre(df)
elif menu == "top 10 most popular game (by year)":
    game_year_popular(df)
elif menu == "top 10 most popular game (by dev)":
    games_by_developer(df)
elif menu == "the 10 more rated games":
    more_rated(df)
elif menu == "the 10 best rated games":
    best_rated(df)
elif menu == "the 10 best rated games by year":
    best_rated_by_year(df)
elif menu == "number of games released in year":
    released_by_year(df)


# footer
# st.write("© 2023 Sistema de Apoio a Decisão")
