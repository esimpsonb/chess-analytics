import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
import plotly.express as px
import chess.pgn
import chess.svg
from io import StringIO
import numpy as np


# =====================
# Función para gráficos de resultados
# =====================
import matplotlib.pyplot as plt

def plot_results(values, labels, title, total):
    """
    Donut chart con Plotly para mostrar resultados (Victorias, Tablas, Derrotas).
    """
    colors = {
        "Victorias": "#2ecc71",  # verde
        "Tablas": "#f1c40f",     # amarillo
        "Derrotas": "#e74c3c"    # rojo
    }

    data = {"Resultado": labels, "Cantidad": values}
    fig = px.pie(
        data,
        names="Resultado",
        values="Cantidad",
        hole=0.5,
        color="Resultado",
        color_discrete_map=colors
    )

    # Mostrar % y valores dentro
    fig.update_traces(
        textposition="inside",
        textinfo="label+percent",
        insidetextfont=dict(color="white", size=12, family="Arial Black"),
    )

    # Texto central con total de partidas
    fig.add_annotation(
        text=f"<b>{total}</b><br>partidas",
        x=0.5, y=0.5, showarrow=False,
        font=dict(size=14, color="white", family="Arial Black"),
        align="center"
    )

    # Layout
    fig.update_layout(
        title=dict(text=title, x=0.5, font=dict(size=14, family="Arial Black")),
        margin=dict(t=50, b=20, l=20, r=20),
        showlegend=False,
        height=350, width=350
    )

    return fig

# =====================
# Función para mostrar info del jugador
# =====================
def show_player_info(jugador_info):
    """
    Muestra la info de un jugador en Streamlit (foto, país, título, rating).
    """
    st.subheader(jugador_info["name"] if pd.notna(jugador_info["name"]) else jugador_info["player"])

    if pd.notna(jugador_info["avatar"]) and str(jugador_info["avatar"]).strip() != "":
        st.image(jugador_info["avatar"], width=150)
    else:
        st.info("📷 Sin foto disponible")

    st.write(f"**País:** {jugador_info['country']}")
    st.write(f"**Título:** {jugador_info['title']}")
    st.write(f"**Rating:** {jugador_info['rating']}")


def plot_titles_distribution(players):
    """
    Gráfico donut (Plotly) con distribución de títulos GM, IM, FM y 'Otros'.
    """
    title_counts = players["title"].value_counts()

    # Agrupar todo lo que no sea GM, IM, FM en "Otros"
    major_titles = ["GM", "IM", "FM"]
    title_counts = title_counts.groupby(
        title_counts.index.where(title_counts.index.isin(major_titles), "Otros")
    ).sum().reset_index()
    title_counts.columns = ["title", "count"]

    fig = px.pie(
        title_counts,
        names="title",
        values="count",
        hole=0.5,
        color="title",
        color_discrete_map={
            "GM": "#e74c3c",    # rojo
            "IM": "#3498db",    # azul
            "FM": "#2ecc71",    # verde
            "Otros": "#95a5a6"  # gris
        }
    )

    fig.update_traces(
        textposition="inside",
        textinfo="label+percent",
        insidetextfont=dict(color="white", size=12, family="Arial Black"),
    )
    fig.update_layout(
        title_text="Jugadores por título",
        title_x=0.5,
        margin=dict(t=40, b=20, l=20, r=20),
        showlegend=False,
        height=400, width=400
    )

    return fig

def plot_openings(df, title, color_scale="Blues"):
    """
    Genera un gráfico de barras horizontales de aperturas.
    - df: DataFrame con columnas ["Apertura", "Partidas"]
    - title: título del gráfico
    - color_scale: esquema de color de Plotly (ej: "Blues", "Greens")
    """
    if df.empty:
        return None

    fig = px.bar(
        df,
        x="Partidas",
        y="Apertura",
        orientation="h",
        color="Partidas",
        color_continuous_scale=color_scale,
        text="Partidas"
    )
    fig.update_layout(
        title=dict(text=title, x=0.5, font=dict(size=14, family="Arial Black")),
        yaxis=dict(categoryorder="total ascending"),
        margin=dict(t=50, b=20, l=20, r=20),
        height=350
    )
    return fig

def plot_top_openings(top_openings):
    """Top 10 aperturas más jugadas"""
    fig = px.bar(
        top_openings.sort_values("count", ascending=True),
        x="count", y="eco_name",
        orientation="h",
        title="Top 10 aperturas más jugadas",
        color="count", color_continuous_scale="Blues"
    )
    fig.update_layout(yaxis=dict(categoryorder="total ascending"))
    return fig


def plot_openings_decisivas(decisivas_df):
    """Porcentaje de partidas decisivas en las 10 aperturas más jugadas"""
    fig = px.bar(
        decisivas_df,
        x="ratio_decisivas", y="eco_name",
        orientation="h",
        title="Aperturas más decisivas (Top 10 jugadas)",
        color="ratio_decisivas", color_continuous_scale="Reds",
        text=decisivas_df["ratio_decisivas"].apply(lambda x: f"{x:.1%}")
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(yaxis=dict(categoryorder="total ascending"))
    return fig


def plot_openings_distribution(top_openings):
    """Distribución global de las aperturas más jugadas"""
    fig = px.pie(
        top_openings,
        names="eco_name", values="count",
        hole=0.4,
        title="Distribución global de aperturas (Top 10)"
    )
    return fig


def show_pgn_viewer(pgn_text, session_key="move_number"):
    game = chess.pgn.read_game(StringIO(pgn_text))
    board = game.board()
    moves = list(game.mainline_moves())

    # Estado de jugada
    if session_key not in st.session_state:
        st.session_state[session_key] = 0

    for move in moves[:st.session_state[session_key]]:
        board.push(move)

    last_move = moves[st.session_state[session_key] - 1] if st.session_state[session_key] > 0 else None
    arrows = []
    if last_move:
        arrows = [(last_move.from_square, last_move.to_square)]

    boardsvg = chess.svg.board(board=board, size=400, arrows=arrows)
    st.write(boardsvg, unsafe_allow_html=True)

    # ---- Navegación con callbacks ----
    def go_start():
        st.session_state[session_key] = 0

    def go_prev():
        st.session_state[session_key] = max(0, st.session_state[session_key] - 1)

    def go_next():
        st.session_state[session_key] = min(len(moves), st.session_state[session_key] + 1)

    def go_end():
        st.session_state[session_key] = len(moves)

    cols = st.columns([0.2,0.2,0.2,0.2,2])
    with cols[0]:
        st.button("⏮️", key=f"{session_key}_start", on_click=go_start)
    with cols[1]:
        st.button("⬅️", key=f"{session_key}_prev", on_click=go_prev)
    with cols[2]:
        st.button("➡️", key=f"{session_key}_next", on_click=go_next)
    with cols[3]:
        st.button("⏭️", key=f"{session_key}_end", on_click=go_end)

    # Info
    st.markdown(f"**Jugada:** {st.session_state[session_key]}/{len(moves)}")
    st.markdown(f"**Evento:** {game.headers.get('Event', '---')}")
    st.markdown(f"**Blancas:** {game.headers.get('White', '---')}")
    st.markdown(f"**Negras:** {game.headers.get('Black', '---')}")
    st.markdown(f"**Resultado:** {game.headers.get('Result', '---')}")
# ---------------------------
# Función: obtener top 5 victorias
# ---------------------------
def get_top_wins(player_games, selected_player, top = True):
    # Agregar rival_elo
    player_games["rival_elo"] = np.where(
        player_games["black_username"] == selected_player,
        player_games["white_rating"],
        player_games["black_rating"]
    )

    # Agregar player_score
    player_games["player_score"] = np.where(
        player_games["white_username"] == selected_player,
        np.where(player_games["white_result"] == "win", 1, 0),
        np.where(player_games["black_result"] == "win", 1, 0)
    )

    # Top 5 victorias
    if top:
        top_wins = (
            player_games[player_games["player_score"] == 1]
            .sort_values("rival_elo", ascending=False)
            .head(5)
        )
        return top_wins
    else:
        worst_wins = (
            player_games[player_games["player_score"] == 0]
            .sort_values("rival_elo", ascending=False)
            .tail(5)
        )
        return worst_wins        
