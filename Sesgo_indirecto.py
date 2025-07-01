import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def indirect_bias(N, s, p_0, t_max, r_max=10):
    output = pd.DataFrame(np.nan, index=range(t_max), columns=[f'run{i+1}' for i in range(r_max)])

    for r in range(r_max):
        # Generación inicial con probabilidades p_0 y 1-p_0
        traits = np.random.choice(["A", "B"], size=N, replace=True, p=[p_0, 1 - p_0])
        payoffs = np.where(np.array(traits) == "A", 1 + s, 1)
        output.iloc[0, r] = np.sum(np.array(traits) == "A") / N

        for t in range(1, t_max):
            relative_payoffs = payoffs / np.sum(payoffs)
            traits = np.random.choice(traits, size=N, replace=True, p=relative_payoffs)
            payoffs = np.where(np.array(traits) == "A", 1 + s, 1)
            output.iloc[t, r] = np.sum(np.array(traits) == "A") / N

    return output

# === STREAMLIT INTERFAZ ===
st.title("Modelo de Transmisión Cultural por Sesgo Indirecto")
st.markdown("Simulación basada en éxito (sesgo indirecto por payoff)")

# Sliders para parámetros
N = st.slider("Tamaño poblacional (N)", min_value=100, max_value=10000, value=1000, step=100)
t_max = st.slider("Cantidad de generaciones (t_max)", min_value=10, max_value=1000, value=150, step=10)
s = st.slider("Tamaño del sesgo (s)", min_value=0.01, max_value=0.5, value=0.1, step=0.01)
p_0 = st.slider("Proporción inicial con rasgo A (p₀)", min_value=0.01, max_value=0.5, value=0.01, step=0.01)
r_max = 10  # fijo como pediste

# Ejecutar simulación
if st.button("Ejecutar simulación"):
    output = indirect_bias(N=N, s=s, p_0=p_0, t_max=t_max, r_max=r_max)

    # Plot
    fig, ax = plt.subplots()
    ax.plot(output.mean(axis=1), label="Promedio", linewidth=3, color="black")
    for col in output.columns:
        ax.plot(output[col], alpha=0.4)
    ax.set_title(f"Proporción del rasgo A (N={N}, s={s})")
    ax.set_xlabel("Generación")
    ax.set_ylabel("p (proporción con rasgo A)")
    ax.set_ylim(0, 1)
    st.pyplot(fig)

    # Mostrar tabla
    if st.checkbox("Mostrar tabla de resultados"):
        st.dataframe(output)

    # Descargar CSV
    csv = output.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Descargar resultados como CSV",
        data=csv,
        file_name='simulacion_sesgada.csv',
        mime='text/csv',
    )
st.write("Elaboración: Marcelo Cardillo, Prof. Adjunto de ELEMENTOS DE ANTROPOLOGÍA Y ARQUEOLOGÍA EVOLUTIVA, Facultad de Filosofía y Letras, Universidad de Buenos Aires.")