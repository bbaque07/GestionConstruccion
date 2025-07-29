# config.py
import psycopg2
import streamlit as st
from dotenv import load_dotenv
import os

# --- Cargar variables del archivo .env ---
load_dotenv()

# --- Configuración de conexión a la base de datos PostgreSQL ---
DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT")
}

def get_connection():
    """
    Crea y retorna una conexión a la base de datos PostgreSQL.
    Si falla, muestra un mensaje de error en Streamlit y retorna None.
    """
    try:
        return psycopg2.connect(**DB_CONFIG)
    except Exception as e:
        st.error(f"Error al conectar a PostgreSQL: {e}")
        return None
