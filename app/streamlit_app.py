import streamlit as st
import os
import pandas as pd

from app.tabs import players_tab, front_tab, openings_tab

st.set_page_config(page_title="Chess Analytics", layout="wide")

DATA_DIR = "./data"

def load_data():
    players = pd.read_csv(os.path.join(DATA_DIR, "players_stats.csv"))
    games = pd.read_csv(os.path.join(DATA_DIR, "chess_games.csv"))
    return players, games

players, games = load_data()

st.title("♟️ Chess Analytics Dashboard")

tabs = st.tabs(["Resumen General", "Jugadores", "Aperturas"])

with tabs[0]:
    front_tab.render(players, games)

with tabs[1]:
    players_tab.render(players, games)

with tabs[2]:
    openings_tab.render(games)
