import streamlit as st
import pandas as pd
import numpy as np
from geopy.geocoders import Nominatim

# Función para obtener la media mundial por edad y país
def obtener_media_mundial():
    # Datos de ejemplo para la media mundial de personalidad según la edad y el país
    data = {
        "País": ["Estados Unidos", "España", "México", "Argentina", "Francia", "Brasil"],
        "Edad": ["18-25", "26-35", "36-45", "46-60", "60+"],
        "Extroversión": [0.75, 0.65, 0.55, 0.45, 0.35],
        "Amabilidad": [0.70, 0.65, 0.60, 0.55, 0.50],
        "Neuroticismo": [0.60, 0.55, 0.50, 0.45, 0.40],
        "Apertura a nuevas experiencias": [0.80, 0.75, 0.70, 0.65, 0.60],
        "Responsabilidad": [0.70, 0.72, 0.75, 0.80, 0.85],
    }
    df = pd.DataFrame(data)
    return df

# Función para determinar el rango de edad
def obtener_rango_edad(edad):
    if edad < 25:
        return "18-25"
    elif 25 <= edad < 35:
        return "26-35"
    elif 35 <= edad < 45:
        return "36-45"
    elif 45 <= edad < 60:
        return "46-60"
    else:
        return "60+"

# Función para obtener el país del usuario usando la geolocalización
def obtener_pais(ubicacion):
    geolocator = Nominatim(user_agent="streamlit_personality_analysis")
    location = geolocator.geocode(ubicacion)
    if location:
        return location.address.split(',')[-1].strip()  # Extraer el país
    else:
        return None

# Función principal de la aplicación Streamlit
def app():
    st.title('Análisis de Personalidad Global')

    st.write("""
    Esta aplicación compara tu perfil de personalidad con la media mundial, teniendo en cuenta tu edad y país de procedencia.
    Por favor, completa el siguiente formulario con tu edad, ubicación y puntúa sobre 5 tu personalidad en 5 aspectos clave.
    """)

    # Entrada de edad y ubicación
    edad = st.number_input('¿Cuántos años tienes?', min_value=10, max_value=100, step=1)
    ubicacion = st.text_input('¿De qué país eres? (Escribe el nombre de tu país)')

    # Determinar el rango de edad
    rango_edad = obtener_rango_edad(edad)

    # Obtener la media mundial
    media_mundial = obtener_media_mundial()

    # Si el usuario proporciona una ubicación
    if ubicacion:
        pais_usuario = obtener_pais(ubicacion)
        if pais_usuario:
            st.write(f"Tu país es: {pais_usuario}")
            # Filtrar datos para ese país
            datos_pais = media_mundial[media_mundial["País"] == pais_usuario]

            if not datos_pais.empty:
                datos_rango = datos_pais[datos_pais["Edad"] == rango_edad]
                st.write(f"Comparación con la media de {pais_usuario} para la edad {rango_edad}:")
                st.table(datos_rango)
            else:
                st.write(f"No se encontraron datos para {pais_usuario}. Mostrando la media mundial.")
        else:
            st.write("No se pudo determinar tu país. Asegúrate de escribir correctamente el nombre del país.")
            st.write("Mostrando la media mundial...")
            # Filtrar por edad global si no se encuentra país
            datos_rango = media_mundial[media_mundial["Edad"] == rango_edad]
            st.table(datos_rango)

    # Recopilar respuestas de personalidad
    st.write("Por favor, puntúa los siguientes aspectos de tu personalidad (1: Muy bajo, 5: Muy alto):")

    extroversion = st.slider("Extroversión", 1, 5)
    amabilidad = st.slider("Amabilidad", 1, 5)
    neuroticismo = st.slider("Neuroticismo", 1, 5)
    apertura = st.slider("Apertura a nuevas experiencias", 1, 5)
    responsabilidad = st.slider("Responsabilidad", 1, 5)

    # Comparación con la media mundial
    st.subheader("Tu perfil vs la media mundial:")

    st.write(f"**Extroversión:** Tu puntuación: {extroversion}")
    st.write(f"**Amabilidad:** Tu puntuación: {amabilidad}")
    st.write(f"**Neuroticismo:** Tu puntuación: {neuroticismo}")
    st.write(f"**Apertura a nuevas experiencias:** Tu puntuación: {apertura}")
    st.write(f"**Responsabilidad:** Tu puntuación: {responsabilidad}")
    
    st.write("¡Gracias por usar la aplicación!")

if __name__ == "__main__":
    app()
