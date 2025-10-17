import streamlit as st
from source.utils import show_player_info, plot_results, plot_openings, show_pgn_viewer, get_top_wins

def render(players, games):
    st.header("Exploración de partidas últimos 3 meses")

    jugadores = players.sort_values("rating", ascending=False)["player"].tolist()
    selected_player = st.selectbox("Selecciona un jugador", jugadores)

    partidas = games[(games["white_username"] == selected_player) | (games["black_username"] == selected_player)]

    victorias = (
        (partidas["white_username"].eq(selected_player) & (partidas["score_white"] == 1)).sum()
        + (partidas["black_username"].eq(selected_player) & (partidas["score_black"] == 1)).sum()
    )
    tablas = (
        (partidas["white_username"].eq(selected_player) & (partidas["score_white"] == 0.5)).sum()
        + (partidas["black_username"].eq(selected_player) & (partidas["score_black"] == 0.5)).sum()
    )
    derrotas = len(partidas) - victorias - tablas

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Partidas", len(partidas))
    c2.metric("Victorias", victorias)
    c3.metric("Tablas", tablas)
    c4.metric("Derrotas", derrotas)

    c1, c2 = st.columns([1, 2])

    with c1:
        jugador_info = players[players["player"] == selected_player].iloc[0]
        show_player_info(jugador_info)

    with c2:
        g1, g2 = st.columns(2)

        with g1:
            fig = plot_results(
                [victorias, tablas, derrotas],
                ["Victorias", "Tablas", "Derrotas"],
                "Últimos 3 meses",
                len(partidas)
            )
            st.plotly_chart(fig, use_container_width=False)

        with g2:
            fig = plot_results(
                [int(jugador_info["wins_total"]),
                int(jugador_info["draws_total"]),
                int(jugador_info["losses_total"])],
                ["Victorias", "Tablas", "Derrotas"],
                "Totales",
                int(jugador_info["wins_total"] + jugador_info["draws_total"] + jugador_info["losses_total"])
            )
            st.plotly_chart(fig, use_container_width=False)
    
    #st.subheader("🏆 Mejores 5 victorias (por ELO del rival)")

    top_wins = get_top_wins(partidas.copy(), selected_player)
    worst_losses =get_top_wins(partidas.copy(), selected_player,False)

    if not top_wins.empty and not worst_losses.empty:
        c1, c2 = st.columns([1.5, 1.5])  # proporciones iguales
        
        # Columna izquierda: mejores victorias
        with c1:
            g1,g2 = st.columns([1.28, 3])
            g1 =st.subheader("🏆 Mejores 5 victorias (por ELO del rival)")
            selected_win = st.selectbox(
                "Selecciona una partida para ver",
                top_wins["url"].tolist(),
                format_func=lambda x: (
                    f"{top_wins.loc[top_wins['url']==x,'white_username'].iloc[0]} "
                    f"({top_wins.loc[top_wins['url']==x,'white_rating'].iloc[0]}) vs "
                    f"{top_wins.loc[top_wins['url']==x,'black_username'].iloc[0]} "
                    f"({top_wins.loc[top_wins['url']==x,'black_rating'].iloc[0]})"
                ),
                key="select_win"
            )
            pgn_win = top_wins[top_wins["url"] == selected_win]["pgn"].iloc[0]
            show_pgn_viewer(pgn_win, session_key="viewer_topwins")

        # Columna derecha: peores derrotas
        with c2:
            st.subheader("💀 Peores 5 derrotas (por ELO del rival)")
            selected_loss = st.selectbox(
                "Selecciona una partida para ver",
                worst_losses["url"].tolist(),
                format_func=lambda x: (
                    f"{worst_losses.loc[worst_losses['url']==x,'white_username'].iloc[0]} "
                    f"({worst_losses.loc[worst_losses['url']==x,'white_rating'].iloc[0]}) vs "
                    f"{worst_losses.loc[worst_losses['url']==x,'black_username'].iloc[0]} "
                    f"({worst_losses.loc[worst_losses['url']==x,'black_rating'].iloc[0]})"
                ),
                key="select_loss"
            )
            pgn_loss = worst_losses[worst_losses["url"] == selected_loss]["pgn"].iloc[0]
            show_pgn_viewer(pgn_loss, session_key="viewer_toplosses")

    st.subheader("📊 Aperturas más jugadas (últimos 3 meses)")

    partidas_blancas = partidas[partidas["white_username"] == selected_player]
    partidas_negras = partidas[partidas["black_username"] == selected_player]

    top_blancas = partidas_blancas["eco_name"].value_counts().head(5).reset_index()
    top_blancas.columns = ["Apertura", "Partidas"]

    top_negras = partidas_negras["eco_name"].value_counts().head(5).reset_index()
    top_negras.columns = ["Apertura", "Partidas"]

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("### ♔ Con blancas")
        fig_white = plot_openings(top_blancas, "Top aperturas con blancas", "Blues")
        if fig_white:
            st.plotly_chart(fig_white, use_container_width=True)
        else:
            st.info("No hay partidas recientes con blancas.")

    with c2:
        st.markdown("### ♚ Con negras")
        fig_black = plot_openings(top_negras, "Top aperturas con negras", "Greens")
        if fig_black:
            st.plotly_chart(fig_black, use_container_width=True)
        else:
            st.info("No hay partidas recientes con negras.")
