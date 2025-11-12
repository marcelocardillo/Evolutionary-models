import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# === DICCIONARIO DE TRADUCCIONES ===
translations = {
    "es": {
        "app_title": "Modelo de Transmisión Cultural por Sesgo Indirecto",
        "app_subtitle": "Simulación basada en éxito (sesgo indirecto por payoff)",
        "N": "Tamaño poblacional (N)",
        "t_max": "Cantidad de generaciones (tₘₐₓ)",
        "s": "Tamaño del sesgo (s)",
        "p_0": "Proporción inicial con rasgo A (p₀)",
        "run_sim": "Ejecutar simulación",
        "mean_label": "Promedio",
        "plot_title": "Proporción del rasgo A (N={N}, s={s})",
        "xlabel": "Generación",
        "ylabel": "p (proporción con rasgo A)",
        "show_table": "Mostrar tabla de resultados",
        "download_csv": "Descargar resultados como CSV",
        "csv_name": "simulacion_sesgada.csv",
        "footer_author": "Elaboración: Marcelo Cardillo, Prof. Adjunto de ELEMENTOS DE ANTROPOLOGÍA Y ARQUEOLOGÍA EVOLUTIVA, Facultad de Filosofía y Letras, Universidad de Buenos Aires.",
        "footer_source": "Basada en código de Alex Mesoudi para R, disponible en: *ABMmodels_model04_indirect_bias.Rmd*"
    },
    "en": {
        "app_title": "Cultural Transmission Model with Indirect Bias",
        "app_subtitle": "Success-based simulation (indirect bias by payoff)",
        "N": "Population size (N)",
        "t_max": "Number of generations (tₘₐₓ)",
        "s": "Bias strength (s)",
        "p_0": "Initial proportion with trait A (p₀)",
        "run_sim": "Run simulation",
        "mean_label": "Mean",
        "plot_title": "Proportion of trait A (N={N}, s={s})",
        "xlabel": "Generation",
        "ylabel": "p (proportion with trait A)",
        "show_table": "Show results table",
        "download_csv": "Download results as CSV",
        "csv_name": "biased_simulation.csv",
        "footer_author": "Developed by Marcelo Cardillo, Associate Professor of Anthropology and Evolutionary Archaeology, University of Buenos Aires.",
        "footer_source": "Based on R code by Alex Mesoudi, available at: *ABMmodels_model04_indirect_bias.Rmd*"
    }
}

# === SELECTOR DE IDIOMA ===
lang = st.sidebar.selectbox(
    "🌐 Language / Idioma",
    options=["es", "en"],
    format_func=lambda x: "Español" if x == "es" else "English"
)
t = translations[lang]

# === FUNCIÓN PRINCIPAL ===
def indirect_bias(N, s, p_0, t_max, r_max=10):
    output = pd.DataFrame(np.nan, index=range(t_max), columns=[f'run{i+1}' for i in range(r_max)])

    for r in range(r_max):
        # Generación inicial con probabilidades p_0 y 1-p_0
        traits = np.random.choice(["A", "B"], size=N, replace=True, p=[p_0, 1 - p_0])
        payoffs = np.where(np.array(traits) == "A", 1 + s, 1)
        output.iloc[0, r] = np.sum(np.array(traits) == "A") / N

        for t_ in range(1, t_max):
            relative_payoffs = payoffs / np.sum(payoffs)
            traits = np.random.choice(traits, size=N, replace=True, p=relative_payoffs)
            payoffs = np.where(np.array(traits) == "A", 1 + s, 1)
            output.iloc[t_, r] = np.sum(np.array(traits) == "A") / N

    return output

# === INTERFAZ DE USUARIO ===
st.title(t["app_title"])
st.markdown(t["app_subtitle"])

# Parámetros de simulación
N = st.slider(t["N"], min_value=100, max_value=10000, value=1000, step=100)
t_max = st.slider(t["t_max"], min_value=10, max_value=1000, value=150, step=10)
s = st.slider(t["s"], min_value=0.01, max_value=0.5, value=0.1, step=0.01)
p_0 = st.slider(t["p_0"], min_value=0.01, max_value=0.5, value=0.01, step=0.01)
r_max = 10  # número de repeticiones fijo

# Ejecución de simulación
if st.button(t["run_sim"]):
    output = indirect_bias(N=N, s=s, p_0=p_0, t_max=t_max, r_max=r_max)

    # --- Gráfico ---
    fig, ax = plt.subplots()
    ax.plot(output.mean(axis=1), label=t["mean_label"], linewidth=3, color="black")
    for col in output.columns:
        ax.plot(output[col], alpha=0.4)
    ax.set_title(t["plot_title"].format(N=N, s=s))
    ax.set_xlabel(t["xlabel"])
    ax.set_ylabel(t["ylabel"])
    ax.set_ylim(0, 1)
    st.pyplot(fig)

    # --- Mostrar tabla ---
    if st.checkbox(t["show_table"]):
        st.dataframe(output)

    # --- Botón de descarga ---
    csv = output.to_csv(index=False).encode("utf-8")
    st.download_button(
        label=t["download_csv"],
        data=csv,
        file_name=t["csv_name"],
        mime='text/csv',
    )

# === PIE DE PÁGINA ===
st.markdown(f"**{t['footer_author']}**")
st.markdown(t["footer_source"])

