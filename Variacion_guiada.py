import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def unbiased_transmission(N, t_max, r_max):
    # Creamos un DataFrame vacío
    output = pd.DataFrame(np.nan, index=range(t_max), columns=[f'run{i+1}' for i in range(r_max)])

    for r in range(r_max):
        # Generación inicial
        traits = np.random.choice(["A", "B"], size=N, replace=True)
        output.iloc[0, r] = np.sum(traits == "A") / N

        for t in range(1, t_max):
            traits = np.random.choice(traits, size=N, replace=True)
            output.iloc[t, r] = np.sum(traits == "A") / N

    return output

# Streamlit UI
st.title("Modelo de Transmisión Cultural No Sesgada")
st.markdown("Simulación basada en el modelo de Mesoudi")

# Parámetros de entrada
N = st.slider("Tamaño poblacional (N)", min_value=10, max_value=500, value=100, step=10)
t_max = st.slider("Cantidad de generaciones (t_max)", min_value=10, max_value=500, value=200, step=10)
r_max = st.slider("Número de corridas (r_max)", min_value=1, max_value=20, value=5, step=1)

# Ejecutar simulación
if st.button("Ejecutar simulación"):
    output = unbiased_transmission(N, t_max, r_max)

    # Graficar
    fig, ax = plt.subplots()
    ax.plot(output.mean(axis=1), label="Promedio", linewidth=3, color="black")

    for col in output.columns:
        ax.plot(output[col], alpha=0.5)

    ax.set_title(f"Proporción del rasgo A (N={N})")
    ax.set_xlabel("Generación")
    ax.set_ylabel("p (proporción con rasgo A)")
    ax.set_ylim(0, 1)
    st.pyplot(fig)

    # Mostrar datos si se desea
    if st.checkbox("Mostrar tabla de resultados"):
        st.dataframe(output)
