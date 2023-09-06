import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# load dataset
df = pd.read_csv("games.csv")
# or 
# data_url = "csvurl"
# df = pd.read_csv(data_url)

st.title("popular video games 1980 - 2023 🎮")

st.dataframe(df)