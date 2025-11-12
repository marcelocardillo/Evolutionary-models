import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# === DICCIONARIO DE TRADUCCIONES ===
translations = {
    "es": {
        "app_title": "Modelo de Transmisión Cultural No Sesgada",
        "N": "Tamaño poblacional (N)",
        "t_max": "Cantidad de generaciones (tₘₐₓ)",
        "r_max": "Número de corridas (rₘₐₓ)",
        "run_sim": "Ejecutar simulación",
        "mean_label": "Promedio",
        "plot_title": "Proporción del rasgo A (N={N})",
        "xlabel": "Generación",
        "ylabel": "p (proporción con rasgo A)",
        "show_table": "Mostrar tabla de resultados",
        "csv_name": "simulacion_no_sesgada.csv",
        "footer_author": "Elaboración: Marcelo Cardillo, Prof. Adjunto de ELEMENTOS DE ANTROPOLOGÍA Y ARQUEOLOGÍA EVOLUTIVA, Facultad de Filosofía y Letras, Universidad de Buenos Aires.",
        "footer_source": "Basada en código de Alex Mesoudi para R, disponible en: *ABMmodels_model01_unbiased_transmission.Rmd*"
    },
    "en": {
        "app_title": "Unbiased Cultural Transmission Model",
        "app_subtitle": "Simulation based on Mesoudi’s model",
        "N": "Population size (N)",
        "t_max": "Number of generations (tₘₐₓ)",
        "r_max": "Number of runs (rₘₐₓ)",
        "run_sim": "Run simulation",
        "mean_label": "Mean",
        "plot_title": "Proportion of trait A (N={N})",
        "xlabel": "Generation",
        "ylabel": "p (proportion with trait A)",
        "show_table": "Show results table",
        "csv_name": "unbiased_simulation.csv",
        "footer_author": "Developed by Marcelo Cardillo, Associate Professor of Anthropology and Evolutionary Archaeology, University of Buenos Aires.",
        "footer_source": "Based on R code by Alex Mesoudi, available at: *ABMmodels_model01_unbiased_transmission.Rmd*"
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
def unbiased_transmission(N, t_max, r_max):
    output = pd.DataFrame(np.nan, index=range(t_max), columns=[f'run{i+1}' for i in range(r_max)])
    for r in range(r_max):
        # Generación inicial
        traits = np.random.choice(["A", "B"], size=N, replace=True)
        output.iloc[0, r] = np.sum(traits == "A") / N
        for t_ in range(1, t_max):
            traits = np.random.choice(traits, size=N, replace=True)
            output.iloc[t_, r] = np.sum(traits == "A") / N
    return output

# === INTERFAZ DE USUARIO ===
st.title(t["app_title"])
st.markdown(t["app_subtitle"])

# Parámetros de entrada
N = st.slider(t["N"], min_value=10, max_value=500, value=100, step=10)
t_max = st.slider(t["t_max"], min_value=10, max_value=500, value=200, step=10)
r_max = st.slider(t["r_max"], min_value=1, max_value=20, value=5, step=1)

# Ejecutar simulación
if st.button(t["run_sim"]):
    output = unbiased_transmission(N, t_max, r_max)

    # Graficar resultados
    fig, ax = plt.subplots()
    ax.plot(output.mean(axis=1), label=t["mean_label"], linewidth=3, color="black")
    for col in output.columns:
        ax.plot(output[col], alpha=0.5)
    ax.set_title(t["plot_title"].format(N=N))
    ax.set_xlabel(t["xlabel"])
    ax.set_ylabel(t["ylabel"])
    ax.set_ylim(0, 1)
    st.pyplot(fig)

    # Mostrar tabla de resultados
    if st.checkbox(t["show_table"]):
        st.dataframe(output)

# === PIE DE PÁGINA ===
st.markdown(f"**{t['footer_author']}**")
st.markdown(t["footer_source"])

