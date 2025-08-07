# config_remota.py
import psycopg2
import streamlit as st
from dotenv import load_dotenv
import os

# --- Cargar variables del archivo .env ---
load_dotenv()

# --- Configuración de conexión a la base de datos PostgreSQL Remota ---
DB_CONFIG = {
    "dbname": os.getenv("DB_NAME_REMOTA"),
    "user": os.getenv("DB_USER_REMOTA"),
    "password": os.getenv("DB_PASSWORD_REMOTA"),
    "host": os.getenv("DB_HOST_REMOTA"),
    "port": os.getenv("DB_PORT_REMOTA")
}

def get_connection():
    """
    Crea y retorna una conexión a la base de datos PostgreSQL remota.
    Si falla, muestra un mensaje de error en Streamlit y retorna None.
    """
    try:
        return psycopg2.connect(**DB_CONFIG)
    except Exception as e:
        st.error(f"Error al conectar a PostgreSQL remoto: {e}")
        return None
