import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Título y descripción
# -----------------------------
st.title("Simulación de selección direccional sobre un rasgo cuantitativo")
st.markdown("""
Este modelo muestra cómo un rasgo cuantitativo cambia a lo largo de las generaciones 
bajo selección direccional, con posibilidad de incorporar ***ruido aleatorio*** (error en el mecanismo de transmisión cultural).
---
""")

# -----------------------------
# Entradas del usuario
# -----------------------------
valor_inicial = st.number_input("Valor inicial del rasgo", value=5.0)
n_gen = st.number_input("Número de generaciones", min_value=10, max_value=10000, value=1000, step=10)
coeficiente_seleccion = st.slider("Intensidad de selección direccional (+/-)", -0.05, 0.05, 0.015, 0.001)

# Checkbox para activar/desactivar el ruido
ruido = st.checkbox("Agregar ruido aleatorio (variabilidad ambiental)")

# Si el usuario activa el ruido, se muestra un slider para su intensidad
if ruido:
    intensidad_ruido = st.slider("Intensidad del ruido (desvío estándar)", 0.0, 2.0, 0.5, 0.05)
else:
    intensidad_ruido = 0.0  # sin ruido

# -----------------------------
# Botón para ejecutar la simulación
# -----------------------------
if st.button("Ejecutar simulación"):
    np.random.seed(123)
    trait = np.zeros(int(n_gen))
    trait[0] = valor_inicial

    # Bucle de simulación
    for i in range(1, int(n_gen)):
        ruido_actual = np.random.normal(0, intensidad_ruido) if ruido else 0
        trait[i] = trait[i - 1] + coeficiente_seleccion + ruido_actual

    # -----------------------------
    # Gráfico del resultado
    # -----------------------------
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(trait, color="darkgreen", linewidth=2)
    ax.axhline(valor_inicial, linestyle="--", color="gray")
    ax.set_title("Tendencia direccional del rasgo")
    ax.set_xlabel("Generaciones")
    ax.set_ylabel("Valor del rasgo")
    st.pyplot(fig)

    # -----------------------------
    # Resumen numérico
    # -----------------------------
    st.write(f"**Valor final del rasgo:** {trait[-1]:.2f}")
    st.write(f"**Cambio total:** {trait[-1] - valor_inicial:.2f}")
    if ruido:

        st.write(f"**Intensidad del ruido:** {intensidad_ruido:.2f}")
        st.write("Elaboracion: Marcelo Cardillo, Facultad de Filosofia y Letras, Universidad de Buenos Aires.") 

