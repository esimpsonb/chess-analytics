import streamlit as st
from source.utils import plot_titles_distribution

def render(players, games):
    st.header("Ranking de jugadores")

    logo_path = "./data/chess_com_logo.png"
    st.image(logo_path, width=160)
    st.markdown("### 🌍 **Top 250 jugadores en Chess.com (Blitz)**")

    col1, col2, col3 = st.columns(3)
    col1.metric("👥 Jugadores activos", len(players))
    col2.metric("♟️ Total partidas", len(games))
    col3.metric("📈 Winrate promedio", f"{players['avg_score'].mean():.2f}")

    st.subheader("Top 10 y distribución de títulos")

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("#### Top 10 por rating")
        top10 = players.sort_values("rating", ascending=False).head(10).reset_index(drop=True)
        top10["Rank"] = ["🥇", "🥈", "🥉"] + list(map(str, range(4, 11)))
        st.table(top10.set_index("Rank")[["name", "rating", "title", "country"]])

    with c2:
        st.markdown("#### Distribución de títulos en el Top 250")
        fig = plot_titles_distribution(players)
        st.plotly_chart(fig, use_container_width=False)

    styled_df = (
        players.sort_values("rating", ascending=False)[[
            "name", "player", "title", "country", "rating",
            "games_played_recent", "wins_recent", "draws_recent", "losses_recent",
            "games_played_total", "wins_total", "draws_total", "losses_total",
            "avg_score"
        ]]
        .reset_index(drop=True)
        .style.background_gradient(subset=["rating"], cmap="Greens")
        .background_gradient(subset=["avg_score"], cmap="Blues")
        .format({"avg_score": "{:.2f}", "rating": "{:,.0f}"})
    )

    st.subheader("Tabla completa (stats recientes + globales)")
    st.dataframe(styled_df, use_container_width=True)
