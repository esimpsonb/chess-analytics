import streamlit as st
import pandas as pd
from source.utils import (
    plot_top_openings,
    plot_openings_decisivas,
    plot_openings_distribution,
)

def render(games):
    st.header("📊 Estadísticas de aperturas (global)")

    # --- Top 10 aperturas ---
    top_openings = (
        games["eco_name"].value_counts()
        .head(10)
        .reset_index()
    )
    top_openings.columns = ["eco_name", "count"]

    fig1 = plot_top_openings(top_openings)
    st.plotly_chart(fig1, use_container_width=True)

    # --- Decisivas por apertura ---
    results = []
    for eco in top_openings["eco_name"]:
        subset = games[games["eco_name"] == eco]
        total = len(subset)

        # Empates: se cuentan solo una vez por partida
        draws = subset["white_result"].isin([
            "agreed", "repetition", "stalemate",
            "timevsinsufficient", "insufficient", "50move"
        ]).sum()

        decisivas = total - draws
        ratio_decisivas = decisivas / total if total > 0 else 0

        results.append({
            "eco_name": eco,
            "decisivas": decisivas,
            "ratio_decisivas": ratio_decisivas
        })

    decisivas_df = pd.DataFrame(results).sort_values("ratio_decisivas", ascending=True)

    fig2 = plot_openings_decisivas(decisivas_df)
    st.plotly_chart(fig2, use_container_width=True)

    # --- Distribución global ---
    fig3 = plot_openings_distribution(top_openings)
    st.plotly_chart(fig3, use_container_width=True)
