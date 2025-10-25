import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Random Walk", layout="centered")

st.title("Simulación de Random Walk")

# --- Panel de control (en el cuerpo principal, no sidebar) ---
st.subheader("Parámetros del modelo")

col1, col2 = st.columns(2)
with col1:
    n_generaciones = st.number_input("Número de generaciones", 100, 5000, 1000, step=100)
    n_trayectorias = st.number_input("Número de trayectorias", 1, 200, 1, step=1)
with col2:
    bias = st.slider("Sesgo (negativo a positivo)", -0.5, 0.5, 0.0, step=0.05)
    semilla = st.number_input("Semilla aleatoria", 0, 9999, 1055)

# --- Configuración del modelo ---
np.random.seed(int(semilla))
p = np.clip(0.5 + bias, 0, 1)  # probabilidad de aumento
st.markdown(f"**Probabilidad efectiva de aumento:** {p:.2f}")

# --- Simulación ---
fig, ax = plt.subplots(figsize=(8, 5))

for i in range(int(n_trayectorias)):
    valor_inicial = np.random.randint(1, 21)
    pasos = np.where(np.random.rand(int(n_generaciones) - 1) < p, 1, -1)
    valores = np.concatenate(([valor_inicial], valor_inicial + np.cumsum(pasos)))

    ax.plot(valores, lw=1.5, alpha=0.7)
    ax.axhline(y=valor_inicial, color="red", linestyle="dotted", alpha=0.5)

ax.set_title(f"{n_trayectorias} trayectorias | bias = {bias}")
ax.set_xlabel("Generación")
ax.set_ylabel("Valor")
ax.grid(True, linestyle="--", alpha=0.4)

# --- Mostrar gráfico debajo ---
st.pyplot(fig)

# --- Texto explicativo ---
st.markdown("""
**Descripción del modelo**  
El *random walk* simula una variable que cambia ±1 en cada generación.  
- `bias` > 0 → tendencia ascendente  
- `bias` = 0 → neutral  
- `bias` < 0 → tendencia descendente  

Cada trayectoria comienza con un valor inicial aleatorio entre 1 y 20.  
Las líneas punteadas rojas indican el valor inicial de cada trayectoria.
""")
st.write("Elaboracion: Marcelo Cardillo, Facultad de Filosofia y Letras, Universidad de Buenos Aires.") 
